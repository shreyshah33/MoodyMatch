import json

with open("./color_data.json") as file:
    colorData = json.load(file)
    colors = colorData["colors"]

with open("./mood_data.json") as file:
    moodData = json.load(file)
    moods = moodData["moods"]
    stressData = moods["stress"]
    joyData = moods["joy"]
    angryData = moods["angry"]
    sadData = moods["sad"]
    energyData = moods["energy"]


def adjectiveMoodScorer(adjectives: list, day: int, hours: int):

    # scale
    happyScale = float(day) * 0.1
    sadScale = float(10 - day) * 0.1

    # stress scale. Can affect upto 50% of the stress score.
    # 50% enabled by dividing by 24 instead of 12
    stressScale = float(1) + float(hours)/float(24)

    stress = 0
    stressCount = 0

    joy = 0
    joyCount = 0

    angry = 0
    angryCount = 0

    sad = 0
    sadCount = 0

    energy = 0
    energyCount = 0

    # scoring
    for adjective in adjectives:
        if adjective in stressData:
            stressCount = stressCount + 1
            stress = stress + stressData[adjective]
        if adjective in joyData:
            joyCount = joyCount + 1
            joy = joy + joyData[adjective]
        if adjective in angryData:
            angryCount = angryCount + 1
            angry = angry + angryData[adjective]
        if adjective in sadData:
            sadCount = sadCount + 1
            sad = sad + sadData[adjective]
        if adjective in energyData:
            energyCount = energyCount + 1
            energy = energy + energyData[adjective]

    # scaling
    stress = round(stress * sadScale * stressScale)
    joy = round(joy * happyScale)
    sad = round(sad * sadScale)
    angry = round(angry * sadScale)

    if joy >= stress and joy >= sad and joy >= angry:
        energy = round(energy * happyScale)
        if energy > joy:
            energy = joy
    else:
        energy = round(energy * sadScale)
        if energy > max(stress, sad, angry):
            energy = max(stress, sad, angry)

    return {"stress": stress, "joy": joy, "sad": sad, "angry": angry, "energy": energy}


def colorAdjectiveExtractor(color: str):
    return colors[color]


def moodDetector(answers: dict):

    # extracting answers
    # answers = jsonData["answers"]
    day = int(answers["day"])
    hoursOfWork = int(answers["hours"])
    rgb = str(answers["color"])
    if rgb != "None":
        color = rgb.replace("rgb(", "")
        color = color.replace(")", "")
        color = (color.split(","))
        hexColor = ""
        for num in color:
            hexColor = hexColor + '%02X' % int(num)
    else:
        hexColor = rgb

    # print(hexColor, rgb)
    adjectives = answers["adjective"].split(",")
    # crowd = int(answers["crowd"])
    # location = str(answers["location"])
    # media = str(answers["media"])

    # getting adjectives from color
    adjectives.extend(colorAdjectiveExtractor(hexColor))

    # adjective scoring
    print(adjectives)
    moodScore = adjectiveMoodScorer(adjectives, day, hoursOfWork)

    return moodScore
