from flask import Flask, jsonify
app = Flask(__name__)

@app.route('/route1/<number>', methods=['GET'])
def route1(number):

    response = {}
    response["input"] = number
    response["output"] = number * 32
    
    return jsonify(response)


@app.route('/')
def index():
    return "<h1>Welcome to our server !!</h1>"

if __name__ == '__main__':
    app.run(threaded=True, port=5000)