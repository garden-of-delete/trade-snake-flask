from flask import Flask, render_template
import json
import redis

r = redis.Redis(host='ec2-54-215-48-242.us-west-1.compute.amazonaws.com', port=6379, db=2, password='insight')

app = Flask(__name__)

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

@app.route('/trades')
def serve_trades():
    trades = {}
    current_iter = 0
    trades[current_iter] = json.loads(r.get(current_iter))
    while True:
        current_iter, keys = r.scan(current_iter)
        for key in keys:
            trades[key] = json.loads(r.get(key))
        if current_iter == 0:
            break
    return json.dumps(trades)

if __name__ == '__main__':
    app.run(host='0.0.0.0')