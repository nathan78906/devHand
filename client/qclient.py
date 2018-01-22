import sys

from PyQt5.QtCore import QThread
from PyQt5.QtWidgets import QApplication
from PyQt5 import uic
from PyQt5 import QtWebEngineWidgets

from socketIO_client import SocketIO, LoggingNamespace
import threading
import webbrowser


app = QApplication(sys.argv)


from PyQt5 import QtCore, QtGui, QtWidgets

class AnswerView(QtWidgets.QDialog):
    def __init__(self):
        super(AnswerView, self).__init__()

        self.ui = uic.loadUi("answerview.ui")

        self.ui.openBrowserButton.clicked.connect(self.open_in_browser)

        self.thread = SocketListener()
        self.thread.signal.connect(self.update_html)
        self.thread.start()

    def update_html(self, html, url):
        self.url = url
        self.ui.textBrowser.setText(html)
        self.ui.show()

    def open_in_browser(self):
        webbrowser.open(self.url)



class SocketListener(QThread):
    signal = QtCore.pyqtSignal(str, str)

    def __init__(self, parent = None):
        super(SocketListener, self).__init__(parent)

        self.socketIO = SocketIO('f237c8a0.ngrok.io', 80, LoggingNamespace)
        self.socketIO.on('connect', self.on_connect)
        self.socketIO.on("thing", self.on_thing)
        self.socketIO.on("stackoverflow", self.on_stackoverflow)

    def run(self):
        self.socketIO.wait()

    def on_connect(self):
        print("Connected.")

    def on_thing(self, data):
        if data["devHand"] == True:
            print("Received message from Google Assistant")

    def on_stackoverflow(self, data):
        if data["devHand"] == True:
            print("Received StackOverflow question:", data["query"])
            #webbrowser.open(data["link"])

            with open("style.css") as css_file:
                css = css_file.read()

                html = (f"""<!DOCTYPE html>
                <html>
                    <head>
                        <title>{data['query']}</title>
                        <style>
                            {css}
                        </style>
                    </head>
                    <body>
                        <div style="answer">
                            <h3 style="answer-heading">BEST ANSWER ({data['answers'][0]['score']} points)</h3>
                            {data['answers'][0]['html']}
                        </div>"""
                + '\n'.join([f"""
                        <hr />
                        <div style="answer">
                            <h3 style="answer-heading">OTHER ANSWER ({i['score']} points)</h3>
                            {i['html']}
                        </div>
                """ for i in data["answers"][1:]])
                + f"""
                        </div>
                    </body>
                </html>
                """)

            self.signal.emit(html, data["answers"][0]["link"])


widget = AnswerView()

QApplication.setQuitOnLastWindowClosed(False)
sys.exit(app.exec_())