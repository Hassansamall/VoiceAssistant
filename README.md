# Voice Assistant

A Python-based voice assistant server using Flask. It provides Speech-to-Text (STT) capabilities using `faster_whisper` and Text-to-Speech (TTS) using `edge_tts`.

## Features

- **Speech-to-Text (STT):** Transcribes audio files uploaded to the `/transcribe` endpoint.
- **Text-to-Speech (TTS):** Converts text to speech and returns an audio file via the `/speak` endpoint.
- **REST API:** Simple Flask-based API for integration with frontend applications.

## Prerequisites

- Python 3.8+
- [FFmpeg](https://ffmpeg.org/download.html) (Required for audio processing)

## Installation

1.  Clone the repository:
    ```bash
    git clone <your-repo-url>
    cd VoiceAssistant
    ```

2.  Create and activate a virtual environment:
    ```bash
    python -m venv venv
    # Windows
    venv\Scripts\activate
    # Linux/Mac
    source venv/bin/activate
    ```

3.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

1.  Start the server:
    ```bash
    python app.py
    ```
    The server will start at `http://127.0.0.1:5000`.

2.  Open `voice-assistant-v4.html` (or `v3`) in your browser to interact with the assistant.

## API Endpoints

### `POST /transcribe`
- **Description:** specific audio file for transcription.
- **Form Data:** `audio` (File)
- **Response:** JSON `{ "transcript": "..." }`

### `POST /speak`
- **Description:** specific text for speech generation.
- **JSON Body:** `{ "text": "Hello world" }`
- **Response:** Audio file (MP3) or JSON error.

## Notes
- To avoid NVIDIA driver errors, the model is configured to run on CPU by default.
