import src.uterm as uterm
from _system import *
import rich

def list_all_themes() -> None:
    themes = uterm.XTERM_SETTINGS.themes.keys()
    for theme in themes:
        rich.print(f"[bold green]{theme}")
    rich.print(f"[bold yellow]TOTAL[/]: {len(themes)}")
