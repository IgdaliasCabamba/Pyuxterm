from _system import *
from server import *
from utils import list_all_themes
from src.rpc import evalRPC

app.on_startup.append(on_startup)
app.router.add_static('/static', STATIC_PATH)
app.router.add_get('/', index)
app.router.add_post('/', evalRPC)
app.router.add_get('/xterm/theme/{theme_name}', XtermRoutes.get_theme)
app.router.add_post('/xterm/theme/{theme_name}', XtermRoutes.post_theme)
app.router.add_get('/xterm/themes/update', XtermRoutes.update_themes)


def run():
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
    
    parser.add_argument('-t',
                        '--theme',
                        help="Enter a theme to uxterm",
                        default="default",
                        type = str)

    parser.add_argument('-ct',
                        '--custom-theme',
                        help="Use a custom theme on uxterm",
                        default="",
                        type = str)
    
    parser.add_argument('--list-themes', help="List all themes and exit", action='store_true')

    args=parser.parse_args()
    
    if args.list_themes:
        sys.exit(list_all_themes())    


    sys.exit(run_new_term(args.command, args.host, args.port, args.binargs, args.theme, args.custom_theme))

    

if __name__ == "__main__":
    run()