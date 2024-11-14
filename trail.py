from flask import Flask, request, render_template, url_for
from PIL import Image
import ollama  # Import the Llama library (replace with the actual import if different)
import os
from werkzeug.utils import secure_filename
import time
import io

app = Flask(__name__)



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
                message = {'role': 'user', 'content': question}
                image_url = None
        else:
            question = request.form["question"]
            message = {'role': 'user', 'content': question}
            image_url = None

        # Use Llama 3.2:3b for image description
        res = ollama.chat(
            model="llava:7b",
            messages=[message])

        return render_template("response.html", question=question, response=res['message']['content'], image_url=image_url)

    except Exception as e:
        return render_template("error.html", error=str(e),question=question,image_url=image_url)


# Route for generating an image from text
@app.route("/generate_image", methods=["POST"])
def generate_image():
    try:
        # Get the text prompt from the form
        prompt = request.form["prompt"]

        # Generate an image using the ollama library
        # Assuming ollama has a method for image generation
        response = ollama.generate_image(
            model="llava:7b",
            prompt=prompt)

        # Check if the response contains an image
        if 'image' in response:
            image_data = response['image']
            # Convert the image data to a PIL Image
            image = Image.open(io.BytesIO(image_data))

            # Save the generated image
            filename = f"{secure_filename(prompt)}_{str(int(time.time()))}.png"
            image_path = os.path.join("static", "generated_images", filename)
            image.save(image_path)

            image_url = url_for('static', filename=f'generated_images/{filename}')
            return render_template("response.html", question=prompt, image_url=image_url)
        else:
            return render_template("error.html", error="Image generation failed.",question=prompt)

    except Exception as e:
        return render_template("error.html", error=str(e),question=prompt)


if __name__ == "__main__":
    app.run(debug=True)
