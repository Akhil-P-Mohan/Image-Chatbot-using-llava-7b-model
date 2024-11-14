# app.py
#imagechatbot

from flask import Flask, request, render_template, send_file, jsonify,session
from PIL import Image
import ollama
import os
from werkzeug.utils import secure_filename
from flask import url_for

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Generates a random 24-byte string



@app.route("/newchat")
def new_chat():
    # Clear the messages from the session
    session.pop('messages', None)
    return  render_template("chat.html") # Redirect to the home page (chat page)


@app.route("/imagedescription")
def image_description():

    session.pop('messages', None)

    return render_template("img.html")

@app.route("/texttoimage")
def text_to_image():
    return render_template("texttoimage.html")


# Define a route for the home page
@app.route("/")
def index():
    return render_template("chat.html")

# Define a route for handling questions(image description)
@app.route("/imgdes", methods=["POST"])
def imgdes():
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

        # Prepare the response message
        response_message = {
            'image_url':image_url,
            'question': question,
            'response': res['message']['content']
            
        }

        # Initialize the messages list in the session if it doesn't exist
        if 'messages' not in session:
            session['messages'] = []

        # Append the new question and response to the session
        session['messages'].append(response_message)
        session.modified = True  # Mark the session as modified


        # Render the response.html template with the response and image
        return render_template("imgresponse.html",messages=session['messages'] )
    except Exception as e:

       # Prepare the error message
        error_message = {
            'image_url': image_url,
            'question': question,
            'response': str(e)
        }
        
        # Initialize the messages list in the session if it doesn't exist
        if 'messages' not in session:
            session['messages'] = []

        # Append the error message to the session
        session['messages'].append(error_message)
        session.modified = True  # Mark the session as modified

        # Render the response.html template with the error message
        return render_template("imgresponse.html", messages=session['messages'])


# Define a route for handling questions (chatting)
@app.route("/chat", methods=["POST"])
def chat():
    try:
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

        # Prepare the response message
        response_message = {
            'question': question,
            'response': res['message']['content']
        }

        # Initialize the messages list in the session if it doesn't exist
        if 'messages' not in session:
            session['messages'] = []

        # Append the new question and response to the session
        session['messages'].append(response_message)
        session.modified = True  # Mark the session as modified

        # Render the response.html template with the response
        return render_template("chatresponse.html",  messages=session['messages'])
    except Exception as e:

        # Prepare the error message
        error_message = {
            'question': question,
            'response': str(e)
        }
        
        # Initialize the messages list in the session if it doesn't exist
        if 'messages' not in session:
            session['messages'] = []

        # Append the error message to the session
        session['messages'].append(error_message)
        session.modified = True  # Mark the session as modified

        # Render the response.html template with the error message
        return render_template("chatresponse.html", messages=session['messages'])
    

if __name__ == "__main__":
    app.run(debug=True)

