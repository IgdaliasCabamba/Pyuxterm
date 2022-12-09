import sys
sys.dont_write_bytecode = True
import os

if getattr(sys, "frozen", False):
    if hasattr(sys, "_MEIPASS"):
        ROOT_PATH = sys._MEIPASS
    else:
        ROOT_PATH = os.path.dirname(os.path.realpath(sys.executable))
    os.environ["UTERM_ROOT_PATH"] = ROOT_PATH
else:
    ROOT_PATH = os.path.dirname(os.path.realpath(__file__))
    os.environ["UTERM_ROOT_PATH"] = ROOT_PATH

SRC_PATH = os.path.join(ROOT_PATH, "src")
STATIC_PATH = os.path.join(ROOT_PATH, "static")
TEMPLATES_PATH = os.path.join(ROOT_PATH, "templates")

os.environ["UTERM_SRC_PATH"] = SRC_PATH
os.environ["UTERM_STATIC_PATH"] = STATIC_PATH
os.environ["UTERM_TEMPLATES_PATH"] = TEMPLATES_PATH

#sys.path.append(os.path.join(ROOT_PATH))
#sys.path.append(os.path.join(SRC_PATH))