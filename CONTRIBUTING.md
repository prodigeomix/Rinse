# Contributing to Rinse

Thank you for contributing to **Rinse**! This project is maintained to the highest open-source engineering standards for World of Warcraft Vanilla (1.12.1 Client) and Turtle WoW (Patch 1.18.1).

---

## ⚠️ Mandatory Engineering Constraints

All code contributions must strictly adhere to the constraints enforced by the Vanilla 1.12.1 game client and the Turtle WoW environment:

### 1. Strict Lua 5.0 Syntax & Runtime Rules
The WoW 1.12.1 client uses **Lua 5.0**. Any Lua 5.1+ syntax or modern standard library functions will crash the game client on load:
* **Length Operator `#`**: **BANNED**. Use `table.getn(tbl)` or `string.len(str)`.
* **Modulo Operator `%`**: **BANNED**. Use `math.mod(a, b)` or `mod(a, b)`.
* **Integer Division `//`**: **BANNED**. Use `math.floor(a / b)`.
* **String Matching**: `string.match` and `string.gmatch` are **BANNED**. Use `string.find` with capture groups or `string.gfind`.
* **Functions & Expressions**: `select()`, `table.pack`, `table.unpack`, `math.huge`, and `...` vararg expressions are **BANNED**. Use `unpack()`, `1/0`, or index into the implicit `arg` table.
* **Control Flow**: `goto` and `::label::` are **BANNED**.

### 2. Zero-Allocation Hot Path (10 Hz Scan Loop)
* `RinseFrame_OnUpdate` executes every 0.1 seconds (10 Hz).
* **NEVER** allocate dynamic tables (`{}`), invoke closures, or format strings in the scan path.
* Pre-allocate reusable scratch tables and recycle them with `wipe()` or field resets.

### 3. Dispel Logic & Cooldown Correctness
* Always verify spell availability before querying cooldowns (`UsableSpells`, `UsableSpellBookIDs`).
* Differentiate between global cooldown (GCD = 1.5s) and actual spell cooldowns (e.g. *Hand of Freedom* [20s], *Devour Magic* [8s]). Spells on real cooldowns must not trigger `SpellStopCasting()`.

### 4. FrameXML Anchor Safety
* Always call `:ClearAllPoints()` before invoking `:SetPoint()` on existing UI elements to prevent anchor stacking and frame drift.

---

## 🧪 Local Testing & Verification Workflow

Before submitting a Pull Request, you MUST run the automated test suite locally:

```bash
python tools/run_tests.py
```

### Gate Checks Overview
1. `check_lua.py` — Verifies block balance and syntax integrity across all Lua files.
2. `validate_lua50.py` — Scans for banned post-Lua 5.0 operators and modern APIs.
3. `scan_global_leaks.py` — Detects any undeclared variable assignments escaping into `_G`.
4. `test_rinse.py` — Comprehensive unit test suite covering dispel profiles, pet mapping, cooldown math, and SavedVariables sanitization.

---

## 📦 Pull Request Process

1. Create a descriptive feature/fix branch (`git checkout -b fix/cooldown-check`).
2. Implement your changes following all Lua 5.0 and zero-allocation rules.
3. Verify that `python tools/run_tests.py` reports `ALL 4 CHECKS PASSED`.
4. Open a Pull Request referencing any related issues and complete the PR checklist.
