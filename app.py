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
        response = [
            {
                "name" : "boston",
                "stops" : api.get_stops_data("boston")
            },
            {
                "name" : "saferidebostone",
                "stops" : api.get_stops_data("saferidebostone")
            }
        ]

        return jsonify(response)

    except Exception as e:
        print(e)
        return jsonify({"error": 'Failed'}), 400
    

if __name__ == '__main__':
    app.run(debug=True, threaded=True, port=5000)