HTML = """
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <title>Uterm</title>
    <style>
      :root {
        --main-bg-color: #212121;
        --scrollbar-bg-color:transparent;
        --scrollbar-thumb-bg-color:rgba(250, 250, 250, 0.4);
        --scrollbar-thumb-hover-bg-color:rgb(250, 250, 250, 0.8)
      }
    </style>
    <link
      rel="stylesheet"
      href="/static/ustyle.css"
    />
    <link
      rel="stylesheet"
      href="/static/packages/xterm/css/xterm.css"
    />
  </head>
  <body>
    
    <div id="terminal"></div>

    <!-- xterm -->
    <script src="/static/packages/xterm/lib/xterm.js"></script>
    <script src="/static/packages/xterm-addon-fit/lib/xterm-addon-fit.js"></script>
    <script src="/static/packages/xterm-addon-web-links/lib/xterm-addon-web-links.js"></script>
    <script src="/static/packages/xterm-addon-search/lib/xterm-addon-search.js"></script>
    <script src="/static/packages/ajax/libs/socket.io/socket.io.min.js"></script>

    <script>
      const term = new Terminal({
        cursorBlink: true,
        macOptionIsMeta: true,
        scrollback: 1000,
      });
      // https://github.com/xtermjs/xterm.js/issues/2941
      const fit = new FitAddon.FitAddon();
      term.loadAddon(fit);
      term.loadAddon(new WebLinksAddon.WebLinksAddon());
      term.loadAddon(new SearchAddon.SearchAddon());

      term.open(document.getElementById("terminal"));
      fit.fit();
      term.resize(15, 50);
      fit.fit();
      
      term.setOption('theme', { background: '#212121' });

      term.onData((data) => {
        console.log("key pressed in browser:", data);
        socket.emit("pty-input", { input: data });
      });

      const socket = io.connect("/pty");
      const status = document.getElementById("status");

      socket.on("pty-output", function (data) {
        console.log("new output received from server:", data.output);
        term.write(data.output);
      });

      function fitToscreen() {
        fit.fit();
        const dims = { cols: term.cols, rows: term.rows };
        console.log("sending new dimensions to server's pty", dims);
        socket.emit("resize", dims);
      }

      function debounce(func, wait_ms) {
        let timeout;
        return function (...args) {
          const context = this;
          clearTimeout(timeout);
          timeout = setTimeout(() => func.apply(context, args), wait_ms);
        };
      }

      const wait_ms = 50;
      window.onresize = debounce(fitToscreen, wait_ms);
    </script>
  </body>
</html>
"""

CSS = """
* {
    margin: 0;
    padding: 0;
    border:0;
    vertical-align: baseline;
}

html, body {
    min-height: 100vh;
    height: 100%;
    overflow: hidden;
    background-color: var(--main-bg-color);
}

#terminal{
    width: 100vw;
    min-height: 100vh;
    max-height: 101vh;
}

::-webkit-scrollbar {
    width: 9px;
    height: 9px;
}
::-webkit-scrollbar-track {
    background-color: var(--scrollbar-bg-color);
}

::-webkit-scrollbar-thumb {
    background-color: var(--scrollbar-thumb-bg-color);
}

::-webkit-scrollbar-thumb:hover {
    background-color: var(--scrollbar-thumb-hover-bg-color);
}
"""