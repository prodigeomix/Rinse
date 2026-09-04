#!/usr/bin/env python3
"""
Global Scope Leak Detector for Rinse.
Verifies that no undeclared variables leak into the global Lua environment.
Accounts for table constructors and Lua 5.0 scope rules.
"""

import os
import re
import sys

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

WOW_AND_ADDON_GLOBALS = {
    # Lua 5.0 standard globals
    'print', 'type', 'tostring', 'tonumber', 'pairs', 'ipairs', 'next', 'unpack',
    'pcall', 'xpcall', 'assert', 'error', 'setmetatable', 'getmetatable', 'getfenv',
    'setfenv', 'string', 'table', 'math', 'io', 'os', 'coroutine', 'table.getn', 'getn',
    'tinsert', 'tremove', 'sort', 'wipe', 'format', 'gsub', 'strfind', 'strsub',
    'strlen', 'strlower', 'strupper', 'strrep', 'mod', 'min', 'max', 'floor', 'abs',

    # WoW API Globals
    'SlashCmdList', 'CreateFrame', 'UIParent', 'Minimap', 'GameTooltip', 'message',
    'this', 'arg1', 'arg2', 'arg3', 'arg4', 'arg5', 'arg6', 'arg7', 'arg8', 'arg9',
    'event', 'DEFAULT_CHAT_FRAME', 'ChatFrame1', 'UIErrorsFrame', 'PlaySoundFile',
    'UnitExists', 'UnitIsFriend', 'UnitIsVisible', 'UnitDebuff', 'UnitBuff', 'UnitClass',
    'UnitIsUnit', 'UnitIsPlayer', 'UnitIsCharmed', 'UnitName', 'UnitCanAssist',
    'UnitCanAttack', 'UnitIsConnected', 'UnitIsDead', 'UnitInRaid', 'UnitInParty',
    'CheckInteractDistance', 'GetTime', 'GetSpellCooldown', 'CastSpellByName',
    'TargetUnit', 'TargetLastTarget', 'AssistUnit', 'GetCVar', 'SetCVar',
    'GetPlayerBuff', 'GetPlayerBuffTexture', 'GetNumSpellTabs', 'GetSpellTabInfo',
    'GetSpellName', 'GetRaidRosterInfo', 'GetCursorPosition', 'MouseIsOver',
    'SendAddonMessage', 'StaticPopup_Show', 'StaticPopupDialogs', 'FauxScrollFrame_GetOffset',
    'FauxScrollFrame_Update', 'GetAddOnMetadata', 'UIDROPDOWNMENU_MENU_VALUE',
    'UIDROPDOWNMENU_MENU_LEVEL', 'BOOKTYPE_SPELL', 'BOOKTYPE_PET', 'UISpecialFrames',

    # Optional / SuperWoW / Nampower APIs
    'SUPERWOW_VERSION', 'UnitXP', 'UnitPosition', 'SpellInfo', 'GetSpellNameAndRankForId',
    'GetCurrentCastingInfo', 'GetNampowerVersion', 'MikSBT',

    # Rinse Specific Globals / SavedVariables / XML Frames
    'Rinse', 'RINSE_CONFIG', 'RINSE_CHAR_CONFIG', 'BINDING_HEADER_RINSE_HEADER',
    'BINDING_NAME_RINSE', 'BINDING_NAME_RINSE_TOGGLE_OPTIONS',
    'BINDING_NAME_RINSE_TOGGLE_PRIO', 'BINDING_NAME_RINSE_TOGGLE_SKIP',
    'RinseFrame', 'RinseDebuffsFrame', 'RinsePrioListFrame', 'RinseSkipListFrame',
    'RinseOptionsFrame', 'RinseFrameTitle', 'RinseFrameHitRect', 'RinseFrameBackground',
    'RinseScanTooltip', 'RinseScanTooltipTextLeft1', 'RinseScanTooltipTextRight1',
    'RinseOptionsFrameBlacklistScrollFrame', 'RinseOptionsFrameClassFilterScrollFrame',
    'RinseOptionsFrameFilterScrollFrame', 'RinseSkipListScrollFrame', 'RinsePrioListScrollFrame',
    'RinseMovingButton', 'RinseMovingButtonText', 'RinseFrameDebuff1',
    'RinseOptionsFrameScaleSlider', 'RinseOptionsFrameOpacitySlider',
    'RinseOptionsFrameIgnoreAbolish', 'RinseOptionsFrameShadowform', 'RinseOptionsFramePets',
    'RinseOptionsFramePrint', 'RinseOptionsFrameMSBT', 'RinseOptionsFrameSound',
    'RinseOptionsFrameLock', 'RinseOptionsFrameBackdrop', 'RinseOptionsFrameShowHeader',
    'RinseOptionsFrameFlip', 'RinseOptionsFrameButtonsSlider', 'RinseOptionsFrameWyvernSting',
    'RinseOptionsFrameMutatingInjection', 'RinseOptionsFrameFilterMagic',
    'RinseOptionsFrameFilterDisease', 'RinseOptionsFrameFilterPoison',
    'RinseOptionsFrameFilterSnare', 'RinseOptionsFrameFilterCurse',
    'RinseSkipListFrameTitle', 'RinseSkipListFrameClear', 'RinsePrioListFrameTitle',
    'RinsePrioListFrameClear', 'RinseOptionsFrameTitle', 'RinseOptionsFrameFilterText',
    'RinseOptionsFrameClassFilterText', 'RinseOptionsFrameHiddenDebuffsText',
    'RinseOptionsFrameAddToFilter', 'RinseOptionsFrameAddToBlacklist',
    'RinseOptionsFrameAddToClassFilter', 'RinseOptionsFrameSelectClassText',
    'RinseFrame_OnLoad', 'RinseFrame_OnEvent', 'RinseFrame_OnUpdate',
    'RinseOptionsFrame_OnLoad', 'Rinse_Cleanse', 'Rinse_ToggleDirection',
    'Rinse_ToggleHeader', 'RinseListButton_OnClick', 'RinseListButton_OnDragStart',
    'RinseListButton_OnDragStop', 'RinseMovingButton_OnUpdate', 'Rinse_AddUnitToList',
    'RinseSkipListScrollFrame_Update', 'RinsePrioListScrollFrame_Update',
    'RinseOptionsFrameBlacklistScrollFrame_Update', 'RinseOptionsFrameClassFilterScrollFrame_Update',
    'RinseOptionsFrameFilterScrollFrame_Update', 'RinseOptionsFrameAddToBlacklist_OnClick',
    'RinseOptionsFrameResetBlacklist_OnClick', 'RinseOptionsFrameAddToFilter_OnClick',
    'RinseOptionsFrameResetFilter_OnClick', 'RinseOptionsFrameAddToClassFilter_OnClick',
    'RinseOptionsFrameResetClassFilter_OnClick', 'RinseOptionsFrameButtonsSlider_OnValueChanged',
    'RinseFrameOptions_OnClick', 'RinseFrameSkipList_OnClick', 'RinseFramePrioList_OnClick',
    'Rinse_StartVersionsCheck', 'Rinse_OutputVersionsCheckResults'
}

