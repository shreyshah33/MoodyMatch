from google.cloud import vision
from google.cloud.vision import types
import os

# Adding the env variable of the credentials for the API
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "./key.json"

client = vision.ImageAnnotatorClient()


def detect_face(content):
    # reading image
    image = types.Image(content=content)

    # processing image via GCP API
    data = client.face_detection(
        image=image, max_results=1).face_annotations

    emotions = {}
    if len(data) >= 1:
        emotions = {
            "joy": int(data[0].joy_likelihood),
            "surprise": int(data[0].surprise_likelihood),
            "angry": int(data[0].anger_likelihood),
            "sorrow": int(data[0].sorrow_likelihood)
        }
    return emotions
