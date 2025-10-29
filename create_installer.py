# Script Runner Pro - Windows Installer
"""
Create a Windows installer for Script Runner Pro using cx_Freeze
"""

import sys
import os
from cx_Freeze import setup, Executable

# Dependencies to include
build_exe_options = {
    "packages": ["PyQt5", "json", "subprocess", "platform", "pathlib"],
    "excludes": ["tkinter", "unittest", "pydoc", "doctest"],
    "include_files": [
        ("scripts.json", "scripts.json"),
    ],
    "optimize": 2,
}

# Base for Windows GUI application
base = None
if sys.platform == "win32":
    base = "Win32GUI"

# Executable configuration
executables = [
    Executable(
        "script-runner-gui.py",
        base=base,
        target_name="ScriptRunnerPro.exe",
    )
]

setup(
    name="Script Runner Pro",
    version="2.0.0",
    description="A modern script management and execution tool for Windows",
    options={"build_exe": build_exe_options},
    executables=executables,
)