def scan_file(filepath):
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    # Find all local declarations, supporting multiple comma-separated variables: local a, b, c = ...
    local_vars = set()
    local_decls = re.findall(r'\blocal\s+(?:function\s+)?([^=\n;]+)', content)
    for decl in local_decls:
        for var in decl.split(','):
            var = var.strip()
            if re.match(r'^[A-Za-z_][A-Za-z0-9_]*$', var):
                local_vars.add(var)

    # Function parameters
    params = re.findall(r'function\s*[A-Za-z0-9_:\.]*\s*\((.*?)\)', content)
    for p_list in params:
        for p in p_list.split(','):
            p = p.strip()
            if p:
                local_vars.add(p)

    # For loop variables
    for_loops = re.findall(r'\bfor\s+([A-Za-z0-9_,\s]+)\s+(?:in|=)', content)
    for loop_vars in for_loops:
        for v in loop_vars.split(','):
            v = v.strip()
            if v:
                local_vars.add(v)

    leaks = []
    lines = content.split('\n')
    brace_depth = 0

    for line_idx, line in enumerate(lines, start=1):
        # Strip comments
        code_part = line.split('--')[0]
        # Strip strings to count braces accurately
        stripped_line = re.sub(r'"[^"\\]*(?:\\.[^"\\]*)*"', '""', code_part)
        stripped_line = re.sub(r"'[^'\\]*(?:\\.[^'\\]*)*'", "''", stripped_line)

        # Check for assignment only when outside of table constructors
        # Inside table constructors (brace_depth > 0), key = val is field assignment
        match = re.search(r'^\s*([A-Za-z_][A-Za-z0-9_]*)\s*=(?!=)', code_part)
        if match and brace_depth == 0:
            var = match.group(1)
            if (var not in WOW_AND_ADDON_GLOBALS and
                not var.startswith('SLASH_') and
                not var.startswith('BINDING_') and
                var not in local_vars):
                leaks.append((line_idx, var, line.strip()))

        # Update brace depth for subsequent lines
        brace_depth += stripped_line.count('{') - stripped_line.count('}')
        if brace_depth < 0:
            brace_depth = 0

    return leaks

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    addon_dir = os.path.abspath(os.path.join(script_dir, ".."))

    files_to_check = ["Rinse.lua", "Localization.lua"]
    all_leaks = []

    print("Scanning for global variable leaks...")
    for f in files_to_check:
        path = os.path.join(addon_dir, f)
        if os.path.exists(path):
            leaks = scan_file(path)
            if leaks:
                for line_idx, var, stmt in leaks:
                    print(f"  ❌ {f}:{line_idx}: Undefined global '{var}' -> {stmt}")
                    all_leaks.append((f, line_idx, var))
            else:
                print(f"  ✅ {f}: 0 global leaks detected")

    if all_leaks:
        print(f"\nTotal global leaks detected: {len(all_leaks)}")
        sys.exit(1)
    else:
        print("\nAll files free of unintended global leaks!")
        sys.exit(0)

if __name__ == "__main__":
    main()
