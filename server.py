from flask import Flask, jsonify, request
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app)

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/assistant", methods=["POST"])
def assistant():
    action = request.get_json()["result"]["action"]
    print(action)
    if action == "message.sendtest":
        socketio.emit("thing", {"devHand": True})
        return jsonify({
            "speech": "Done",
            "displayText": "Done",
            "data": {},
            "contextOut": [],
            "source": ""
        })
    elif action == "howto":
        query = request.get_json()["result"]["resolvedQuery"]
        socketio.emit("stackoverflow", {"devHand": True, "query": query})
        return jsonify({
            "speech": "Getting results from stack overflow dot com",
            "displayText": "Getting results from StackOverflow.com",
            "data": {},
            "contextOut": [],
            "source": ""
        })

if __name__ == "__main__":
    socketio.run(app)
