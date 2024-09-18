# app.py

from flask import Flask, request, render_template, send_file, jsonify
from PIL import Image
import ollama
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Define a route for the home page
@app.route("/")
def index():
    return render_template("index.html")

# Define a route for handling questions
@app.route("/ask", methods=["POST"])
def ask():
    try:
        
        # Check if an image is provided
        if "image" in request.files:
            image_file = request.files["image"]
            filename = secure_filename(image_file.filename)
            if filename:  # Check if filename is not empty
                image_path = os.path.join("static", "images", filename)
                image_file.save(image_path)
                question = ""
                message = {
                    'role': 'user',
                    'content': question,
                    'images': [image_path]
                }
            else:
                question = request.form["question"]
                message = {
                    'role': 'user',
                    'content': question
                }
        else:
            question = request.form["question"]
            message = {
                'role': 'user',
                'content': question
            }

        

        # Use the ollama.chat function to generate a response
        res = ollama.chat(
            model="llava:7b",
            messages=[message]
            
        )

        # Return the response as a JSON object
        return jsonify(res['message']['content'])
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == "__main__":
    app.run(debug=True)