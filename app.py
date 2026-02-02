import os
import tempfile
import asyncio
import edge_tts
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from faster_whisper import WhisperModel

# --- Configuration ---
MODEL_SIZE = "base.en" 
# Force CPU to avoid NVIDIA driver errors
MODEL_DEVICE = "cpu" 
MODEL_COMPUTE_TYPE = "int8"
TTS_VOICE = "en-GB-RyanNeural" #jarvis voice

# --- Initialization ---
print("Loading Whisper STT model...")
try:
    stt_model = WhisperModel(MODEL_SIZE, device=MODEL_DEVICE, compute_type=MODEL_COMPUTE_TYPE)
    print(f"Whisper model loaded on {MODEL_DEVICE}.")
except Exception as e:
    print(f"Error loading Whisper: {e}")
    stt_model = None

app = Flask(__name__)
CORS(app) 

# --- Routes ---
@app.route('/')
def index():
    return "Voice Assistant Server is running. Endpoints: /transcribe (STT), /speak (TTS)"

# 1. The Ear (Speech-to-Text)
@app.route('/transcribe', methods=['POST'])
def transcribe_audio():
    if stt_model is None: return jsonify({"error": "Model not loaded"}), 500
    if 'audio' not in request.files: return jsonify({"error": "No audio file"}), 400

    audio_file = request.files['audio']
    
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix='.webm') as temp_audio:
            audio_file.save(temp_audio.name)
            temp_audio_path = temp_audio.name
        
        segments, info = stt_model.transcribe(temp_audio_path, beam_size=5, language="en")
        transcript_text = " ".join(segment.text for segment in segments).strip()
        
        print(f"Heard: '{transcript_text}'")
        return jsonify({"transcript": transcript_text})

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if 'temp_audio_path' in locals() and os.path.exists(temp_audio_path):
            os.remove(temp_audio_path)

# 2. The Mouth (Text-to-Speech)
@app.route('/speak', methods=['POST'])
def speak_text():
    """
    Receives text JSON, generates an MP3 using Edge-TTS, and returns the audio file.
    """
    data = request.json
    text = data.get('text', '')
    
    if not text:
        return jsonify({"error": "No text provided"}), 400

    print(f"Speaking: '{text}'")

    try:
        # Create a temporary file for the MP3
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as temp_mp3:
            output_file = temp_mp3.name

        # Edge-TTS is asynchronous, so we need a helper loop to run it
        async def _generate_audio():
            communicate = edge_tts.Communicate(text, TTS_VOICE)
            await communicate.save(output_file)

        asyncio.run(_generate_audio())

        # Send the MP3 file back to the browser
        # The browser will play this file automatically
        return send_file(output_file, mimetype="audio/mpeg")

    except Exception as e:
        print(f"TTS Error: {e}")
        return jsonify({"error": str(e)}), 500
    # Note: We rely on the OS or a cleanup cron to remove the temp mp3 files 
    # because send_file needs it to exist when returning.

if __name__ == '__main__':
    print("Starting server on http://127.0.0.1:5000")
    app.run(host='127.0.0.1', port=5000, debug=False)