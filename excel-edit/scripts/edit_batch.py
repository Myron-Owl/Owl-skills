"""Sequential multi-workbook edits with guarded recovery on caught failures, not atomic commit."""
import argparse
import json
import os
from pathlib import Path
import shutil
from edit_common import EditError, require, load_plan, digest, check_unlocked, stage_path, commit


def execute_batch(spec, runners=None):
    if runners is None:
        from edit_simple import execute as simple
        from edit_native import execute as native
        runners = {"simple": simple, "native": native}
    require(set(spec) == {"steps", "recovery_directory"}, "Batch needs steps and recovery_directory")
    require(isinstance(spec["steps"], list) and len(spec["steps"]) >= 2, "Use a single editor for one file")
    steps = []
    for step in spec["steps"]:
        require(set(step) == {"engine", "plan"} and step["engine"] in runners, "Invalid batch step")
        require(Path(step["plan"]).is_absolute(), "Plan paths must be absolute")
        steps.append((step["engine"], load_plan(step["plan"])))
    keys = [os.path.normcase(p["workbook"]) for _, p in steps]
    require(len(set(keys)) == len(keys), "Each target may appear only once")
    for i, (_, plan) in enumerate(steps):
        for dep in plan["dependencies"]:
            key = os.path.normcase(str(Path(dep).resolve()))
            require(key not in keys or keys.index(key) < i, "Order target workbooks upstream first; cycles need scoped handling")
    recovery = Path(spec["recovery_directory"])
    require(recovery.is_absolute() and not recovery.exists(), "Recovery directory must be a new absolute path")
    recovery.mkdir(parents=True)
    records = []
    journal = recovery / "journal.json"

    def record():
        temp = recovery / "journal.tmp"
        temp.write_text(json.dumps(records, ensure_ascii=True, indent=2), encoding="utf-8")
        os.replace(temp, journal)

    # Verify each backup against its source; executors still guard their own commits.
    for i, (_, plan) in enumerate(steps):
        path = Path(plan["workbook"])
        check_unlocked(path)
        before = digest(path)
        backup = recovery / f"{i:03d}-{path.name}"
        shutil.copy2(path, backup)
        require(digest(backup) == before == digest(path), f"Source changed while backing up: {path}")
        records.append(dict(workbook=str(path), backup=str(backup), before=before, state="prepared"))
    record()
    results = []
    try:
        for (engine, plan), row in zip(steps, records):
            require(digest(row["workbook"]) == row["before"], "Target changed since batch backup")
            row["state"] = "running"
            record()
            results.append(runners[engine](plan))
            row["after"] = results[-1]["committed_hash"]
            row["state"] = "committed"
            record()
            require(digest(row["workbook"]) == row["after"], "Target changed after commit")
    except Exception as error:
        for row in reversed(records):
            if row["state"] not in ("committed", "running"):
                continue
            temp = None
            try:
                current = digest(row["workbook"])
                if current == row["before"]:
                    row["state"] = "unchanged"
                    continue
                require(row.get("after") == current, "Concurrent or uncertain change; kept file and backup for manual recovery")
                require(digest(row["backup"]) == row["before"], "Backup changed; refused recovery")
                temp = stage_path(Path(row["workbook"]))
                shutil.copy2(row["backup"], temp)
                commit(temp, Path(row["workbook"]), current)
                row["state"] = "restored"
            except Exception as restore_error:
                row["state"] = "recovery_blocked"
                row["error"] = str(restore_error)
            finally:
                if temp is not None and temp.exists():
                    temp.unlink()
        record()
        raise EditError(str(error), stage="batch", recovery_directory=str(recovery), files=records,
                        cause=getattr(error, "context", {})) from error
    return {"status": "PASS_BATCH", "atomic": False, "results": results, "recovery_directory": str(recovery)}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("batch")
    args = parser.parse_args()
    try:
        print(json.dumps(execute_batch(json.loads(Path(args.batch).read_text(encoding="utf-8-sig"))), ensure_ascii=True))
    except Exception as error:
        print(json.dumps({"status": "FAILED", "error": str(error), **getattr(error, "context", {})}, ensure_ascii=True))
        raise SystemExit(1)
