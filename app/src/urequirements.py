import requests
import os
import pathlib
from .static_files import *

root_path = os.environ["UTERM_ROOT_PATH"]

DATAS = {
    "https://unpkg.com/xterm@4.11.0/css/xterm.css":os.path.join(root_path, "static", "packages", "xterm", "css", "xterm.css"),
    "https://unpkg.com/xterm@4.11.0/lib/xterm.js":os.path.join(root_path, "static", "packages", "xterm", "lib", "xterm.js"),
    "https://unpkg.com/xterm-addon-fit@0.5.0/lib/xterm-addon-fit.js":os.path.join(root_path, "static", "packages", "xterm-addon-fit", "lib", "xterm-addon-fit.js"),
    "https://unpkg.com/xterm-addon-web-links@0.4.0/lib/xterm-addon-web-links.js":os.path.join(root_path, "static", "packages", "xterm-addon-web-links", "lib", "xterm-addon-web-links.js"),
    "https://unpkg.com/xterm-addon-search@0.8.0/lib/xterm-addon-search.js":os.path.join(root_path, "static", "packages", "xterm-addon-search", "lib", "xterm-addon-search.js"),
    "https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.0.1/socket.io.min.js":os.path.join(root_path, "static", "packages", "ajax", "libs", "socket.io", "socket.io.min.js"),
}

STATIC_DATA = {
    HTML:os.path.join(root_path, "templates", "index.html"),
    CSS:os.path.join(root_path, "static", "ustyle.css")
}

def touch(file):
    folder = pathlib.Path(file).parent
    if not os.path.exists(folder):
        os.makedirs(folder)
    pathlib.Path(file).touch()

def download(url):
    return requests.get(url, allow_redirects=True)

def save(content, name_with_path):
    touch(name_with_path)
    with open(name_with_path, 'wb') as fp:
        fp.write(content)

def main():
    for url, path in DATAS.items():
        if os.path.exists(path):
            continue
        else:
            resp = download(url)
            save(resp.content, path)
    
    for file, path in STATIC_DATA.items():
        if not os.path.exists(path):
            touch(path)
            with open(path, 'w') as fp:
                fp.write(file)

if __name__ == "__main__":
    main()