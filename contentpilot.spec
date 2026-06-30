# -*- mode: python ; coding: utf-8 -*-
"""PyInstaller spec for ContentPilot Desktop.

Usage:
    pyinstaller contentpilot.spec

This produces a single-file executable in dist/.
"""

import os
from pathlib import Path

block_cipher = None
root = Path(SPECPATH)

# ── Data files to bundle ──────────────────────────────────────────────
datas = [
    # Python package (pipeline core)
    (str(root / "src" / "contentpilot"), "src/contentpilot"),
    # Web UI templates + static
    (str(root / "web" / "templates"), "web/templates"),
    (str(root / "web" / "static"), "web/static"),
    # Article templates
    (str(root / "templates"), "templates"),
    # Workspace defaults (config template, voice guide)
    (str(root / "workspace" / "config.template.yaml"), "workspace"),
    (str(root / "workspace" / "voice.md"), "workspace"),
    # Reference files
    (str(root / "workspace" / "reference"), "workspace/reference"),
]

# ── Hidden imports (modules PyInstaller can't auto-detect) ───────────
hiddenimports = [
    # Core
    "contentpilot",
    "contentpilot.interface.cli",
    "contentpilot.application.service",
    "contentpilot.application.ports",
    "contentpilot.application.results",
    # Domain
    "contentpilot.domain.stages",
    "contentpilot.domain.gates",
    "contentpilot.domain.article",
    "contentpilot.domain.images",
    "contentpilot.domain.link_validator",
    # Infrastructure
    "contentpilot.infrastructure.config",
    "contentpilot.infrastructure.journal",
    "contentpilot.infrastructure.draft_store",
    "contentpilot.infrastructure.idea_bank",
    "contentpilot.infrastructure.publisher",
    "contentpilot.infrastructure.notifier",
    "contentpilot.infrastructure.image_host",
    "contentpilot.infrastructure.clock",
    "contentpilot.infrastructure.html",
    "contentpilot.infrastructure.paths",
    "contentpilot.infrastructure.throttle",
    "contentpilot.infrastructure.watchdog",
    "contentpilot.infrastructure.reconciler",
    "contentpilot.infrastructure.job_workspace",
    # Extras
    "contentpilot.license",
    "contentpilot.seo",
    "contentpilot.blogger",
    # API module
    "contentpilot.api",
    "contentpilot.api.client",
    "contentpilot.api.exceptions",
    # Flask/Jinja2
    "jinja2",
    "markupsafe",
    # PyWebView
    "webview",
]

a = Analysis(
    [str(root / "web" / "desktop.py")],
    pathex=[str(root / "src")],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        # Tkinter (not needed for webview)
        "tkinter", "_tkinter",
        # Matplotlib, numpy, pandas (not used)
        "matplotlib", "numpy", "pandas",
        # Testing
        "pytest", "_pytest",
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name="ContentPilot",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # No console window
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # Add icon path here when available: str(root / "assets" / "icon.ico")
)
