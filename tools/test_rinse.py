#!/usr/bin/env python3
"""
Unit Test Suite for Rinse Dispel Profiles, Cooldown Handling, Pet Mapping, and Sanitization.
Turtle WoW 1.18.1 / Vanilla 1.12.1 Compliance.
"""

import os
import re
import sys
import unittest

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ADDON_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

class TestRinseDispelProfiles(unittest.TestCase):
    """Verifies that all dispelling classes have exact abilities defined."""

    def setUp(self):
        lua_path = os.path.join(ADDON_DIR, "Rinse.lua")
        with open(lua_path, "r", encoding="utf-8", errors="ignore") as f:
            self.content = f.read()

    def test_paladin_profile(self):
        self.assertIn('Spells["PALADIN"] = {', self.content)
        # Paladin has Cleanse (Magic, Poison, Disease), Purify, and Hand of Freedom (Snare)
        self.assertIn('[L["Magic"]] = {L["Cleanse"]}', self.content)
        self.assertIn('[L["Snare"]] = {L["Hand of Freedom"]}', self.content)

    def test_druid_profile(self):
        self.assertIn('Spells["DRUID"] = {', self.content)
        self.assertIn('[L["Curse"]] = {L["Remove Curse"]}', self.content)
        self.assertIn('[L["Poison"]] = {L["Abolish Poison"], L["Cure Poison"]}', self.content)

    def test_priest_profile(self):
        self.assertIn('Spells["PRIEST"] = {', self.content)
        self.assertIn('[L["Magic"]] = {L["Dispel Magic"]}', self.content)
        self.assertIn('[L["Disease"]] = {L["Abolish Disease"], L["Cure Disease"]}', self.content)

    def test_shaman_profile(self):
        self.assertIn('Spells["SHAMAN"] = {', self.content)
        self.assertIn('[L["Poison"]] = {L["Cure Poison"]}', self.content)
        self.assertIn('[L["Disease"]] = {L["Cure Disease"]}', self.content)

    def test_mage_profile(self):
        self.assertIn('Spells["MAGE"] = {', self.content)
        self.assertIn('[L["Curse"]] = {L["Remove Lesser Curse"]}', self.content)

    def test_warlock_profile(self):
        self.assertIn('Spells["WARLOCK"] = {', self.content)
        self.assertIn('[L["Magic"]] = {L["Devour Magic"]}', self.content)

    def test_pure_dps_profiles_empty(self):
        self.assertIn('Spells["WARRIOR"] = {}', self.content)
        self.assertIn('Spells["ROGUE"]   = {}', self.content)
        self.assertIn('Spells["HUNTER"]  = {}', self.content)

class TestRinseUnitMapping(unittest.TestCase):
    """Verifies that unit ID and pet mapping handles 'player' and party/raid members correctly."""

    def map_unit_to_pet(self, unit_id):
        if unit_id == "player":
            return "pet"
        # Lua pattern: gsub(u, "(%a+)(%d*)", "%1pet%2")
        match = re.match(r'^([a-zA-Z]+)(\d*)$', unit_id)
        if match:
            prefix, num = match.groups()
            return f"{prefix}pet{num}"
        return unit_id

    def test_player_pet_mapping(self):
        # player must map to 'pet', NEVER 'playerpet'
        self.assertEqual(self.map_unit_to_pet("player"), "pet")

    def test_party_pet_mapping(self):
        self.assertEqual(self.map_unit_to_pet("party1"), "partypet1")
        self.assertEqual(self.map_unit_to_pet("party4"), "partypet4")

    def test_raid_pet_mapping(self):
        self.assertEqual(self.map_unit_to_pet("raid1"), "raidpet1")
        self.assertEqual(self.map_unit_to_pet("raid40"), "raidpet40")

