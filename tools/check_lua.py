#!/usr/bin/env python3
"""
Block Balance and Syntax Integrity Checker for Rinse Lua files.
Verifies balance of function, if, do, repeat, end, until blocks.
"""

import re
import sys
import os

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

def check_blocks(filepath):
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    # Strip block comments
    content = re.sub(r'--\[\[.*?\]\]', '', content, flags=re.DOTALL)
    # Strip line comments
    content = re.sub(r'--.*', '', content)
    # Strip strings
    content = re.sub(r'"[^"\\]*(?:\\.[^"\\]*)*"', '""', content)
    content = re.sub(r"'[^'\\]*(?:\\.[^'\\]*)*'", "''", content)

    stack = []
    lines = content.split('\n')

    for line_idx, line in enumerate(lines, start=1):
        tokens = re.findall(r'\b(function|if|do|repeat|end|until)\b', line)
        for token in tokens:
            if token in ['function', 'if', 'do']:
                stack.append((token, line_idx))
            elif token == 'repeat':
                stack.append((token, line_idx))
            elif token == 'end':
                if not stack:
                    print(f"  ❌ Unmatched 'end' at line {line_idx}")
                    return False
                top_token, top_line = stack.pop()
                if top_token not in ['function', 'if', 'do']:
                    print(f"  ❌ Mismatched 'end' at line {line_idx} for '{top_token}' opened at line {top_line}")
                    return False
            elif token == 'until':
                if not stack:
                    print(f"  ❌ Unmatched 'until' at line {line_idx}")
                    return False
                top_token, top_line = stack.pop()
                if top_token != 'repeat':
                    print(f"  ❌ Mismatched 'until' at line {line_idx} for '{top_token}' opened at line {top_line}")
                    return False

    if stack:
        print(f"  ❌ Unclosed blocks remaining: {stack}")
        return False

    print(f"  ✅ {os.path.basename(filepath)}: balanced ({len(lines)} lines)")
    return True

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    addon_dir = os.path.abspath(os.path.join(script_dir, ".."))

    files_to_check = []
    if len(sys.argv) > 1:
        files_to_check = [sys.argv[1]]
    else:
        for f in ["Rinse.lua", "Localization.lua"]:
            p = os.path.join(addon_dir, f)
            if os.path.exists(p):
                files_to_check.append(p)

    all_ok = True
    print("Checking Lua block balance...")
    for f in files_to_check:
        if not check_blocks(f):
            all_ok = False

    sys.exit(0 if all_ok else 1)
