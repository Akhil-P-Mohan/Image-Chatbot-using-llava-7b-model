from flask import Flask, request, render_template, send_file, jsonify, url_for
from PIL import Image
import ollama  # Assuming Ollama is used for both chat and image generation
import os
from werkzeug.utils import secure_filename
import requests
import time
from diffusers import StableDiffusionGLIGENPipeline
import torch
from transformers import AutoTokenizer
from diffusers.utils import load_image


app = Flask(__name__)

# Load the GLIGEN model and tokenizer once at startup

pipe = StableDiffusionGLIGENPipeline.from_pretrained(
    "masterful/gligen-1-4-generation-text-box", variant="fp16", torch_dtype=torch.float16
)
pipe = pipe.to("cuda")

# Route to render the image description page
@app.route("/imagedescription")
def image_description():
    return render_template("imagedescription.html")

# Route to render the text-to-image generation page
@app.route("/texttoimage")
def text_to_image():
    return render_template("texttoimage.html")

# Route for the home page
@app.route("/")
def index():
    return render_template("index.html")

# Route to handle image description and questions
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

        # Use the Ollama model (or another model) for image description
        res = ollama.chat(
            model="llava:7b",  # or another relevant model for image descriptions
            messages=[message]
        )

        return render_template("response.html", question=question, response=res['message']['content'], image_url=image_url)

    except Exception as e:
        return render_template("error.html", error=str(e))


# Route for generating an image from text
@app.route("/generate_image", methods=["POST"])
def generate_image():
    try:
        # Get the text prompt, phrases, and bounding boxes from the form
        prompt = request.form["prompt"]
        
        # Parse phrases and bounding boxes from the form (example input format)
        #phrases = request.form.getlist("phrases")  # e.g., ["a waterfall", "a high speed train"]
        
        #boxes = request.form.getlist("boxes")  # Example input format: "x1,y1,x2,y2"
        #boxes = [[0.1, 0.2, 0.4, 0.5]]

        
        # Convert boxes to the expected format
        #boxes = [list(map(float, box.split(','))) for box in boxes]  # Convert string to list of floats

        # Generate an image using GLIGEN with bounding boxes and phrases
        with torch.no_grad():
            images = pipe(
                prompt=prompt,
                #gligen_phrases=phrases,
               #gligen_boxes=boxes,
                #gligen_scheduled_sampling_beta=1,
                output_type="pil",
                num_inference_steps=50,
            ).images

        # Save the generated image
        filename = f"{secure_filename(prompt)}_{str(int(time.time()))}.png"
        image_path = os.path.join("static", "generated_images", filename)
        images[0].save(image_path)

        image_url = url_for('static', filename=f'generated_images/{filename}')
        return render_template("response.html", question=prompt, image_url=image_url)

    except Exception as e:
        return render_template("error.html", error=str(e))




if __name__ == "__main__":
    app.run(debug=True)
