"""Fast import check; does not start Excel, install packages or change configuration."""
import argparse
import importlib
import json
import sys
from time import perf_counter


def check(native=False):
    start = perf_counter()
    modules, missing = {}, []
    for name in ['openpyxl'] + (['pythoncom', 'win32com.client', 'lxml.etree'] if native else []):
        try:
            module = importlib.import_module(name)
            modules[name] = getattr(module, '__file__', None)
        except (ImportError, OSError) as error:
            missing.append({'module': name, 'error': str(error)})
    return dict(status='READY' if not missing else 'MISSING_DEPENDENCY',
                python=sys.executable, modules=modules, missing=missing,
                seconds=round(perf_counter()-start, 3))


def require_native():
    result = check(True)
    if result['missing']:
        from edit_common import EditError
        raise EditError('Native dependencies unavailable. Repair this interpreter before preparing or rewriting an editor.',
                        stage='runtime', original_written=False, runtime=result)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--native', action='store_true')
    result = check(parser.parse_args().native)
    print(json.dumps(result, ensure_ascii=True))
    raise SystemExit(bool(result['missing']))
