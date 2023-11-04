import base64
import io

import matplotlib
from pytesseract import pytesseract
from PIL import Image
import keras_ocr
import matplotlib.pyplot as plt



from image_analysis import *

def extract_text(pipeline, img):

    # Get a set of three example images



    # Each list of predictions in prediction_groups is a list of
    # (word, box) tuples.
    prediction_groups = pipeline.recognize(img)
    pc = prediction_groups[0]

    for text, box in pc:
        if text.isnumeric():
            return text


def pathfind(loadedImg, start_point, end_point, pipeline):
    # start_point = (137, 281)
    # end_point = (430, 390)

    path = astar(loadedImg, start_point, end_point)
    new_image = draw_path(loadedImg, path)
    rgb_img = new_image.convert('RGB')
    buffer = io.BytesIO()
    rgb_img.save(buffer, format="JPEG")
    img_b64 = base64.b64encode(buffer.getvalue())

    return img_b64

