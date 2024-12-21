from flask import Flask, request, jsonify
from google.oauth2 import service_account
from google.cloud import dialogflow_v2 as dialogflow
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET'])
def home():
    return "Chatbot Ticketing System for Museums is running!"

@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)
    print("Request:")
    print(json.dumps(req, indent=4))

    res = process_request(req)
    res = jsonify(res)
    res.headers['Content-Type'] = 'application/json'
    return res

def process_request(req):
    query_result = req.get("queryResult")

    if query_result.get("action") == "book_ticket":
        visitor_name = query_result.get("parameters").get("name")
        visit_date = query_result.get("parameters").get("date")
        ticket_type = query_result.get("parameters").get("ticket_type")

        response_text = (f"Thank you, {visitor_name}. Your {ticket_type} ticket has been booked for {visit_date}. "
                         "Please proceed with the payment to confirm your booking.")

        return {"fulfillmentText": response_text}

    elif query_result.get("action") == "provide_info":
        exhibit = query_result.get("parameters").get("exhibit")

        # Example response, can be extended with real data
        response_text = (f"The {exhibit} exhibit is located in Hall 3. Timings are from 10 AM to 5 PM. "
                         "Let me know if you need further assistance!")

        return {"fulfillmentText": response_text}

    else:
        return {"fulfillmentText": "I'm sorry, I couldn't understand your request. Can you please repeat?"}

if __name__ == '__main__':
    app.run(debug=True)
