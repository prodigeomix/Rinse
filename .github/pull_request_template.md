## Description

Please provide a summary of the changes, problem addressed, and mechanics touched:

- **Type of Change**: Bug fix / Performance optimization / Refactoring / Documentation
- **Encounters / Mechanics Affected**:

---

## 🛡️ Mandatory Lua 5.0 & Architecture QA Checklist

- [ ] **Strict Lua 5.0 Compliance**:
  - [ ] No `#` length operator (used `table.getn(tbl)` or `string.len(str)`).
  - [ ] No `%` modulo operator (used `math.mod(a, b)` or `mod(a, b)`).
  - [ ] No `//` integer division (used `math.floor(a / b)`).
  - [ ] No `goto` or `::label::` statements.
  - [ ] No `string.match` or `string.gmatch` (used `string.find` or `string.gfind`).
  - [ ] No `select()`, `table.pack`, `table.unpack`, or `math.huge`.
- [ ] **Zero Dynamic Table Allocation**: The 10 Hz scan loop (`RinseFrame_OnUpdate`) allocates 0 new tables per tick.
- [ ] **Backward Compatibility**: User `RINSE_CONFIG` and `RINSE_CHAR_CONFIG` SavedVariables are safely sanitized without data loss.
- [ ] **Safe API Guarding**: Optional extension APIs (`SuperWoW`, `UnitXP`, `Nampower`, `MikSBT`) are guarded with `type(fn) == "function"` or nil checks.

---

## 🧪 Verification Suite Execution

- [ ] Ran automated test suite locally with zero failures:
  ```bash
  python tools/run_tests.py
  ```
