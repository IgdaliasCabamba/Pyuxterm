import aiohttp_jinja2
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


class PtyInterface:

    def input_(text: str, *args, **kwargs) -> None:
        terminal_api.write(text.encode())


class XtermRoutes:

    def update_themes(request) -> web.Response:
        uterm.XTermSettings.update_themes()

    def post_theme(request) -> web.Response:
        ...

    async def get_theme(request) -> web.Response:
        theme_name:str = request.match_info['theme_name']

        theme = uterm.XTERM_SETTINGS.themes.get(
            theme_name.lower(),
            uterm.XTermSettings.Defaults.THEME
        )

        return web.json_response(theme, content_type='application/json')


class UIInterface:

    async def updateUi(settings: dict) -> bool:
        await usocket.emit("pty-ui", {"settings": settings}, namespace="/pty")
        return True

    async def updateXtermTheme(theme_name: str) -> bool:
        await usocket.emit("pty-set-theme", {"name": theme_name}, namespace="/pty")
        return True


async def read_and_forward_pty_output() -> None:
    max_read_bytes = 1024 * 20
    while True:
        await usocket.sleep(0.01)
        output = terminal_api.read(max_read_bytes)
        if output:
            await usocket.emit("pty-output", {"output": output}, namespace="/pty")


async def on_startup(app):
    if "cmd" not in usocket_config.keys():
        usocket_config["cmd"] = uterm.TermUtils.get_split_command(
            "python3", "")

    if "theme" not in usocket_config.keys():
        usocket_config["theme"] = "default"


@aiohttp_jinja2.template('index.html')
async def index(request) -> dict:
    """Serve the client-side application."""

    theme = uterm.XTERM_SETTINGS.themes.get(
        usocket_config["theme"],
        uterm.XTermSettings.Defaults.THEME
    )
    return {"cssvar_background": theme["background"]}


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

    await usocket.emit("pty-set-theme", {"name": usocket_config["theme"]}, namespace="/pty")


def run_new_term(command: str = "python3", host: str = "127.0.0.1", port: int = 9990, command_args: str = "", theme: str = "default", custom_theme: str = None) -> None:
    usocket_config["cmd"] = uterm.TermUtils.get_split_command(
        command, command_args)
    usocket_config["theme"] = theme.lower()
    
    if custom_theme:
        usocket_config["theme"] = uterm.XTERM_SETTINGS.add_theme(custom_theme)

    web.run_app(app, port=port, host=host)