"""Bounded diagnostics and one proven native-save repair; no openpyxl saving."""
from copy import copy, deepcopy
import os
import posixpath
import zipfile
from edit_common import read_book, style, content, capture, cells, require, stage_path
from edit_common import dimension_signature

def extension_guard(wb):
    return (wb.sheetnames, {(s.title,c.coordinate):content(c) for s in wb for c in s._cells.values() if c.value is not None},
            {(s.title,k,a):dimension_signature(d) for s in wb for k in ('row_dimensions','column_dimensions') for a,d in getattr(s,k).items()},
            {s.title:str(s.merged_cells) for s in wb})

def capture_protected(wb, full=False):
    if full: require(sum(len(s._cells) for s in wb)<=20000,'Large custom edits need bounded extension design')
    old={}
    for s in wb:
        candidates=list(s._cells.values()) if full else [s[m.start_cell.coordinate] for m in s.merged_cells.ranges]
        for c in candidates:
            if c.__class__.__name__!='MergedCell':old[s.title,c.coordinate]=(content(c),style(c))
    dims={(s.title,k,a):dimension_signature(d) for s in wb for k in ('row_dimensions','column_dimensions') for a,d in getattr(s,k).items()} if full else {}
    return dict(old=old,dims=dims)

def verify_protected(wb, baseline, p):
    changes={}
    for op in p['operations']:
        for sh,addr,_,_ in cells(op['sheet'],op['range']):changes.setdefault((sh,addr),set()).add(op['kind'])
    for (sh,addr),(before,styles) in baseline['old'].items():
        c=wb[sh][addr];allowed=changes.get((sh,addr),set());after=style(c)
        if not allowed & {'value','formula'}:require(content(c)==before,f'Protected content changed: {sh}!{addr}')
        for k,a in styles.items():
            b=after[k]
            if k=='fill' and 'fill_color' in allowed:continue
            if k=='font' and 'font_color' in allowed:a,b=copy(a),copy(b);a.color=b.color=None
            require(a==b,f'Protected {k} changed: {sh}!{addr}; expected {a!r}, actual {b!r}')
    for (sh,k,addr),expected in baseline['dims'].items():
        block=p.get('append_block')
        if block and sh==block['sheet'] and k=='row_dimensions':
            from edit_common import bounds
            _,start,_,end=bounds(block['range'])
            if start<=addr<=end:continue
        d=getattr(wb[sh],k).get(addr)
        require(d is not None and dimension_signature(d)==expected,f'Protected dimension changed: {sh}/{k}/{addr}')

PROPERTIES = ('data_validations', 'page_setup', 'page_margins', 'print_options',
              'sheet_format', 'sheet_properties', 'print_area', 'print_title_rows',
              'print_title_cols')

def capture_metadata(wb):
    return {s.title: {k: deepcopy(getattr(s, k)) for k in PROPERTIES} for s in wb}

def verify_metadata(wb, baseline):
    for name, props in (baseline or {}).items():
        require(name in wb.sheetnames, f'Old sheet missing: {name}')
        for key, before in props.items():
            require(getattr(wb[name], key) == before, f'Old sheet metadata changed: {name}/{key}')

def changed_cells(p):
    return {(s,a) for op in p['operations'] for s,a,_,_ in cells(op['sheet'],op['range'])}

