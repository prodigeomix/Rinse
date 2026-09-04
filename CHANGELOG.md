# Changelog

All notable changes to **Rinse** are documented in this file.
The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [2.8.0] - 2026-09-04

### 🛡️ Critical Fixes & Bug Patches
* **Fixed Nil Spell Slot Crash in `Rinse_Cleanse`**: Guarded against nil `spellName` and `spellSlot` lookups, preventing fatal Lua error `Bad argument #1 to 'GetSpellCooldown' (number expected, got nil)` when dispels are unavailable or unlearned.
* **Real Spell Cooldown Protection**: Differentiated between standard 1.5s Global Cooldown (GCD) and long-cooldown dispels (*Hand of Freedom* [20s], Warlock Felhunter *Devour Magic* [8s]). Spells on actual cooldown are now immediately bypassed without interrupting active healer casts via `SpellStopCasting()`.
* **Fixed Player Pet Unit ID Corruption**: Resolved regex bug in `UpdatePrio` that generated invalid `"playerpet"` unit IDs instead of `"pet"`. The player's own pet is now properly scanned and cleansed in party/raid environments.
* **SuperWoW Vector Arithmetic Protection**: Safely guarded `UnitPosition("player")` and `UnitPosition(unit)` against nil returns during zoning or out-of-world transitions, preventing `attempt to perform arithmetic on local 'myX' (a nil value)`. Added instant self-cast fast path `UnitIsUnit("player", unit)`.

### ⚡ Performance & Resource Optimizations
* **Empty Aura Slot Optimization**: In `GetDebuffInfo`, `UnitDebuff(unit, i)` is now checked before manipulating `RinseScanTooltip`, eliminating hundreds of unnecessary tooltip queries and texture lookups per second across 40 raid members. Added `RinseScanTooltip:ClearLines()` to eliminate stale tooltip text retention.
* **Bounded Aura Scan Loops**: Clamped aura scanning loops (`i <= 16` for party/raid, `i <= 24` for target). Clamped `HasAbolish` loop from unbounded `repeat-until` to strict 32-slot iteration.
* **FrameXML Anchor Stacking Prevention**: Added explicit `:ClearAllPoints()` calls prior to `:SetPoint()` in `UpdateDirection()` and `UpdateHeader()`.

### 🔒 Reliability & State Management
* **Combat Drop State Reset**: Registered and handled `PLAYER_REGEN_ENABLED` to cleanly reset `autoattack`, `errorCooldown`, `stopCastCooldown`, `lastSpellName`, and `lastButton`.
* **SavedVariables Sanitization**: Added strict bounds checking for `SCALE` (0.5–2.0), `OPACITY` (0.1–1.0), `BUTTONS` (1–20), `POSITION`, and verified all 9 player class keys in `FILTER_CLASS`.
* **Safe Optional Extension Guarding**: Added robust `type(fn) == "function"` guards for all SuperWoW, Nampower, UnitXP SP3, and MikSBT optional APIs.

### 🧪 Engineering Infrastructure & Tooling
* **Automated Verification Suite in `tools/`**: Added `validate_lua50.py`, `check_lua.py`, `scan_global_leaks.py`, `test_rinse.py`, and `run_tests.py`.
* **GitHub Actions CI**: Added continuous integration matrix testing across Python 3.10, 3.11, and 3.12.
* **Repository Governance**: Added standardized issue templates, PR template, CONTRIBUTING guide, and security policy.

---

## [2.7.0]

- Baseline fork integrating audited raid dispel profile for Turtle WoW / Vanilla raids.
- Automated priority sorting for wipe mechanics (*Twisted Reflection*, *Impending Doom*, *Brood Afflictions*, *Decrepit Fever*).
- Blacklist protection against raid-wiping dispels (*Mutating Injection*, *Sanctum Mind Decay*, *Wyvern Sting*).
- Class-specific filters preserving healer mana on non-mana classes.
