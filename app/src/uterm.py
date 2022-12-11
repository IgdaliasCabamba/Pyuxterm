import platform
import sys
import os
import subprocess
import glob
import pathlib
import hjson
from dataclasses import dataclass

class XTermSettings:
    
    @dataclass
    class Defaults:
        THEME = {"background": "#212121"}

    def __init__(self):
        self.__themes = self.read_themes()
    
    @property
    def themes(self) -> dict:
        return self.__themes
    
    def update_themes(self) -> None:
        self.__themes.clear()
        self.__themes = self.read_themes()

    def read_themes(self) -> dict:
        themes = dict()

        possible_themes = glob.glob(
            os.path.join("/",os.environ["UTERM_ROOT_PATH"],"settings","themes")+"/**.theme.json",
            recursive=True
        )
        for file in possible_themes:
            name = pathlib.Path(file).name
            name = name.split(".")[0].lower()
            with open(file, "r") as fp:
                themes[name] = hjson.load(fp)
        
        return themes

XTERM_SETTINGS = XTermSettings()

IS_UNIX = False

if platform.system().lower() in {"linux", "darwin"}:
    IS_UNIX = True

if IS_UNIX:
    import pty
    import select
    import termios
    import struct
    import fcntl
    import shlex

else:
    import winpty #pip install pywinpty    

class TermUtils:

    @staticmethod
    def get_split_command(command, command_args):
        if IS_UNIX:
            return [command] + shlex.split(command_args) 
        else:
            command += command_args
            return command


class TerminalCoreApi:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.child_pid = None
        self.fd = None
        
        self.process = None #Windows
    
    @property
    def communication(self):
        if IS_UNIX:
            return self.fd
        else:
            return self.process
    
    def spawn(self, cmd):
        if IS_UNIX:
            if self.child_pid is not None:
                return

            (child_pid, fd) = pty.fork()
        
            if child_pid == 0:
                subprocess.run(cmd)
        
            else:
                self.fd = fd
                self.child_pid = child_pid

                self.set_window_size(self.rows, self.cols)
        else:
            if self.process is None:
                self.process = winpty.PTY(self.cols, self.rows)
                self.process.spawn(cmd)
    
    def set_window_size(self, row, col, xpix=0, ypix=0):
        if IS_UNIX:
            if self.fd is not None:
                size = struct.pack("HHHH", row, col, xpix, ypix)
                fcntl.ioctl(self.fd, termios.TIOCSWINSZ, size)
        else:
            if self.process is not None:
                self.process.set_size(row, col)
    
    def read(self, max_read_bytes):
        if IS_UNIX:
            if self.fd is not None:
                try:
                    timeout_sec = 0
                    (data_ready, _, _) = select.select([self.fd], [], [], timeout_sec)
                    if data_ready:
                        return os.read(self.fd, max_read_bytes).decode()
                except Exception as e:
                    print(e)
                    return False
        else:
            if self.process is not None:
                return self.process.read()
    
    def write(self, data):
        if IS_UNIX:
            if self.fd is not None:
                os.write(self.fd, data)
        
        else:
            if self.process is not None:
                self.process.write(data)
    
    def is_alive(self):
        if IS_UNIX and self.fd is not None:

            return os.isatty(self.fd) and os.fstat(self.fd) and os.ttyname(self.fd)
        
        else:
            if self.process is not None:
                return self.process.isalive()
    
    def kill(self):
        del self.process
        self.process = None