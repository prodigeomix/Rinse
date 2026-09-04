# Rinse Addon

[![CI](https://github.com/prodigeomix/Rinse/actions/workflows/ci.yml/badge.svg)](https://github.com/prodigeomix/Rinse/actions/workflows/ci.yml)
[![Turtle WoW](https://img.shields.io/badge/Turtle_WoW-1.18.1-1f8b4c.svg)](https://turtle-wow.org)
[![Vanilla 1.12.1](https://img.shields.io/badge/Client-1.12.1-blue.svg)](https://github.com/prodigeomix/Rinse)
[![Lua 5.0 Strict](https://img.shields.io/badge/Lua-5.0_Strict-orange.svg)](https://www.lua.org/manual/5.0/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**Rinse** is a high-performance, memory-optimized decursive dispel addon for World of Warcraft **Vanilla (1.12.1 Client)** and **Turtle WoW (Patch 1.18.1)**. It automatically tracks, filters, prioritizes, and removes dispellable debuffs from party and raid members with a single keypress or click.

Rinse dynamically integrates with client extensions if installed:
* **[SuperWoW](https://github.com/balakethelock/SuperWoW)**: Fast directional spell casting (`CastSpellByName(spell, unit)`), 3D coordinate vector range calculations, and instant debuff spell ID lookups without tooltip queries.
* **[nampower](https://github.com/pepopo978/nampower)**: Spell queue pop event integration (`SPELL_QUEUE_EVENT`) and non-destructive cast state checking (`GetCurrentCastingInfo`).
* **[UnitXP_SP3](https://github.com/allfoxwy/UnitXP_SP3)**: True melee reach distance calculation (`distanceBetween`) and line-of-sight checks (`inSight`).
* **[MikSBT](https://www.curseforge.com/wow/addons/mik-scrolling-battle-text)**: Optional on-screen scrolling combat text announcements for cleansed allies.

---

## ⚡ Quick Start & Macro Usage

To cleanse without clicking inside the GUI, create a macro:

```lua
/rinse
```
or
```lua
/run Rinse()
```

Bind this macro to a convenient key. Pressing it will automatically prioritize and cleanse the top debuff in your raid or party.

### Slash Commands
* `/rinse` — Cleanse the top prioritized debuff.
* `/rinse options` — Open the Options configuration window.
* `/rinse skip` — Open the Skip List (ignore specific players/units).
* `/rinse prio` — Open the Priority List (cleanse specific players/tanks first).
* `/rinse versions` — Perform a version check across your raid or party.

---

![Rinse Interface](https://github.com/user-attachments/assets/8ede3d8b-7dda-4ccb-96f4-2b69bbb13b05)

---

## 🛡️ Raid Dispel Profile & Safety Mechanics

This fork integrates a battle-tested raid dispel profile tailored for Vanilla and Turtle WoW raid encounters:

1. **Foolproof Raid Safety (Hard Blacklists):**
   * Suppresses automated dispels of wipe-inducing debuffs (*Mutating Injection* on Grobbulus, *Sanctum Mind Decay* in Karazhan Crypts, *Wyvern Sting* in PvP/PvE, *Seed of Corruption*).
2. **Encounter Filter vs. Blacklist Optimization:**
   * Uses non-suppressive filters for low-threat debuffs (*Thunderclap* on Lord Kazzak, *Magma Shackles* on Garr, *Thunderfury*). Unlike a blacklist, filtering hides only that specific spell without blinding the addon to critical debuffs of the same school (e.g. Kazzak's *Twisted Reflection*).
3. **Emergency Priority Sorting:**
   * Automatically elevates catastrophic debuffs (*Twisted Reflection*, *Impending Doom*, *Brood Afflictions*, *Decrepit Fever*, *True Fulfillment*, *Plague*, *Enveloping Winds*, *Hex*) to the absolute front of the dispel queue raidwide.
4. **Mana Preservation (Class Filters):**
   * Automatically suppresses mana burns, silences, and mind decay on non-mana melee classes (Warriors and Rogues), conserving thousands of healer mana per encounter.

Detailed mechanical justifications and test verifications are documented in [DISPEL_PROFILE_AUDIT.md](DISPEL_PROFILE_AUDIT.md).

---

## Supported Dispel Classes & Abilities

| Class | Magic | Poison | Disease | Curse | Snare |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Paladin** | Cleanse | Cleanse, Purify | Cleanse, Purify | — | Hand of Freedom |
| **Priest** | Dispel Magic | — | Abolish Disease, Cure Disease | — | — |
| **Druid** | — | Abolish Poison, Cure Poison | — | Remove Curse | — |
| **Shaman** | — | Cure Poison | Cure Disease | — | — |
| **Mage** | — | — | — | Remove Lesser Curse | — |
| **Warlock** | Devour Magic *(Felhunter)* | — | — | — | — |

---

## 🧪 Automated Testing & Verification

Rinse includes an automated testing and static analysis suite in `tools/`:

```bash
# Run the entire test and verification suite:
python tools/run_tests.py
```

### Verification Gates:
* **`tools/check_lua.py`**: Verifies strict block and syntax balance (`function`, `if`, `do`, `repeat`, `end`, `until`).
* **`tools/validate_lua50.py`**: Validates 100% strict Lua 5.0 compliance (guarantees zero Lua 5.1+ operators like `#`, `%`, `//`, `goto`, `string.match`, `select()`).
* **`tools/scan_global_leaks.py`**: Scans for unintended global variable leaks escaping into `_G`.
* **`tools/test_rinse.py`**: Unit test suite covering dispel profile completeness, pet unit ID mapping, GCD/cooldown math, and SavedVariables sanitization.

---

## 🤝 Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for engineering constraints and test requirements before opening a pull request.

---

## 📜 Attribution & License

* **Original Author:** [Otari98](https://github.com/Otari98) (Spit)
* **Performance Enhancements:** [MarcelineVQ](https://github.com/MarcelineVQ)
* **Raid Dispel Profile & Maintenance:** [prodigeomix](https://github.com/prodigeomix)
* **License:** Licensed under the [MIT License](LICENSE) (Copyright (c) 2025 Spit).
