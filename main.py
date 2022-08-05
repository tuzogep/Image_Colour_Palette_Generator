from flask import Flask, render_template, request, flash, redirect, url_for
from werkzeug.utils import secure_filename
from flask_bootstrap import Bootstrap
import numpy as np
from scipy import misc
from PIL import Image
import pandas as pd
import os

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}
app = Flask(__name__)
UPLOAD_FOLDER = os.path.join('static', 'uploads')
app.config[UPLOAD_FOLDER] = UPLOAD_FOLDER
Bootstrap(app)


def color_count(filename):
    """Takes the filename as an argument and returns the top 10 colors of the image"""
    im = Image.open(f"{UPLOAD_FOLDER}/{filename}")
    im_np = np.array(im)
    # print(f"The type of the image: {type(im_np)}")
    print(f"The shape of the image: {np.shape(im_np)}")
    im_width = np.shape(im_np)[0]
    im_height = np.shape(im_np)[1]
    # print(im_np)
    # print(im.format, im.size, im.mode)
    pix = im.load()
    # print(pix[500, 500])
    colors_rgb = []
    for x in range(0, im_width):
        for y in range(0, im_height):
            colors_rgb.append(pix[y, x])

    count = pd.Series(colors_rgb).value_counts()
    top_10_colors = count[:10]
    # print(count[:10])
    hex_list = []
    for i in top_10_colors.index:
        hex_list.append(f"{'#%02x%02x%02x' % i}")
    color_dict = {
        "RGB": top_10_colors.index,
        "HEX": hex_list,
        "Color": hex_list
    }
    return color_dict


def rgb_to_hex(list):
    """Takes a list of RGB tuples and converts them to hexademical strings. Returns a list"""
    hex_list = []
    for i in list:
        hex_list.append('#%02x%02x%02x' % i)
    return hex_list

# test = color_count("66720568_a_1.jpg")
# print(test)

def allowed_file(filename):
    """Checks if the extension is valid"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=["GET", "POST"])
def home():
    colors = []
    image_to_display = ""
    colors_hex = []
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
            # colors_hex = rgb_to_hex(colors)
            image_to_display = f"{UPLOAD_FOLDER}/{filename}"
    return render_template("index.html", color_list=colors, image_location=image_to_display)


if __name__ == "__main__":
    app.run(debug=True)
