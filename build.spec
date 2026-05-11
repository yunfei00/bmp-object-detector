# -*- mode: python ; coding: utf-8 -*-
from __future__ import annotations

from pathlib import Path

from PyInstaller.utils.hooks import collect_dynamic_libs, collect_submodules

project_root = Path(__file__).resolve().parent
icon_file = project_root / "assets" / "icon.ico"
icon_path = str(icon_file) if icon_file.exists() else None

hiddenimports = (
    collect_submodules("PySide6")
    + collect_submodules("cv2")
    + collect_submodules("numpy")
)
binaries = collect_dynamic_libs("PySide6") + collect_dynamic_libs("cv2")

a = Analysis(
    ["scripts/run_gui.py"],
    pathex=[str(project_root)],
    binaries=binaries,
    datas=[],
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name="BMPObjectDetector",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=icon_path,
)
