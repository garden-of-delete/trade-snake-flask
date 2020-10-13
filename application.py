from flask import Flask, render_template, request
from flask_cors import CORS
import json
import redis

r = redis.Redis(host='ec2-54-215-48-242.us-west-1.compute.amazonaws.com', port=6379, db=2, password='insight')

app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

'''
@app.route('/')
def hello_world():
    trades = {}
    with open("static/test_trades.json",'r') as test_trades:
        trades = json.load(test_trades)
        trades.sort(reverse=True, key=lambda t : t['ppj'])
    #sprites = [json['sprites'][key] for key in json['sprites'] if isinstance(json['sprites'][key], str)]
    return render_template('hello.html',trades=trades)
'''

@app.route('/api/trades')
def serve_trades():
    trades = {}
    current_iter = 0
    trades[current_iter] = json.loads(r.get(current_iter))
    while True:
        current_iter, keys = r.scan(current_iter)
        for key in keys:
            trades[int(key)] = json.loads(r.get(int(key)))
        if current_iter == 0:
            break
    return json.dumps(trades)

@app.route('/api/accept-trade', methods=['POST'])
def accept_trade():
    print(request.form)
    print(request.form.selected_trade)
    #r.delete('')

if __name__ == '__main__':
    app.run(host='0.0.0.0')