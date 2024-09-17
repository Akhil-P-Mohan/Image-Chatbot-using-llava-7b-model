#app.py

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

# Define a route for handling image uploads and questions
@app.route("/ask", methods=["POST"])
def ask():
    try:
        image_file = request.files["image"]
        question = request.form["question"]

        # Save the image to a temporary file
        filename = secure_filename(image_file.filename)
        image_path = os.path.join("static", "images", filename)
        image_file.save(image_path)

        # Use the ollama.chat function to generate a response
        res = ollama.chat(
            model="llava:7b",
            messages=[
                {
                    'role': 'user',
                    'content': question,
                    'images': [image_path]
                }
            ]
        )

        # Return the response as a JSON object
        return jsonify({'response': res['message']['content']})
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == "__main__":
    app.run(debug=True)
