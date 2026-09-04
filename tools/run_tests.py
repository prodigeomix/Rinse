#!/usr/bin/env python3
"""
Rinse Addon Unified Test & Verification Suite Runner.
Executes all static analysis, syntax validation, global leak detection, and behavioral unit tests.
Returns exit code 0 if all checks pass, 1 if any check fails.
"""

import os
import subprocess
import sys
import time

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ADDON_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, ".."))

CHECKS = [
    ("Lua Syntax Block Balance (check_lua.py)", [sys.executable, os.path.join(SCRIPT_DIR, "check_lua.py")]),
    ("Lua 5.0 & WoW 1.12 Compliance (validate_lua50.py)", [sys.executable, os.path.join(SCRIPT_DIR, "validate_lua50.py"), ADDON_ROOT]),
    ("Global Variable Scope Leak Scan (scan_global_leaks.py)", [sys.executable, os.path.join(SCRIPT_DIR, "scan_global_leaks.py")]),
    ("Dispel Profiles & Logic Unit Tests (test_rinse.py)", [sys.executable, os.path.join(SCRIPT_DIR, "test_rinse.py"), "-v"]),
]

def main():
    print("=" * 80)
    print("RINSE AUTOMATED VERIFICATION SUITE")
    print("Patch 1.18.1 / Vanilla 1.12.1 Client Compatibility")
    print("=" * 80)

    total_start = time.time()
    all_passed = True
    results = []

    for name, cmd in CHECKS:
        print(f"\n>>> Running {name}...")
        start_t = time.time()
        res = subprocess.run(cmd, cwd=ADDON_ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace", check=False)
        duration = time.time() - start_t

        output = (res.stdout or "") + (res.stderr or "")
        lines = [l for l in output.strip().splitlines() if l.strip()]
        for l in lines[-8:]:
            print(f"    {l}")

        passed = (res.returncode == 0) and ("FAILED" not in output) and ("❌" not in output)
        if not passed:
            all_passed = False
            results.append((name, "FAIL", duration))
            print(f"    --> [FAIL] Exit code: {res.returncode}")
        else:
            results.append((name, "PASS", duration))
            print(f"    --> [PASS] ({duration:.2f}s)")

    print("\n" + "=" * 80)
    print("SUITE EXECUTION SUMMARY")
    print("=" * 80)
    for name, status, duration in results:
        indicator = "[PASS]" if status == "PASS" else "[FAIL]"
        print(f"  {indicator:<8} {name:<54} ({duration:.2f}s)")

    total_time = time.time() - total_start
    print("-" * 80)
    if all_passed:
        print(f"OVERALL RESULT: ALL {len(CHECKS)} CHECKS PASSED (Total time: {total_time:.2f}s)")
        print("=" * 80)
        sys.exit(0)
    else:
        print(f"OVERALL RESULT: VERIFICATION FAILED (Total time: {total_time:.2f}s)")
        print("=" * 80)
        sys.exit(1)

if __name__ == "__main__":
    main()
