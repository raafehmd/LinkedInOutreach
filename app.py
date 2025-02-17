# app.py
import os
from flask import Flask, request, jsonify
from linkedin_automation import send_connection_request
from ai_messaging import get_ai_response
from profile_generator import generate_profile
from calendar_integration import create_event
from compliance_dashboard import log_activity, get_activities
from auth import require_api_key
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["100 per hour"]
)

@app.route('/linkedin/connect', methods=['POST'])
@require_api_key
@limiter.limit("10 per minute")
def linkedin_connect():
    data = request.json
    profile_url = data.get('profileUrl')
    message = data.get('message')
    try:
        result = send_connection_request(profile_url, message)
        log_activity({
            'module': 'linkedin_automation',
            'action': 'send_connection_request',
            'details': {'profile_url': profile_url}
        })
        return jsonify({'success': True, 'result': result})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/ai/message', methods=['POST'])
@require_api_key
@limiter.limit("20 per minute")
def ai_message():
    data = request.json
    user_message = data.get('userMessage')
    try:
        response = get_ai_response(user_message)
        log_activity({
            'module': 'ai_messaging',
            'action': 'get_ai_response',
            'details': {'user_message': user_message}
        })
        return jsonify({'success': True, 'response': response})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/profile/generate', methods=['GET'])
@require_api_key
@limiter.limit("30 per minute")
def profile_generate():
    try:
        profile = generate_profile()
        log_activity({
            'module': 'profile_generator',
            'action': 'generate_profile',
            'details': {'full_name': profile.get('full_name')}
        })
        return jsonify({'success': True, 'profile': profile})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/calendar/appointment', methods=['POST'])
@require_api_key
@limiter.limit("10 per minute")
def calendar_appointment():
    data = request.json
    summary = data.get('summary')
    description = data.get('description')
    start = data.get('start')  # Format: "YYYY-MM-DDTHH:MM:SS"
    end = data.get('end')
    try:
        event = create_event(summary, description, start, end)
        log_activity({
            'module': 'calendar_integration',
            'action': 'create_event',
            'details': {'summary': summary}
        })
        return jsonify({'success': True, 'event': event})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/compliance/activities', methods=['GET'])
@require_api_key
@limiter.limit("5 per minute")
def compliance_activities():
    return jsonify({'success': True, 'activities': get_activities()})

if __name__ == '__main__':
    # In production, serve with a proper WSGI server (e.g., gunicorn)
    app.run(debug=False, port=3000)
