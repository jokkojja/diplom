from flask import Flask, request, Response
import json

app = Flask(__name__)

#@app.route('/')
#def home():
    #return {'hello': 'world'}

@app.route('/calc', methods=['POST'])
def calc():
    one = request.json['first']
    two = request.json['two']
    res = one + two
    return Response(json.dumps({'response' : res}))

if __name__ == '__main__':
    app.run(debug=True)