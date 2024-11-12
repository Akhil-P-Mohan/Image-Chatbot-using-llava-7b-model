# app.py
#imagechatbot

from flask import Flask, request, render_template, send_file, jsonify
from PIL import Image
import ollama
import os
from werkzeug.utils import secure_filename
from flask import url_for

app = Flask(__name__)


@app.route("/imagedescription")
def image_description():
    return render_template("imagedescription.html")

@app.route("/texttoimage")
def text_to_image():
    return render_template("texttoimage.html")


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
                question = request.form["question"]
                message = {
                    'role': 'user',
                    'content': question,
                    'images': [image_path]
                }
                image_url = url_for('static', filename='images/' + filename)
            else:
                question = request.form["question"]
                message = {
                    'role': 'user',
                    'content': question
                }
                image_url = None
        else:
            question = request.form["question"]
            message = {
                'role': 'user',
                'content': question
            }
            image_url = None

        

        # Use the ollama.chat function to generate a response
        res = ollama.chat(
            model="llava:7b",
            messages=[message]
            
        )

        # Render the response.html template with the response and image
        return render_template("response.html", question=question, response=res['message']['content'], image_url=image_url)
    except Exception as e:
        return render_template("error.html", error=str(e))

if __name__ == "__main__":
    app.run(debug=True)