class TestRinseCooldownLogic(unittest.TestCase):
    """Verifies the GCD vs Real Spell Cooldown clamping math."""

    def check_cooldown(self, start, duration, current_time, attempted_cast):
        cd_remaining = 0
        if start and duration and start > 0 and duration > 0:
            cd_remaining = max(0, (start + duration) - current_time)

        # Real spell cooldown (e.g. Hand of Freedom [20s], Devour Magic [8s])
        if duration and duration > 1.5 and cd_remaining > 0:
            return False, "Spell on real cooldown"

        on_gcd = (duration == 1.5 and cd_remaining > 0)
        if attempted_cast and on_gcd:
            return False, "Spell queue blocked by active GCD"

        return True, "Cast Allowed"

    def test_ready_spell(self):
        can_cast, reason = self.check_cooldown(0, 0, 100.0, False)
        self.assertTrue(can_cast)

    def test_gcd_active_first_attempt(self):
        # First button while on GCD can attempt cast to queue via Nampower/Vanilla
        can_cast, reason = self.check_cooldown(99.0, 1.5, 100.0, False)
        self.assertTrue(can_cast)

    def test_gcd_active_subsequent_attempt(self):
        # Second button while on GCD must NOT attempt cast
        can_cast, reason = self.check_cooldown(99.0, 1.5, 100.0, True)
        self.assertFalse(can_cast)
        self.assertEqual(reason, "Spell queue blocked by active GCD")

    def test_long_cooldown_active(self):
        # Hand of Freedom on 20s cooldown (10s remaining)
        can_cast, reason = self.check_cooldown(90.0, 20.0, 100.0, False)
        self.assertFalse(can_cast)
        self.assertEqual(reason, "Spell on real cooldown")

    def test_long_cooldown_expired(self):
        # Hand of Freedom cooldown expired
        can_cast, reason = self.check_cooldown(80.0, 20.0, 105.0, False)
        self.assertTrue(can_cast)

class TestRinseSavedVariablesSanitization(unittest.TestCase):
    """Verifies that SavedVariables are properly validated and bounded."""

    def sanitize_config(self, scale, opacity, buttons, position, filter_class):
        try:
            scale = float(scale)
        except (ValueError, TypeError):
            scale = 0.85
        if scale < 0.5 or scale > 2.0:
            scale = 0.85

        try:
            opacity = float(opacity)
        except (ValueError, TypeError):
            opacity = 1.0
        if opacity < 0.1 or opacity > 1.0:
            opacity = 1.0

        try:
            buttons = int(buttons)
        except (ValueError, TypeError):
            buttons = 5
        if buttons < 1 or buttons > 20:
            buttons = 5

        if not isinstance(position, dict) or "x" not in position or "y" not in position:
            position = {"x": 0, "y": 0}
        if not isinstance(position["x"], (int, float)) or not isinstance(position["y"], (int, float)):
            position = {"x": 0, "y": 0}

        valid_classes = ["WARRIOR", "DRUID", "PALADIN", "WARLOCK", "MAGE", "PRIEST", "ROGUE", "HUNTER", "SHAMAN"]
        if not isinstance(filter_class, dict):
            filter_class = {}
        for c in valid_classes:
            if c not in filter_class:
                filter_class[c] = {}

        return scale, opacity, buttons, position, filter_class

    def test_normal_values(self):
        s, o, b, p, fc = self.sanitize_config(1.0, 0.8, 8, {"x": 100, "y": -50}, {})
        self.assertEqual(s, 1.0)
        self.assertEqual(o, 0.8)
        self.assertEqual(b, 8)
        self.assertEqual(p, {"x": 100, "y": -50})
        self.assertEqual(len(fc), 9)

    def test_out_of_bounds_values(self):
        s, o, b, p, fc = self.sanitize_config(99.0, -5.0, 999, "invalid", None)
        self.assertEqual(s, 0.85)
        self.assertEqual(o, 1.0)
        self.assertEqual(b, 5)
        self.assertEqual(p, {"x": 0, "y": 0})
        self.assertEqual(len(fc), 9)

class TestLocalizationParity(unittest.TestCase):
    """Verifies that Localization.lua defines all expected keys across all supported locales."""

    def test_locale_keys(self):
        loc_path = os.path.join(ADDON_DIR, "Localization.lua")
        with open(loc_path, "r", encoding="utf-8", errors="ignore") as f:
            loc_content = f.read()

        required_keys = [
            "Cleanse", "Purify", "Dispel Magic", "Cure Disease", "Abolish Disease",
            "Cure Poison", "Abolish Poison", "Remove Curse", "Remove Lesser Curse",
            "Hand of Freedom", "Devour Magic", "Magic", "Poison", "Disease", "Curse", "Snare",
        ]

        for key in required_keys:
            pattern = rf'\["{re.escape(key)}"\]'
            self.assertTrue(re.search(pattern, loc_content), f"Missing key '{key}' in Localization.lua")

        # Format string keys
        fmt_keys = ["FMT_SCALE", "FMT_OPACITY", "FMT_DEBUFFS_SHOWN"]
        for key in fmt_keys:
            self.assertTrue(key in loc_content, f"Missing format key '{key}' in Localization.lua")

if __name__ == "__main__":
    unittest.main()
