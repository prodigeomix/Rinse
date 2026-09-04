# Rinse Addon
This addon is very similar to Decursive, it helps with removing debuffs from friendly units. Rinse is optimized for memory usage and also utilizes [SuperWoW](https://github.com/balakethelock/SuperWoW), [nampower](https://github.com/pepopo978/nampower) and [UnitXP_SP3](https://github.com/allfoxwy/UnitXP_SP3) functions if you have these mods installed.<br>
You can use `/rinse` or `/run Rinse()` in a macro or make a key binding to cleanse without clicking inside GUI.

Other commands:<br>
`/rinse options` - open the options GUI to change settings<br>
`/rinse skip` - open the skip list GUI to add or remove units from the skip list<br>
`/rinse prio` - open the priority list GUI to add or remove units from the priority list<br>

![Rinse](https://github.com/user-attachments/assets/8ede3d8b-7dda-4ccb-96f4-2b69bbb13b05)

---

## About This Fork & Raid Dispel Profile

This repository is a maintained fork of [Otari98/Rinse](https://github.com/Otari98/Rinse) by **Otari98** (with CPU/memory performance refactoring by **MarcelineVQ**).

This fork integrates an audited, high-performance raid dispel profile tailored for Vanilla and Turtle WoW raid encounters:
* **Foolproof Raid Safety (Hard Blacklists):** Prevents automated raid-wiping dispels (*Mutating Injection*, *Sanctum Mind Decay*, *Wyvern Sting*).
* **Encounter Filter vs. Blacklist Optimization:** Filters low-impact debuffs (*Thunderclap* on Lord Kazzak, *Magma Shackles* on Garr, *Thunderfury*) without suppressing critical same-type debuffs.
* **Emergency Priority Sorting:** Automatically bumps wipe-inducing debuffs (*Twisted Reflection*, *Impending Doom*, *Brood Afflictions*, *Decrepit Fever*) to the absolute front of the dispel queue.
* **Mana Preservation (Class Filters):** Automatically suppresses mana burns and silences on non-mana melee classes (Warriors and Rogues), saving thousands of healer mana per encounter.

Detailed mechanical justifications, trade-off analyses, and test verifications are documented in [DISPEL_PROFILE_AUDIT.md](DISPEL_PROFILE_AUDIT.md).

---

## Attribution & License

* **Original Author:** [Otari98](https://github.com/Otari98) (Spit)
* **Performance Enhancements:** [MarcelineVQ](https://github.com/MarcelineVQ)
* **Raid Dispel Profile & Maintenance:** [prodigeomix](https://github.com/prodigeomix)
* **License:** Licensed under the [MIT License](LICENSE) (Copyright (c) 2025 Spit).

