from flask import Flask, render_template
import requests
import json

app = Flask(__name__)



@app.route('/')
def hello_world():
    trades = {}
    with open("static/test_trades.json",'r') as test_trades:
        trades = json.load(test_trades)
        trades.sort(reverse=True, key=lambda t : t['ppj'])
    #sprites = [json['sprites'][key] for key in json['sprites'] if isinstance(json['sprites'][key], str)]
    return render_template('hello.html',trades=trades)

if __name__ == '__main__':
    app.run(host='0.0.0.0')