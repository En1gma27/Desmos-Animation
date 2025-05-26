from flask import Flask, render_template
import os
import sys
import subprocess
from desmos import get_latex, get_points, get_contours, flip_image

app = Flask(__name__)

print("Enter 1 to render a single image by run command python main.py name_of image.png")
print("Enter 2 to render a multiple images and combine them into a video:")
Mode = int(input())

if Mode == 1:
    path = os.path.join(os.path.dirname(__file__), 'desmos_animations')
    # Render 1 ảnh duy nhất, lấy tên file từ dòng lệnh
    if len(sys.argv) < 2:
        print("Please enter the image file name, for example: python page.py name.png")
        exit(1)
    filename = sys.argv[1]
    @app.route("/")
    def plot_image():

        points = ""
        shape = get_contours(filename)
        raw_latex = get_latex(filename.split(".")[0] + ".pnm")
        latex = "".join(raw_latex)
        points, c = get_points(filename)
        for i in c:
        
            return render_template("index.html", points=points, latex=latex, shape=shape, filename=filename)

elif Mode == 2:
    # Render nhiều frame trong thư mục FrameInput
    INPUT_DIR = os.path.join(os.path.dirname(__file__), 'FrameInput')
    subprocess.Popen([sys.executable, os.path.join(os.path.dirname(__file__), 'FrameRender.py')])
    @app.route("/frame/<filename>")
    def plot_image(filename):
        filepath = os.path.join(INPUT_DIR, filename)
        colors = ""
        points = ""
        shape = get_contours(filepath)
        raw_latex = get_latex(filepath.split(".")[0] + ".pnm")
        latex = "".join(raw_latex)
        points, c = get_points(filepath)
        for i in c:
            colors += str(i) + "~"
        return render_template("index.html", colors=colors, points=points, latex=latex, shape=shape, filename=filename)

if __name__ == "__main__":
    app.run()
