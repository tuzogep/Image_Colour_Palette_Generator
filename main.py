from flask import Flask, render_template, request, flash, redirect
from werkzeug.utils import secure_filename
from flask_bootstrap import Bootstrap
import os
from colorthief import ColorThief
from datetime import datetime

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get("APP_SECRET_KEY")
UPLOAD_FOLDER = os.path.join('static', 'uploads')
app.config[UPLOAD_FOLDER] = UPLOAD_FOLDER
Bootstrap(app)


def color_count(filename):
    """Takes the filename as an argument and returns the top 10 dominant colors of the image in RGB and HEX code,
    in a dictionary """
    color_thief = ColorThief(f"{UPLOAD_FOLDER}/{filename}")
    # build a color palette
    palette = color_thief.get_palette(color_count=11)
    # print(palette)
    hex_list = []
    for i in palette:
        hex_list.append(f"{'%02x%02x%02x' % i}")
    color_dict = {
        "RGB": palette,
        "HEX": hex_list,
        "Color": hex_list
    }
    return color_dict


def allowed_file(filename):
    """Checks if the extension is valid"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def empty_upload_folder():
    """Deletes files in the uploads folder"""
    uploaded_files = os.listdir(UPLOAD_FOLDER)
    if len(uploaded_files) > 0:
        empty_folder = [os.remove(f"{UPLOAD_FOLDER}/{file}") for file in uploaded_files]


@app.route('/', methods=["GET", "POST"])
def home():
    empty_upload_folder()
    colors = []
    image_to_display = ""
    if request.method == 'POST':
        # Check if the POST request has the file part
        if 'file' not in request.files:
            flash("No file part")
            return redirect(request.url)
        file = request.files["file"]
        # If the user does not select a file
        # the browser submits an empty file without a filename
        if file.filename == "":
            flash("No selected file")
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            colors = color_count(filename)
            image_to_display = f"{UPLOAD_FOLDER}/{filename}"
    return render_template("index.html", color_list=colors, image_location=image_to_display, now=datetime.utcnow())


if __name__ == "__main__":
    app.run(debug=True, port=5001)
