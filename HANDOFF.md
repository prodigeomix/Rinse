# Rinse — Project Status & Handoff Document

> **Last Updated:** 2026-09-06 09:05 (Antigravity Assistant)  
> **Status:** Production Ready  
> **Target Engine:** Turtle WoW 1.18.1 / Vanilla 1.12.1 Client  
> **Active Verification:** `python tools/run_tests.py` → **100% PASS**

---

## 1. Current Architecture
* **Purpose**: Dedicated, high-speed dispel, decurse, and cure engine completely decoupled from healing addons (`HolyPriest`).
* **Core Components**:
  - `Rinse.lua`: Core scanning loop, unit debuff analysis, range checking, priority matrix, mouseover cast binding.
  - `Rinse.xml` / `Templates.xml`: Visual alert frames and click-casting UI overlays.
  - `Localization.lua`: Multi-language debuff names, dispel types (Magic, Curse, Disease, Poison).
* **Decoupled Architecture**:
  - Handles `Dispel Magic` (Rank 1 & 2), `Cure Disease`, and `Abolish Disease`.
  - Ensures `HolyPriest` remains a pure throughput/reaction healing addon with zero dispel interference.
* **Test Suite (`tools/run_tests.py`)**:
  - Validates Lua 5.0 compliance, block balance, global leak scans, and `SavedVariables` sanitization under out-of-bounds inputs.

---

## 2. Invariant Rules (DO NOT TOUCH)
1. **Strict Separation of Concerns**: Never import or integrate Rinse dispel heuristics back into `HolyPriest`. Rinse runs as its own standalone subsystem.
2. **Rank Optimization**: Ensure Dispel Magic Rank 1 is used for low-mana or non-critical debuffs where mana efficiency is paramount, while Rank 2 is reserved for critical high-priority raid debuffs.
3. **Sound & Visual Throttling**: Alert frames and audio chimes must be throttled to prevent spam during high-debuff raid encounters (e.g. Lucifron, Shazzrah, Chromaggus).

---

## 3. Active Backlog & Next Steps
- [x] All test suites passing (`tools/run_tests.py`).
- [x] Git working tree is clean on branch `master`.
- [ ] Maintain code freeze; do not modify priority lists without in-game encounter logs.
