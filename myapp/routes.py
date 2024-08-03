from flask import Blueprint, jsonify, request, send_file, abort
from datetime import datetime, timedelta
import io
import requests
import os
from collections import defaultdict
import logging
import time

transformer_data = {
    "T-1001": {"latitude": 34.052235, "longitude": -118.243683},
    "T-1002": {"latitude": 40.712776, "longitude": -74.005974},
    "T-1003": {"latitude": 51.507351, "longitude": -0.127758},
    "T-1004": {"latitude": 35.689487, "longitude": 139.691711},
    "T-1005": {"latitude": 48.856613, "longitude": 2.352222},
    "T-1006": {"latitude": 55.755825, "longitude": 37.617298},
    "T-1007": {"latitude": 37.774929, "longitude": -122.419418},
    "T-1008": {"latitude": -33.868820, "longitude": 151.209290},
    "T-1009": {"latitude": 19.432608, "longitude": -99.133209},
    "T-1010": {"latitude": 39.904202, "longitude": 116.407394}
}

@route.route('/albert_send_sms', methods=['POST'])
def albert_send_sms():
    data = request.json
    message = data.get('message')
    transformer_id = data.get('transformer_id')
    phone = data.get('phone')
    
    if not message:
        return jsonify({'message': 'Message is required'}), 400

    if not transformer_id or transformer_id not in transformer_data:
        return jsonify({'message': 'Valid transformer_id is required'}), 400

    if not phone:
        return jsonify({'message': 'Valid phone number is required'}), 400

    lat = transformer_data[transformer_id]['latitude']
    long = transformer_data[transformer_id]['longitude']
    location_str = f"{lat}, {long}"
    message = message.replace("{location}", location_str)
    
    sms_api_key = os.environ.get('SMS_API_KEY')
    sms_url = f"https://sms.arkesel.com/sms/api?action=send-sms&api_key={sms_api_key}"
    sms_params = {
        'to': phone,
        'from': 'Transformer',
        'sms': message
    }
    
    try:
        response = requests.get(sms_url, params=sms_params)
        response.raise_for_status()
        return jsonify({'message': 'SMS sent successfully'}), 200
    except requests.RequestException as e:
        print(f"SMS sending failed: {e}")
        return jsonify({'message': 'Failed to send SMS'}), 500