def restore_merged_wrap(path, baseline, p):
    """Only untouched merged anchors whose sole difference is wrap True -> off.

    Clone a style for each affected cell style; never mutate a shared style in place.
    Resolve actual worksheet package paths via relationships, not sheet indices.
    lxml keeps namespace declarations used by mc:Ignorable; reopen follows in caller.
    """
    changed = changed_cells(p)
    wb = read_book(path)
    repairs = []
    try:
        for (name, addr), (old_content, old_style) in baseline['old'].items():
            if (name, addr) in changed: continue
            c = wb[name][addr]
            current = style(c)
            if old_content != content(c) or old_style == current: continue
            if [k for k in current if current[k] != old_style[k]] != ['alignment']: continue
            a, b = old_style['alignment'], copy(current['alignment'])
            if a.wrapText is not True or b.wrapText not in (None, False): continue
            b.wrapText = True
            if a != b: continue
            if not any(addr == m.start_cell.coordinate and m.size['columns']*m.size['rows'] > 1
                       for m in wb[name].merged_cells.ranges): continue
            repairs.append((name, addr))
    finally: wb.close()
    if not repairs: return 0
    from lxml import etree as ET
    ns = {'m':'http://schemas.openxmlformats.org/spreadsheetml/2006/main',
          'r':'http://schemas.openxmlformats.org/officeDocument/2006/relationships'}
    with zipfile.ZipFile(path) as z:
        entries = {i.filename:(i,z.read(i.filename)) for i in z.infolist()}
    parser = ET.XMLParser(resolve_entities=False, no_network=True)
    def parse(part): return ET.fromstring(entries[part][1], parser)
    rels = {e.get('Id'):e.get('Target') for e in parse('xl/_rels/workbook.xml.rels')
            if e.get('TargetMode') != 'External'}
    sheets = {}
    for e in parse('xl/workbook.xml').findall('m:sheets/m:sheet', ns):
        target = rels[e.get('{'+ns['r']+'}id')]
        part = target.lstrip('/') if target.startswith('/') else posixpath.normpath('xl/'+target)
        require(part.startswith('xl/') and part in entries, 'Unrecognized worksheet relationship')
        sheets[e.get('name')] = part
    styles = parse('xl/styles.xml'); xfs = styles.find('m:cellXfs', ns)
    trees, nodes, remap = {}, {}, {}
    for name, addr in repairs:
        part = sheets[name]
        if part not in trees:
            trees[part] = parse(part)
            nodes[part] = {c.get('r'):c for c in trees[part].findall('m:sheetData/m:row/m:c', ns)}
        c = nodes[part][addr]; sid = int(c.get('s', '0'))
        if sid not in remap:
            xf = deepcopy(xfs[sid]); align = xf.find('m:alignment', ns)
            if align is None: align = ET.SubElement(xf, '{'+ns['m']+'}alignment')
            align.set('wrapText','1'); xf.set('applyAlignment','1')
            remap[sid] = len(xfs); xfs.append(xf)
        c.set('s',str(remap[sid]))
    xfs.set('count',str(len(xfs)))
    trees['xl/styles.xml'] = styles
    for part, tree in trees.items():
        entries[part] = entries[part][0], ET.tostring(tree,encoding='utf-8',xml_declaration=True)
    out = stage_path(path)
    try:
        with zipfile.ZipFile(out,'w') as z:
            for info, data in entries.values(): z.writestr(info,data)
        os.replace(out,path)
    finally:
        if out.exists(): out.unlink()
    return len(repairs)

def diagnose(path, p, baseline, created, limit=12):
    """Run only on failure; retain staged file for deeper inspection, bounded output."""
    wb = None
    result = []
    def add(where, prop, before, after):
        if before != after and len(result) < limit:
            result.append(dict(location=str(where), property=prop,
                               before=repr(before)[:700], after=repr(after)[:700]))
    try:
        wb = read_book(path)
        now = capture(wb,p)
        for prop in ('rows','cols','merges'):
            for key in dict.fromkeys([*baseline[prop], *now[prop]]):
                # New column widths use native units and were checked through Excel.
                if prop == 'cols' and key in {s['name'] for s in p.get('new_sheets',[])}: continue
                before, after = baseline[prop].get(key),now[prop].get(key)
                if prop == 'rows' and key[0] in {s['name'] for s in p.get('new_sheets',[]) if 'row_height' in s}:
                    before = (None,*before[1:]) if before else before
                    after = (None,*after[1:]) if after else after
                add(key,prop,before,after)
        snapshots = dict((created or {}).get('old', {}))
        snapshots.update(baseline['targets'])
        allowed = baseline['changes']
        for (name,addr),(old_content,old_style) in snapshots.items():
            c=wb[name][addr]; current=style(c); kinds=allowed.get((name,addr),set())
            if not kinds & {'value','formula'}: add(f'{name}!{addr}','content',old_content,content(c))
            for prop, before in old_style.items():
                after=current[prop]
                if prop == 'fill' and 'fill_color' in kinds: continue
                if prop == 'font' and 'font_color' in kinds:
                    before,after=copy(before),copy(after);before.color=after.color=None
                add(f'{name}!{addr}',prop,before,after)
            if len(result)>=limit: break
    except Exception as e: result.append({'diagnostic_error':str(e)[:500]})
    finally:
        if wb is not None: wb.close()
    return result
