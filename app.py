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
        
        response = ""
        
        # daytime =  api.get_stops_data("boston", "84 Mass Ave")
        # api.get_stops_data("boston", "478 Commonwealth Ave")
        # stop_stud = [each for each in daytime if each["name"] == "84 Mass Ave"][0]
        # stop_472 = [each for each in daytime if each["name"] == "478 Commonwealth Ave"][0]
        
        stop1 = api.get_stops_data("boston", "84 Mass Ave") + "\n"
        stop2 = api.get_stops_data("boston", "478 Commonwealth Ave") + "\n"

        if not "Not Available" in stop1 and not "Not Available" in stop2:
            response += "Boston Daytime\n\n"
            response += stop1
            response += stop2

        stop1 = api.get_stops_data("saferidebostone", "84 Mass Ave") + "\n"
        stop2 = api.get_stops_data("saferidebostone", "478 Commonwealth Ave") + "\n"

        if not "Not Available" in stop1 and not "Not Available" in stop2:
            response += "Boston East\n\n"
            response += stop1
            response += stop2


        response += "Harvard M2\n\n"
        
        kenmore = api.get_m2_stop("Kenmore (Outbound)")
        response+=kenmore + "\n"
        
        mit = api.get_m2_stop("Mass Ave at MIT (Southbound)")
        response+=mit + "\n"
        
        return jsonify(response)

    except Exception as e:
        print(e)
        return jsonify({"error": str(e), "message": "Oops"}), 400
    

if __name__ == '__main__':
    app.run(debug=True, threaded=True, port=5000)