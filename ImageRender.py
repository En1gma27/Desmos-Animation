from flask import Flask, render_template
import os
import sys
from desmos import get_latex, get_points, get_contours, flip_image

app = Flask(__name__)

filename = sys.argv[1]  # Lấy tên file ảnh từ dòng lệnh

@app.route("/")
def plot_image():
    points = ""
    shape = get_contours(filename)
    raw_latex = get_latex(filename.split(".")[0] + ".pnm")
    latex = "".join(raw_latex)
    points, c = get_points(filename)
    for i in c:
        colors += str(i) + "~"
    return render_template("index.html", points=points, latex=latex, shape=shape, filename=filename)

if __name__ == "__main__":
    app.run()






















