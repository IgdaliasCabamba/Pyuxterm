import pprint

import aiohttp_jinja2
import hjson
import jinja2
import socketio
import src.urequirements as urequirements
import src.uterm as uterm
from _system import *
from aiohttp import web

urequirements.main()

usocket = socketio.AsyncServer()
app = web.Application()
aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader(TEMPLATES_PATH))
usocket.attach(app)
usocket_config = dict()

terminal_api = uterm.TerminalCoreApi(rows=50, cols=50)


async def read_and_forward_pty_output() -> None:
    max_read_bytes = 1024 * 20
    while True:
        await usocket.sleep(0.01)
        output = terminal_api.read(max_read_bytes)
        if output:
            await usocket.emit("pty-output", {"output": output}, namespace="/pty")


async def update_ui(settings: dict) -> bool:
    return settings


async def eval_payload(prompt: str, aio: bool) -> str:
    if aio:
        return await eval(prompt)

    return eval(prompt)


async def exec_payload(prompt: str, aio: bool) -> str:
    if aio:
        return await exec(prompt)

    return exec(prompt)


async def evalRPC(request) -> web.Response:
    payload = await request.json()

    if "eval" in payload.keys():
        try:
            evaluated_res = await eval_payload(
                prompt=payload["eval"][">>>"],
                aio=payload["eval"]["async"]
            )
        except Exception as e:
            return web.json_response(
                {
                    "status": False,
                    "log": "Not Evaluated",
                    "code": 1,
                    f"Exception {e}": {
                        "name": str(e),
                        "args": e.args,
                    }
                }
            )

    if "exec" in payload.keys():
        try:
            _ = exec_payload(
                prompt=payload["exec"][">>>"],
                aio=payload["exec"]["async"]
            )
        except Exception as e:
            return web.json_response(
                {
                    "status": False,
                    "log": "Not Excuted",
                    "code": 2,
                    f"Exception {e}": {
                        "name": str(e),
                        "args": e.args,
                    }
                }
            )

    return web.json_response(
        {
            "status": True,
            "log": "sucess",
            "code": 0,
            "evaluated": evaluated_res
        }
    )


@aiohttp_jinja2.template('index.html')
async def index(request) -> dict:
    """Serve the client-side application."""

    theme = hjson.loads(usocket_config["theme"])
    bg_color = "#000000"
    if "background" in theme.keys():
        bg_color = theme["background"]

    return {'theme': usocket_config["theme"], "cssvar_background": bg_color}


@usocket.on("pty-input", namespace="/pty")
async def pty_input(sid, data: dict) -> None:
    """write to the child pty. The pty sees this as if you are typing in a real
    terminal.
    """
    terminal_api.write(data["input"].encode())


@usocket.on("resize", namespace="/pty")
async def resize(sid, data: dict) -> None:
    terminal_api.set_window_size(data["rows"], data["cols"])


@usocket.on("connect", namespace="/pty")
async def connect(sid, environ) -> None:
    """new client connected"""
    terminal_api.spawn(usocket_config["cmd"])
    usocket.start_background_task(target=read_and_forward_pty_output)


def run_new_term(command: str = "python3", host: str = "127.0.0.1", port: int = 9990, command_args: str = "", theme: str = "default") -> None:
    usocket_config["cmd"] = uterm.TermUtils.get_split_command(
        command, command_args)
    usocket_config["theme"] = uterm.TermUtils.get_theme(theme.lower())
    web.run_app(app, port=port, host=host)


def list_all_themes() -> None:
    for theme in uterm.THEMES.keys():
        print(theme)
