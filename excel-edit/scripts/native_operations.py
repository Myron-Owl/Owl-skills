"""Optional native-only format inheritance and single-cell validation edits."""
from copy import copy, deepcopy
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.worksheet.cell_range import CellRange
from edit_common import require, bounds, cells, style, effective_style_array

FIELDS = ('type','operator','formula1','formula2','allowBlank','showErrorMessage',
          'showInputMessage','errorTitle','error','promptTitle','prompt','errorStyle')

def signature(rule):
    return {k:getattr(rule,k) for k in FIELDS} if rule is not None else None

def rule_at(ws, addr):
    rules=[d for d in ws.data_validations.dataValidation if addr in d.sqref]
    require(len(rules)<=1,f'Overlapping validation rules: {ws.title}!{addr}')
    return rules[0] if rules else None

def prepare(wb,p):
    result={'styles':{},'rules':{}}
    seen=set()
    for spec in p.get('format_copies',[]):
        require(set(spec)=={'sheet','range','source_sheet','source_range'},'Format copy fields invalid')
        x,y,z,t=bounds(spec['range']);a,b,c,d=bounds(spec['source_range'])
        require((z-x,t-y)==(c-a,d-b) and (z-x+1)*(t-y+1)<=256,'Format copy shapes differ or exceed 256 cells')
        src=wb[spec['source_sheet']];dst=wb[spec['sheet']]
        require(not dst.protection.sheet,'Protected format destination')
        for ws,area in ((src,spec['source_range']),(dst,spec['range'])):
            from append_block import intersects
            require(not any(intersects(area,m) for m in ws.merged_cells.ranges),'Format copy needs unmerged cells')
            require(not any(intersects(area,r) for cf in ws.conditional_formatting for r in cf.sqref.ranges),'Conditional formats need scoped inheritance')
        values=[copy(effective_style_array(src.cell(b+dy,a+dx))) for _,_,dy,dx in cells(dst.title,spec['range'])]
        for (_,addr,_,_),st in zip(cells(dst.title,spec['range']),values):
            require((dst.title,addr) not in seen,'Overlapping format copies')
            seen.add((dst.title,addr));dst[addr]._style=st
            result['styles'][dst.title,addr]=style(dst[addr])
    seen=set()
    for spec in p.get('validations',[]):
        require(set(spec)=={'sheet','cell','before','after'},'Validation needs sheet/cell/before/after')
        x,y,z,t=bounds(spec['cell']);require((x,y)==(z,t),'Validation edit must target one cell')
        ws=wb[spec['sheet']];addr=spec['cell'];key=(ws.title,addr)
        require(key not in seen and not ws.protection.sheet,'Duplicate/protected validation target');seen.add(key)
        require(not any(addr in m for m in ws.merged_cells.ranges),'Merged validation target needs scoped handling')
        old=rule_at(ws,addr)
        require(signature(old)==spec['before'],f'Validation before conflict: {ws.title}!{addr}; actual {signature(old)!r}')
        after=spec['after']
        require(isinstance(after,dict) and set(after)<=set(FIELDS) and after.get('type') in ('whole','decimal','custom'),'Unsupported validation definition')
        if old:
            ranges=list(old.sqref.ranges)
            shared=str(old.sqref)!=addr
            if shared:
                require(old.type in ('whole','decimal') and all(v is None or str(v).replace('.','',1).lstrip('-').isdigit() for v in (old.formula1,old.formula2)),
                        'Shared relative/list validation needs scoped handling; no implicit rebasing')
            keep=[]
            for r in ranges:
                if addr not in r:keep.append(str(r));continue
                boxes=[(r.min_col,r.min_row,r.max_col,y-1),(r.min_col,y+1,r.max_col,r.max_row),
                       (r.min_col,y,x-1,y),(x+1,y,r.max_col,y)]
                keep.extend(str(CellRange(min_col=a,min_row=b,max_col=c,max_row=d)) for a,b,c,d in boxes if a<=c and b<=d)
            ws.data_validations.dataValidation.remove(old)
            if keep:
                old.sqref=' '.join(keep);ws.add_data_validation(old)
        rule=DataValidation(**after);rule.add(addr);ws.add_data_validation(rule)
        result['rules'][key]=signature(rule)
    return result

def apply(target,p,expected):
    for spec in p.get('format_copies',[]):
        target.Worksheets(spec['source_sheet']).Range(spec['source_range']).Copy()
        target.Worksheets(spec['sheet']).Range(spec['range']).PasteSpecial(Paste=-4122)
        target.Application.CutCopyMode=False
    operators={'between':1,'notBetween':2,'equal':3,'notEqual':4,'greaterThan':5,'lessThan':6,'greaterThanOrEqual':7,'lessThanOrEqual':8}
    for (sheet,addr),s in expected['rules'].items():
        v=target.Worksheets(sheet).Range(addr).Validation
        v.Delete()
        v.Add(Type={'whole':1,'decimal':2,'custom':7}[s['type']],
              AlertStyle={'stop':1,'warning':2,'information':3}.get(s['errorStyle'],1),
              Operator=operators.get(s['operator'],1),Formula1=s['formula1'],Formula2=s['formula2'])
        for prop,field in [('IgnoreBlank','allowBlank'),('ShowError','showErrorMessage'),('ShowInput','showInputMessage'),
                           ('ErrorTitle','errorTitle'),('ErrorMessage','error'),('InputTitle','promptTitle'),('InputMessage','prompt')]:
            setattr(v,prop,s[field] if s[field] is not None else (False if prop in ('IgnoreBlank','ShowError','ShowInput') else ''))

def validation_map(ws):
    out={}
    for rule in ws.data_validations.dataValidation:
        for area in rule.sqref.ranges:
            require(area.size['columns']*area.size['rows']<=20000,'Large validation region needs scoped handling')
            for _,addr,_,_ in cells(ws.title,str(area)):
                require(addr not in out,'Overlapping validation rules')
                s=signature(rule)
                for k in ('errorTitle','error','promptTitle','prompt'):s[k]=s[k] or None
                s['errorStyle']=s['errorStyle'] or 'stop'
                for k in ('formula1','formula2'):
                    if s[k] and s[k].startswith('='):s[k]=s[k][1:]
                if s['type']=='custom':s['operator']=None
                out[addr]=s
                require(len(out)<=20000,'Validation map exceeds bounded extension limit')
    return out
