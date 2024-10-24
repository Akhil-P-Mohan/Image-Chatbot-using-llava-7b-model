# Image Chatbot

This is a simple Flask web application that allows users to ask questions with optional images, and get responses from the LLaVA model.

## Features:
- Upload an image and ask a question.
- Receive a response based on the image and the question.

## Requirements
- Python 3.8+
- Flask
- Pillow
- ollama
- Werkzeug

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/your-username/image-chatbot.git
   cd image-chatbot
2.Install dependencies:
   ```bash
   pip install -r requirements.txt
3.Run the application:
   ```bash
   python app.py
4.Open a browser and visit http://127.0.0.1:5000 to use the application.

##Notes.

Ensure the static/images directory exists for uploaded images.
You may need to download the LLaVA model separately.


### 5. **`.gitignore`**
To prevent certain files from being included in your repository (e.g., virtual environments, cache files, or uploaded images), create a `.gitignore` file.

#### Example `.gitignore`:
