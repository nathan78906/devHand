from socketIO_client import SocketIO, LoggingNamespace
#import webbrowser
import webview
import threading

socketIO = SocketIO('f237c8a0.ngrok.io', 80, LoggingNamespace)

def on_connect():
    print("Connected.")

def on_thing(data):
    if data["devHand"] == True:
        print("Received message from Google Assistant")

def on_stackoverflow(data):
    if data["devHand"] == True:
        try:
            webview.destroy_window()
        except Exception:
            pass

        print("Received StackOverflow question:", data["query"])
        #webbrowser.open(data["link"])

        with open("style.css") as css_file:
            css = css_file.read()

            html = f"""<!DOCTYPE html>
            <html>
                <head>
                    <title>{data['query']}</title>
                    <style>
                        {css}
                    </style>
                </head>
                <body>
                    <div id="answer">
                        <h3 style="answer-heading">BEST ANSWER ({data['score']})</h3>
                        {data['html']}
                    </div>
                </body>
            </html>
            """

        def load_html():
            webview.load_html(html)

        t = threading.Thread(target=load_html)
        t.start()
        webview.create_window(data["query"], width=500, height=700)

socketIO.on('connect', on_connect)
socketIO.on("thing", on_thing)
socketIO.on("stackoverflow", on_stackoverflow)
socketIO.wait()
