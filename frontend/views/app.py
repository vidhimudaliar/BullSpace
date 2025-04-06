from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS  # Allows frontend to call backend
import requests
from datetime import timedelta, datetime
from zoneinfo import ZoneInfo

app = Flask(__name__, static_url_path='', static_folder='frontend')
CORS(app)  # Enable CORS

# Canvas API Config
API_TOKEN = 'YOUR_API_TOKEN_HERE'  # Replace with valid token
CANVAS_DOMAIN = 'https://usflearn.instructure.com'
TODO_ENDPOINT = f"{CANVAS_DOMAIN}/api/v1/users/self/todo"
HEADERS = {'Authorization': f'Bearer {API_TOKEN}'}


@app.route('/')
def serve_page():
    return send_from_directory('frontend', 'todopage.html')


@app.route('/api/weekly-tasks')
def get_tasks():
    try:
        response = requests.get(TODO_ENDPOINT, headers=HEADERS)
        if response.status_code != 200:
            return jsonify({'error': 'Canvas API error'}), 500

        todos = response.json()
        now = datetime.now(ZoneInfo("America/New_York"))
        next_week = now + timedelta(days=7)

        weekly = []
        for item in todos:
            due = item.get('due_at') or item.get('assignment',
                                                 {}).get('due_at')
            if not due:
                continue
            try:
                due_date = datetime.fromisoformat(due.replace("Z", "+00:00"))
            except:
                continue
            if now <= due_date <= next_week:
                weekly.append({
                    'title':
                    item.get('title')
                    or item.get('assignment', {}).get('name', 'No Title'),
                    'due_date':
                    due_date.strftime('%Y-%m-%d %H:%M'),
                    'course':
                    item.get('context_name', 'Unknown Course')
                })

        return jsonify(weekly)

    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
