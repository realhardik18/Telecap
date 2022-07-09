from flask import Flask, render_template, request, Response
import cv2
from frames import get_frames
import json

app = Flask('')
camera = cv2.VideoCapture(0)

'''
def get_frames():
    while True:
        gotten_frame, frame = camera.read()
        if not gotten_frame:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
        yield(b'--frame\r\n'
              b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
'''


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/profiles')
def profiles():
    f = open("profiles.json", "r")
    data = f.read()
    jsonObj = json.loads(data)
    return render_template("profiles.html", data=jsonObj['users'])


@app.route('/tracking')
def tracking():
    return Response(get_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


app.run()

# todo
# work on showing vdieo in website part nicely with ui
# work on time database system
