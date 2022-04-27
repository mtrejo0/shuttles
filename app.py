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
                "name" : "Boston Daytime",
                "stops" : api.get_stops_data("boston")
            },
            {
                "name" : "Saferide Boston East",
                "stops" : api.get_stops_data("saferidebostone")
            }
        ]

        return jsonify(response)

    except Exception as e:
        print(e)
        return jsonify({"error": 'Failed'}), 400


@app.route('/sigma_nu', methods = ['POST', 'GET'])
def sigma_nu():
    
    try:

        daytime =  api.get_stops_data("boston")
        stop_stud = None
        stop_472 = None
        for each in daytime:
            if each["name"] == "84 Mass Ave":
                stop_stud = each
            if each["name"] == "478 Commonwealth Ave":
                stop_472 = each

        response = '''Boston Daytime, Student Center: {} min, 472: {} min'''.format(stop_stud["mins_away"], stop_472["mins_away"])

        return jsonify(response)

    except Exception as e:
        print(e)
        return jsonify({"error": str(e), "message": "Oops"}), 400
    

if __name__ == '__main__':
    app.run(debug=True, threaded=True, port=5000)