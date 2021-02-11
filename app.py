import streamlit as st
import requests
import base64
import io
from PIL import Image
import glob
from base64 import decodebytes
from io import BytesIO
import json
import copy

st.write('# Welcome to Diva :princess:')

st.write('### Your number one confidant, always')

user_input = st.text_input("Which of my photos looks most like :", "a good looking person")

uploaded_files = st.sidebar.file_uploader('Drop the images you would like to compare here.',
                                         type=['png', 'jpg', 'jpeg'],
                                         accept_multiple_files=True)

## Convert and display image.
if len(uploaded_files) > 0:
    display_images = []
    for uploaded_file in uploaded_files:
        image = Image.open(uploaded_file)
        buffered = io.BytesIO()
        image_rgb = image.convert("RGB")
        image_rgb.save(buffered, quality=90, format="JPEG")
        img_str = base64.b64encode(buffered.getvalue())
        img_str = img_str.decode("ascii")

        url = 'https://muemnvy0si.execute-api.us-east-2.amazonaws.com/Prod/infer/'
        headers = {
            "Content-Type": "text/plain"
        }
        data = json.dumps({
            "image": img_str,
            "prompt": "a photo of " + user_input,
        })

        r = requests.post(url,
                      data=data,
                      headers=headers
        )

        sim = r.json()["similarity"]
        display_images.append({"image": copy.deepcopy(image), "sim": sim})

    display_images = sorted(display_images, key=lambda k: k['sim'], reverse=True)

    for i, im in enumerate(display_images):
        rank = i + 1

        st.image(im["image"],
             caption="Rank " + str(rank) + " Sim " + str(im['sim']),
             use_column_width=True)
    uploaded_files = []
