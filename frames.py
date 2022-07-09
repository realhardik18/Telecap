# Import required libraries
from keras.models import load_model
from PIL import Image, ImageOps
import numpy as np
import cv2
import time
import json

# Load the Model
model = load_model('TeleCap.h5')

# Input Pre Processing
data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
labels = ["Preetham", "Hardik", "Ananya", "Vedika", "Samyak", "Nobody"]


def imagePreparation(image):
    # resize the image and then cropping from the center
    size = (224, 224)
    image = ImageOps.fit(image, size, Image.ANTIALIAS)
    image_array = np.asarray(image)
    normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1
    data[0] = normalized_image_array


def get_frames():
    output = ""  # Stores output of model
    camera = cv2.VideoCapture(0)
    local_data = {'Preetham': 0,
                  "Hardik": 0, "Ananya": 0, "Vedika": 0, "Samyak": 0}
    while (True):
        # Getting the current frame
        gotten_frame, frame = camera.read()
        if not gotten_frame:
            break
        else:
            img = Image.fromarray(frame)

            # Get the Prediction
            imagePreparation(img)
            prediction = model.predict(data)
            result = np.argmax(prediction[0])
            output = labels[result]

            # Show the Result
            cv2.putText(frame, "Current User: " + output, (0,
                        frame.shape[0] - 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
        if output != 'Nobody':
            print(output, local_data[output])
            with open('profiles.json', 'r+') as f:
                json_data = json.load(f)
                local_data[output] += 1
                if local_data[output] == 10:
                    json_data['users'][labels.index(output)]['total_time'] += 1
                    f.seek(0)
                    json.dump(json_data, f, indent=4)
                    f.truncate()
                    local_data[output] = 0

        yield(b'--frame\r\n'
              b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
# work from here
