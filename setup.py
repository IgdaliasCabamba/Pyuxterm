import sys
import os
from cx_Freeze import setup, Executable

build_exe_options = {
    "packages": [
        
        "src.uterm",
        "src.urequirements",
        "src.static_files",
        "_system",
        "server",
        "main",

        "aiohttp",
        "aiohttp_jinja2",
        "aiosignal",
        "altgraph",
        "async_timeout",
        "attrs",
        "bidict",
        "certifi",
        "charset_normalizer",
        "click",
        "engineio",
        "frozenlist",
        "hjson",
        "idna",
        "importlib_metadata",
        "multidict",
        "socketio",
        "requests",
        "rich",
        "urllib3",
        "yarl",
        "zipp",
        
        "engineio.async_drivers.aiohttp",
        "engineio.async_aiohttp"
    ],
    "excludes": ["static","templates"]}

base = None

setup(
    name="pyuterm",
    version="0.1",
    description="Pyuxterm - A powerful cross platform Terminal emulator",
    options={"build_exe": build_exe_options},
    executables=[Executable("app/__main__.py", base=base)],
)