"""Read-only local concordance. Python 3.9+; standard library only."""
import argparse, json, sqlite3
from pathlib import Path

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("query",nargs="?",default="")
    p.add_argument("--db",type=Path)
    p.add_argument("--game")
    p.add_argument("--variant")
    p.add_argument("--exact",action="store_true")
    p.add_argument("--key")
    p.add_argument("--limit",type=int,default=10)
    args=p.parse_args()
    if not 1<=args.limit<=100: p.error("--limit must be 1..100")
    if not args.db:
        cfg=Path(__file__).resolve().parents[1]/"references"/"local-corpus.json"
        if not cfg.exists(): p.error("No local corpus configured; supply --db.")
        args.db=Path(json.loads(cfg.read_text(encoding="utf-8-sig"))["database"])
    if not args.db.is_file(): p.error("Corpus unavailable: "+str(args.db))
    db=sqlite3.connect(args.db.resolve().as_uri()+"?mode=ro",uri=True)
    db.row_factory=sqlite3.Row
    where=[]; values=[]
    for field,value in [("game",args.game),("variant",args.variant),("string_key",args.key)]:
        if value: where.append(field+" = ?"); values.append(value)
    if args.query:
        if args.exact:
            where.append("(en_plain = ? COLLATE NOCASE OR zh_plain = ?)")
            values.extend([args.query,args.query])
        else:
            escaped=args.query.replace("\\","\\\\").replace("%","\\%").replace("_","\\_")
            where.append("(en_plain LIKE ? ESCAPE '\\' OR zh_plain LIKE ? ESCAPE '\\')")
            values.extend(["%"+escaped+"%"]*2)
    if not where: p.error("Supply query, --key, --game or --variant.")
    query="SELECT game,variant,string_key AS key,en,zh,source,alignment FROM pairs WHERE "+" AND ".join(where)+" ORDER BY length(en_plain),game,variant,string_key LIMIT ?"
    rows=[dict(r) for r in db.execute(query,values+[args.limit])]
    print(json.dumps({"matches_returned":len(rows),"limit":args.limit,"results":rows},ensure_ascii=False,indent=2))
    db.close()

if __name__=="__main__": main()
