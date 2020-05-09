from flask import Flask, render_template, request, jsonify, redirect, session
import operator
import re

from image import detect_face
from mood import moodDetector
import api

app = Flask(__name__)

app.secret_key = "NeverGonnaGiveYouUp"


@app.route("/")
def main():
    return render_template("index.html")


@app.route("/gettingstarted")
def getStarted():
    return render_template("survey.html")


@app.route("/survey", methods=["GET", "POST"])
def survey():
    if request.method == "GET":
        return render_template("survey-questions.html")
    elif request.method == "POST":
        form = request.form
        mood = moodDetector(form)
        crowd = int(form["crowd"])
        location = str(form["location"])
        media = str(form["media"])
        mainMood = max(mood.items(), key=operator.itemgetter(1))[0]
        if media != None and media != "":
            if re.match("(.*?),", media) != None:
                media = re.match("(.*?),", media).group()
            gifUrls = api.tenorQuery(media)
            ytUrls = api.youtubeQuery(media + " funny scenes")
        else:
            gifUrls = api.tenorQuery("school memes")
            ytUrls = api.youtubeQuery("funniest videos")
        if mainMood == "joy":
            if location != None and location != "":
                playlistUrl = api.spotifyQuery(location)
            elif crowd > 1 or mood["energy"] > 5:
                playlistUrl = api.spotifyQuery("Happy EDM")
            else:
                playlistUrl = api.spotifyQuery("Happy pop")
        else:
            if location != None and location != "":
                playlistUrl = api.spotifyQuery(location)
            elif crowd > 1 or mood["energy"] > 5:
                playlistUrl = api.spotifyQuery("Uplifting pop")
            else:
                playlistUrl = api.spotifyQuery("Calm uplifting")
        session["playlist"] = playlistUrl
        session["yt"] = ytUrls
        session["gif"] = gifUrls
        session["page"] = "survey"
        return "success"


@app.route("/webcam", methods=["GET", "POST"])
def webcam():
    if request.method == "GET":
        return render_template("webcam.html")
    elif request.method == "POST":
        # getting image from the request
        image = request.files["upimage"].read()

        mood = detect_face(image)
        if mood != None or mood != {}:
            mainMood = max(mood.items(), key=operator.itemgetter(1))[0]
            # gifUrls = api.tenorQuery("school memes")
            # ytUrls = api.youtubeQuery("funniest videos")
            if mainMood == "joy" or mainMood == "surprise":
                if mood["surprise"] > 2:
                    playlistUrl = api.spotifyQuery("Happy EDM")
                else:
                    playlistUrl = api.spotifyQuery("Happy pop")
            else:
                if mood["surprise"] > 2:
                    playlistUrl = api.spotifyQuery("Uplifting pop")
                else:
                    playlistUrl = api.spotifyQuery("Calm uplifting")
            session["playlist"] = playlistUrl
            # session["yt"] = ytUrls
            # session["gif"] = gifUrls
            session["page"] = "webcam"
            return "success"
        return "welp"


@app.route("/results", methods=["GET"])
def results():
    playlistUrl = session["playlist"]
    # print(session)
    page = session["page"]
    if page == "survey":
        ytUrls = session["yt"]
        gifUrls = session["gif"]
        return render_template("results.html", playlistUrl=playlistUrl, ytUrls=ytUrls, gifUrls=gifUrls)
    elif page == "webcam":
        return render_template("results-webcam.html", playlistUrl=playlistUrl)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080)
