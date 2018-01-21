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
        if json_search_data["items"]:
            top_result_id = json_search_data["items"][0]["question_id"]

            url_answer = "https://api.stackexchange.com/2.2/questions/{}/answers?order=desc&sort=votes&site=stackoverflow&filter=!-*jbN.9m(dML&key={}".format(top_result_id, key)
            answer_response = requests.get(url=url_answer)
            json_answer_data = answer_response.json()
            if json_answer_data["items"]:
                body = json_answer_data["items"][0]["body"]
                answer_link = json_answer_data["items"][0]["link"]

                body_parsed = re.sub(r'<[^<]+?>', '', body)

                short_body = ' '.join(body_parsed.split(" ")[:20]) + "..."
                
                body_spoken = re.sub(r'\<pre\>.*\</pre\>', '', body)
                body_spoken = re.sub(r'\<code\>.*\</code\>', '', body_spoken)
                body_spoken = re.sub(r'\<a.*\>(?P<text>.*)\</a\>', r'(\g<text>)', body_spoken)
                body_spoken = re.sub(r'\<img.*\>', '', body_spoken)
                body_spoken = re.sub(r'<[^<]+?>', '', body_spoken)
                body_spoken = ' '.join(body_spoken.split(" ")[:20]) + ". Read more on your PC."

                socketio.emit("stackoverflow", {"devHand": True, "query": query, "link": answer_link, "html": body})
                return jsonify({
                    "speech": body_spoken,
                    "displayText": short_body,
                    "data": {},
                    "contextOut": [],
                    "source": ""
                })
            else:
                return jsonify({
                    "speech": "It looks like there aren't any answers to that question. Big mystery!",
                    "displayText": "It looks like there aren't any answers to that question. Big mystery!",
                    "data": {},
                    "contextOut": [],
                    "source": ""
                })
        else:
            return jsonify({
                "speech": "Sorry, we didn't find any results for that search.",
                "displayText": "Sorry, we didn't find any results for that search.",
                "data": {},
                "contextOut": [],
                "source": ""
            })

if __name__ == "__main__":
    socketio.run(app)
