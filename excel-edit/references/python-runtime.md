# Configured Python runtime

Use `scripts/excel-python.cmd` for every Python invocation in this skill, including existing helper scripts. The launcher contains one configured interpreter path, under the current Windows USERPROFILE by default. It selects the Codex bundled Python; verify its imports on each machine before first native use. Update that single path if workspace dependency discovery reports another location. Do not use bare `python`, `py`, or `pip`, or the Python bundled with Inkscape.

## Invocation

PowerShell (agent shell):

```powershell
& (Join-Path $env:USERPROFILE '.codex\skills\excel-edit\scripts\excel-python.cmd') -B -c "import sys, openpyxl; print(sys.executable); print(openpyxl.__version__)"
& (Join-Path $env:USERPROFILE '.codex\skills\excel-edit\scripts\excel-python.cmd') -m pip --version
```

CMD (the user's current shell):

```cmd
"%USERPROFILE%\.codex\skills\excel-edit\scripts\excel-python.cmd" -B -c "import sys, openpyxl; print(sys.executable); print(openpyxl.__version__)"
```

Run a task script by passing its quoted path and arguments to the same launcher. The launcher preserves Python's exit code. Examples elsewhere in this skill beginning with `python` must use this launcher instead.

## Packages and maintenance

- Inspect packages through this launcher with `-m pip show openpyxl pywin32 xlwings`. Install requested dependencies through the same launcher with `-m pip install PACKAGE`, subject to task authorization and filesystem/network permissions. A package installation is not part of a routine environment check.
- After installing a dependency, import its actual module through this launcher and check `sys.executable` and the module's `__file__`. Package names can differ from import names: pywin32 supplies `win32com.client` and `pythoncom`.
- Do not use `--user`, `--target`, another environment, or a different pip as a workaround for an installation failure; diagnose the selected environment first.
- This is an application-managed runtime, not a permanently provisioned independent Python installation. Codex updates can change the interpreter or packages. Do not claim that added packages are guaranteed to survive updates.
- If the configured executable disappears or stops working, use `load_workspace_dependencies` to locate the current bundled Python, verify the needed imports, and update the single path in the launcher within the authorized scope. Do not silently switch to a Python found on PATH. If the runtime works but an import is missing, report the missing package in this environment rather than saying Python is absent.
- A later move to a dedicated Excel environment must update this same launcher and verify the required imports and pip location. Do not change the system PATH for this skill.
- Perform a quick interpreter/import check once per task when needed; do not repeat full environment discovery per workbook.
- Use `check_runtime.py --native` before generating native edit code. It imports openpyxl, pythoncom and win32com.client, prints interpreter/module locations and returns nonzero if imports fail; it does not launch Excel. A working executable path is not proof that its former packages remain installed. Repair missing packages using this launcher's `-m pip`, verify imports, then resume the same executor. Do not switch languages or alter PATH just to bypass a missing dependency. Package repair remains subject to actual authorization and permissions.
