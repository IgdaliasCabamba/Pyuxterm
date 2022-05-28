import sys
import os
from cx_Freeze import setup, Executable

build_exe_options = {
    "packages": [
        
        "src.uterm",
        "src.urequirements",
        "src.static_files",
        "pyuterm",

        "aiohttp",
        "aiosignal",
        "altgraph",
        "async_timeout",
        "attrs",
        "bidict",
        "certifi",
        "charset_normalizer",
        "engineio",
        "frozenlist",
        "idna",
        "importlib_metadata",
        "multidict",
        "socketio",
        "requests",
        "urllib3",
        "yarl",
        "zipp"
    ],
    "excludes": ["static","templates"]}

base = None

setup(
    name="pyuterm",
    version="0.1",
    description="Test",
    options={"build_exe": build_exe_options},
    executables=[Executable("pyuterm.py", base=base)],
)