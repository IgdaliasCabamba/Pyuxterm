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

from aiohttp import web
import socketio

import src.urequirements as urequirements
import src.uterm as uterm

urequirements.main()

usocket = socketio.AsyncServer()
app = web.Application()
usocket.attach(app)
usocket_config = dict()

terminal_api = uterm.TerminalCoreApi(rows=50, cols=50)

async def read_and_forward_pty_output():
    max_read_bytes = 1024 * 20
    while True:
        await usocket.sleep(0.01)
        output = terminal_api.read(max_read_bytes)
        if output:    
            await usocket.emit("pty-output", {"output": output}, namespace="/pty")

async def index(request):
    """Serve the client-side application."""
    with open(os.path.join(TEMPLATES_PATH, 'index.html')) as f:
        return web.Response(text=f.read(), content_type='text/html')

@usocket.on("pty-input", namespace="/pty")
async def pty_input(sid, data):
    """write to the child pty. The pty sees this as if you are typing in a real
    terminal.
    """
    terminal_api.write(data["input"].encode())

@usocket.on("resize", namespace="/pty")
async def resize(sid, data):
    terminal_api.set_window_size(data["rows"], data["cols"])

@usocket.on("connect", namespace="/pty")
async def connect(sid,environ):
    """new client connected"""
    terminal_api.spawn(usocket_config["cmd"])
    usocket.start_background_task(target=read_and_forward_pty_output)

def run_new_term(command:str = "python3", host:str="127.0.0.1", port:int=9990, command_args:str=""):    
    usocket_config["cmd"] = uterm.TermUtils.get_split_command(command, command_args)
    web.run_app(app, port = port, host = host)

app.router.add_static('/static', STATIC_PATH)
app.router.add_get('/', index)

def main():
    import argparse

    parser=argparse.ArgumentParser(description="Pyuxterm - A powerful cross platform Terminal emulator")
     
    parser.add_argument('-cmd',
                        '--command',
                        help="Enter the bin to run",
                        default="bash",
                        type=str)
 
    parser.add_argument('-ip',
                        '--host',
                        help="Enter the host Bruh",
                        default="127.0.0.1",
                        type=str)
 
    parser.add_argument('-p',
                        '--port',
                        help="Enter the port XD",
                        default=9990,
                        type = int)
    
    parser.add_argument('-ba',
                        '--binargs',
                        help="Enter args to bin",
                        default="",
                        type = str)
     
    args=parser.parse_args()

    sys.exit(run_new_term(args.command, args.host, args.port, args.binargs))

if __name__ == '__main__':
    main()
