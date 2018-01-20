from flask import Flask, jsonify, request
from flask_socketio import SocketIO

import requests
import json
import re

key = "nGbD1fk2wjuOI2YdZ9w0Rg(("

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

        url = "https://api.stackexchange.com/2.2/search/advanced?order=desc&sort=votes&site=stackoverflow&q={}&key={}".format(query, key)
        search_response = requests.get(url=url)
        json_search_data = search_response.json()
        top_result_id = json_search_data["items"][0]["question_id"]


        url_answer = "https://api.stackexchange.com/2.2/questions/{}/answers?order=desc&sort=votes&site=stackoverflow&filter=!9Z(-wzu0T&key={}".format(top_result_id, key)
        answer_response = requests.get(url=url_answer)
        json_answer_data = answer_response.json()
        body = json_answer_data["items"][0]["body"]

        body_parsed = re.sub('<[^<]+?>', '', body)

        search_response = requests.get(url=url)
        json_search_data = search_response.json()

        socketio.emit("stackoverflow", {"devHand": True, "query": query})
        return jsonify({
            "speech": "Getting results from stack overflow dot com",
            "displayText": body_parsed,
            "data": {},
            "contextOut": [],
            "source": ""
        })

if __name__ == "__main__":
    socketio.run(app)
