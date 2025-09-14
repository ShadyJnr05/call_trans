from flask import Flask, request, jsonify, send_file, session, render_template
import os
import whisper
from deep_translator import GoogleTranslator
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "supersecretkey"  # For session handling

latest_transcript = ""
users = {}  # {username: password_hash}

# Load Whisper model
model = whisper.load_model("base")

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if username in users:
        return jsonify({"status": "error", "message": "Username already exists."})

    users[username] = generate_password_hash(password)
    return jsonify({"status": "success", "message": "Signup successful! Please login."})

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if username not in users or not check_password_hash(users[username], password):
        return jsonify({"status": "error", "message": "Invalid username or password."})

    session['user'] = username
    return jsonify({"status": "success", "message": f"Logged in as {username}."})

def login_required(func):
    from functools import wraps
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'user' not in session:
            return jsonify({"status": "error", "message": "You must be logged in to perform this action."})
        return func(*args, **kwargs)
    return wrapper

@app.route('/upload', methods=['POST'])
@login_required
def upload_file():
    global latest_transcript
    if 'file' not in request.files:
        return jsonify({"status": "error", "message": "No file uploaded"})

    file = request.files['file']
    filename = file.filename
    os.makedirs("uploads", exist_ok=True)
    file_path = os.path.join("uploads", filename)
    file.save(file_path)

    try:
        result = model.transcribe(file_path)
        latest_transcript = result["text"]
        return jsonify({
            "status": "success",
            "message": "Transcription completed!",
            "transcript": latest_transcript
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@app.route('/translate', methods=['POST'])
@login_required
def translate_text():
    global latest_transcript
    data = request.get_json()
    transcript = data.get("transcript", "")
    target_lang = data.get("target_lang", "en")

    if not transcript:
        return jsonify({"status": "error", "message": "Transcript is empty."})

    try:
        translated = GoogleTranslator(source='auto', target=target_lang).translate(transcript)
        latest_transcript = translated
        return jsonify({"status": "success", "translation": translated})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@app.route('/download', methods=['GET'])
@login_required
def download_transcript():
    global latest_transcript
    if not latest_transcript:
        return jsonify({"status": "error", "message": "No transcript available to download."})

    filename = "transcript.txt"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(latest_transcript)

    return send_file(filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
