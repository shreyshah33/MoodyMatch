from mood import moodDetector
import os
import json

for root, dirs, files in os.walk("./testJson"):
    for filename in files:
        with open("./testJson/" + filename) as file:
            data = json.load(file)
            print(filename)
            print(moodDetector(data))
