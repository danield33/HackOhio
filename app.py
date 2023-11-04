import base64
import io
import json
import os

import cv2
import keras_ocr
from flask import Flask, request, flash, redirect, render_template, jsonify
from PIL import Image
import time

from CSVUtils import *
from image_analysis import *
from image_reader import pathfind, extract_text

pipeline = None


def create_app():
    app = Flask(__name__)
    app.secret_key = 'super secret key'

    @app.route('/parseImage')
    def hello_world():  # put application's code here
        return 'Hello World!'

    @app.route('/', methods=['POST'])
    def upload_image():
        # if request.method == 'POST':
        # check if the post request has the file part
        now = time.time()

        data = request.data
        json_data = json.loads(data.decode('utf-8'))
        img_data = json_data['image']
        roomNumber = json_data['room_number']
        imgStart = base64.b64decode(img_data) # Gets actual image to later parse
        img_arr = np.frombuffer(imgStart, dtype=np.uint8)
        img_arr = cv2.imdecode(img_arr, cv2.IMREAD_COLOR)

        print("=============EXTRACTING TEXT=============")
        text = str(extract_text(pipeline, [img_arr]))
        print(f"=============TEXT EXTRACTED: {text}=============")

        print("=============DETERMINING PATH=============")

        if img_data:
            # try:
            startRoom = text
            print(startRoom)
            endRoom = roomNumber
            pos1 = findCoordinates(startRoom)
            print(pos1)

            xStart = int(pos1[0])
            yStart = int(pos1[1])
            floor = int(pos1[2])
            pos2 = findCoordinates(endRoom)
            xEnd = int(pos2[0])
            yEnd = int(pos2[1])

            img = None

            if floor == 3:
                img = Image.open("static/goodFloor3.png")
            elif floor == 4:
                img = Image.open("static/goodFloor4.png")
            print(xStart, yStart, 'nums', xEnd, yEnd)

            loadedImg = np.array(img)
            start_point = (yStart, xStart)
            end_point = (yEnd, xEnd)

            img_str = pathfind(loadedImg, start_point, end_point, pipeline)
            print("=============FINISHED PATH=============")
            print(f"Total Runtime: {time.time()-now}s")

            return img_str

        # except Exception as e:
        #     print(f"Error: {e}")
        #     return render_template("index.html", error=True)
        else:
            return "Noneee"

    return app


if __name__ == '__main__':

    pipeline = keras_ocr.pipeline.Pipeline()
    create_app().run(host="0.0.0.0", port=8080)
    # app.run(host="0.0.0.0", port=8080, debug=True)
    # app.run()
