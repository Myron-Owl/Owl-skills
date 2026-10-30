"""Check JSONL localization pairs. Does not edit inputs. Exit 1 = structural errors."""
import argparse, collections, json, re
from pathlib import Path

TOKENS=re.compile(r"/\*[A-Za-z_][\w.]*\*/|~(?:[A-Za-z_][\w]*|/)~|::[A-Za-z_][\w.]*::|\{[^{}\n]*\}|\[[A-Za-z_0-9][\w.!:-]*\]|%(?:\([^)]+\))?[-+0-9.#]*[sdifuxX]|%\d+")
TAGS=re.compile(r"</?[A-Za-z_][^<>]*>|</?::[A-Za-z_]\w*::>")
NUMBERS=re.compile(r"(?<!\w)[+-]?\d+(?:[.,]\d+)?%?")
def tokens(s):
    return collections.Counter(TOKENS.findall(s))
def tags(s):
    return collections.Counter(re.sub(r"\s*/>$","/>",t) for t in TAGS.findall(s))
def nums(s):
    s=TAGS.sub("",s); s=TOKENS.sub("",s)
    return collections.Counter(NUMBERS.findall(s))
def delta(a,b):
    return {"missing":list((a-b).elements()),"added":list((b-a).elements())}
def inspect(rows,source_field="en",target_field="zh",max_chars=None):
    issues=[]; seen={}
    for i,row in enumerate(rows,1):
        key=str(row.get("id",row.get("key",i)))
        scope=(str(row.get("game","")),str(row.get("variant","")),key)
        a=row.get(source_field); b=row.get(target_field)
        def add(level,kind,detail): issues.append({"row":i,"id":key,"severity":level,"kind":kind,"detail":detail})
        if not isinstance(a,str) or not isinstance(b,str):
            add("error","missing_text_field",[source_field,target_field]); continue
        if scope in seen and seen[scope]!=(a,b): add("error","duplicate_id_conflict",key)
        seen[scope]=(a,b)
        if a.strip() and not b.strip(): add("error","empty_translation","Nonempty source")
        if tokens(a)!=tokens(b): add("error" if set(tokens(a))!=set(tokens(b)) else "review","placeholder_or_control_mismatch",delta(tokens(a),tokens(b)))
        if tags(a)!=tags(b): add("error","markup_mismatch",delta(tags(a),tags(b)))
        if nums(a)!=nums(b): add("review","number_difference",delta(nums(a),nums(b)))
        if max_chars is not None:
            plain=TAGS.sub("",TOKENS.sub("",b))
            if len(plain)>max_chars: add("review","character_limit",{"actual":len(plain),"limit":max_chars})
    return issues
def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("input",type=Path); p.add_argument("--source-field",default="en"); p.add_argument("--target-field",default="zh")
    p.add_argument("--max-chars",type=int); p.add_argument("--report",type=Path)
    args=p.parse_args()
    rows=[json.loads(s) for s in args.input.read_text(encoding="utf-8-sig").splitlines() if s.strip()]
    issues=inspect(rows,args.source_field,args.target_field,args.max_chars)
    result={"rows":len(rows),"errors":sum(x["severity"]=="error" for x in issues),"reviews":sum(x["severity"]=="review" for x in issues),"issues":issues}
    rendered=json.dumps(result,ensure_ascii=False,indent=2)
    if args.report:
        if args.report.resolve()==args.input.resolve(): p.error("Report must not overwrite input.")
        args.report.parent.mkdir(parents=True,exist_ok=True); args.report.write_text(rendered,encoding="utf-8")
        print(json.dumps({k:v for k,v in result.items() if k!="issues"},ensure_ascii=False))
    else: print(rendered)
    raise SystemExit(1 if result["errors"] else 0)
if __name__=="__main__": main()
