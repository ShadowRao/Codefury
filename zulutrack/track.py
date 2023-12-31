from flask import Flask, jsonify, request
from datetime import datetime
import json
import time

app = Flask(__name__)
url_timestamp = {}
url_viewtime = {}
prev_url = ""

def url_strip(url):
    if "http://" in url or "https://" in url:
        url = url.replace("https://", '').replace("http://", '').replace('\"', '')
    if "/" in url:
        url = url.split('/', 1)[0]
    return url

@app.route('/send_url', methods=['POST'])
def send_url():
    resp_json = request.get_data()
    params = resp_json.decode()
    url = params.replace("url=", "")
    id=params.replace("id=", "")
    print(id)
    print("currently viewing: " + url_strip(url))
    parent_url = url_strip(url)

    global url_timestamp
    global url_viewtime

    global prev_url

    
    print("initial db prev tab: ", prev_url)
    print("initial db timestamp: ", url_timestamp)
    
    print("initial db viewtime: ", url_viewtime)
    # print("intial time: ", datetime.fromtimestamp(url_timestamp[url_strip(url)]))

    if parent_url not in url_timestamp.keys():
        url_viewtime[parent_url] = 0

    if prev_url != '':
        time_spent = int(time.time() - url_timestamp[prev_url])
        url_viewtime[prev_url] = url_viewtime[prev_url] + time_spent
    


    x = int(time.time())
    url_timestamp[parent_url] = x
    prev_url = parent_url
    print("final timestamps: ", url_timestamp)
    print("final viewtimes: ", url_viewtime)
    print("intial time of the website being opened: ", datetime.fromtimestamp(x))
    print("\n\n")
   


    with open('./zulutrack/extension/file.txt', 'w') as file:
        file.write(json.dumps(url_viewtime))
    with open('./zulutrack/extension/file2.txt', 'w') as file:
        file.write(prev_url)
    return jsonify({'message': 'success!'}),200


@app.route('/quit_url', methods=['POST'])
def quit_url():
    resp_json = request.get_data()
    print("Url closed: " + resp_json.decode())
    return jsonify({'message': 'quit success!'}), 200


app.run(host='0.0.0.0', port=5000)