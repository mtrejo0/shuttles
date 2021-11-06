from flask import Flask, jsonify
from flask_cors import CORS
import api


app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
        
    response = {
        "message": "it works!"
    }

    return jsonify(response)

@app.route('/route_info')
def route_info():
    
    try:
        response = {
            "boston": api.get_data("boston"),
            "saferidebostone": api.get_data("saferidebostone")
        }

        return jsonify(response)

    except Exception as e:
        print(e)
        return jsonify({"error": 'Failed'}), 400
    

if __name__ == '__main__':
    app.run(debug=True, threaded=True, port=5000)