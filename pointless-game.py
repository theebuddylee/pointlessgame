import tkinter as tk
from tkinter.ttk import *
import time
import math
import random
import json


questionDir = "D:/Programming/Python Programs/pointless/data/questions/"
roundFileNames = [
    "round-1-answers.json",
    "round-2-answers.json",
    "round-3-answers.json",  # Maybe delete this round based on number of teams taking part
    "round-4-answers.json"
]
h2hFileNames = [
    "h2h-round-1.json",
    "h2h-round-2.json",
    "h2h-round-3.json",
    "h2h-round-4.json",
    "h2h-round-5.json",
    "h2h-round-6.json",
    "h2h-round-7.json"
]
jackpotFileNames = [
    "jackpot-option-1.json",
    "jackpot-option-2.json",
    "jackpot-option-3.json",
    "jackpot-option-4.json",
    "jackpot-option-5.json"
]


def loadQuestionJSON(filename, round):
    global data
    # Opens json file and sets jsonData to a dict of the data in the file
    with open(filename, 'r') as file:
        jsonData = json.load(file)
        data[round] = jsonData
        print(jsonData)
    file.close()


def loadAllQuestions():
    global data
    global roundFileNames
    global h2hFileNames
    global jackpotFileNames
    global jackpotRound
    global h2hRound

    round = 0

    for i in range(len(roundFileNames)):
        round += 1
        loadQuestionJSON(questionDir + roundFileNames[i], round)
    h2hRound = round + 1
    for i in range(len(h2hFileNames)):
        round += 1
        loadQuestionJSON(questionDir + h2hFileNames[i], round)
    jackpotRound = round + 1
    round += 1
    data[round] = {
        "type": "jackpotIntro",
        "topic": "Jackpot Round",
        "topics": []
    }
    for i in range(len(jackpotFileNames)):
        round += 1
        loadQuestionJSON(questionDir + jackpotFileNames[i], round)
        data[jackpotRound]["topics"].append(data[round]["topic"])


def getRoundAnswers():
    global data
    global roundData

    if roundData["type"] == "guess":
        return roundData["answers"]


def setMaxProgress(initial=False):
    global value_progress
    global value_string
    global answer_string
    global s
    global reset_flag
    global barFrame

    reset_flag = True
    
    value_progress.set(100)
    value_string.set("100")
    answer_string.set("")
    s.configure("score.Vertical.TProgressbar", foreground='blue', background='blue')
    barFrame.configure(highlightbackground="red")

    if not initial:
        global redLineFrame
        global redLineLabel
        global buttonS
        redLineFrame.place_forget()
        redLineLabel.place_forget()
        buttonS["state"] = "normal"
    

def nextTeam():
    global currentTeam
    global teams
    global teamDirection

    print(f"Before: {currentTeam}")
    print(len(teams))

    if teams[currentTeam]["out"]:
        teams[currentTeam]["teamFrame"].configure(highlightbackground="red")
    else:
        teams[currentTeam]["teamFrame"].configure(highlightbackground="blue")

    while True:
        if teamDirection == "asc":
            if currentTeam < len(teams) - 1:
                currentTeam += 1
            else:
                teamDirection = "desc"
        else:
            if currentTeam > 0:
                currentTeam -= 1
            else:
                teamDirection = "asc"
        if not teams[currentTeam]["out"]:
            break
    
    print(f"After: {currentTeam}")
    teams[currentTeam]["teamFrame"].configure(highlightbackground="yellow")


def setScore(score, nextTeamFlag):
    global teams
    scoreVar = teams[currentTeam]["score"]
    newScore = scoreVar.get() + score
    teams[currentTeam]["score"].set(newScore)
    if nextTeamFlag: nextTeam()


def countDown(stopPoint, nextTeam=True, jackpot=False):
    global value_string
    global reset_flag
    global barFrame

    reset_flag = False
    progress = value_progress.get()
    value_string.set(str(progress))
    if progress != stopPoint:
        progressbar.step(-1)
        if not jackpot:
            window.after(75, lambda: countDown(stopPoint, nextTeam, jackpot))
        else:
            window.after(125, lambda: countDown(stopPoint, nextTeam, jackpot))
    else:
        if stopPoint == 0:
            barFrame.configure(highlightbackground="green")
        setScore(stopPoint, nextTeam)


def wrongAnswer(nextTeam=True):
    global value_string
    s.configure("score.Vertical.TProgressbar", foreground='red', background='red')
    value_string.set("X")
    setScore(100, nextTeam)
    

def checkAnswer(answers, answer):
    global teams
    global buttonS
    print(answers)

    answer = answer.lower()
    time.sleep((random.random()*1.5 + 1))
    buttonS["state"] = "disabled"
    answersFiltered = [a for a in answers if a["answer"] == answer]
    if len(answersFiltered) == 1:
        countDown(answersFiltered[0]["points"])
    else:
        wrongAnswer()


def findRedLineValue():
    global redLine_string

    highestScore = (0, -1)
    for key, team in teams.items():
        print(team)
        print(highestScore)
        if not team["out"]:
            print(team["score"].get() > highestScore[0])
            if team["score"].get() > highestScore[0]:
                highestScore = (team["score"].get(), key)
    if not highestScore[1] == currentTeam:
        redLine_string.set(str(highestScore[0] - 1 - teams[currentTeam]["score"].get()))
        return highestScore[0] - 1 - teams[currentTeam]["score"].get()
    else:
        redLine_string.set("None")
        return None


def placeRedLine():
    global redLineFrame
    global progressbar

    window.update()

    value = findRedLineValue()
    if value is not None:
        # Adding 3px to this to account for borders
        yVal = progressbar.winfo_y() + (((100 - value) / 100) * progressbar.winfo_height()) + 3
        print(progressbar.winfo_y(), progressbar.winfo_height())
        print(value, yVal)
        redLineFrame.place(relx=0.2, y=yVal, relwidth=0.7)
        redLineLabel.place(relx=0.05, y=(yVal - 10))



def eliminateHighestTeam():
    global teams
    maxScore = (math.inf * -1, -1)
    for key, team in teams.items():
        print(team)
        score = team["score"].get()
        if score > maxScore[0]:
            maxScore = (score, key)
        team["score"].set(0)

    eliminateTeam(maxScore[1])


def eliminateTeam(teamIndex):
    global teams
    teams[teamIndex]["out"] = True
    teams[teamIndex]["teamFrame"].configure(highlightbackground="red")


def placeTeamWidget(frame, teamNumber):
    rowNum = teamNumber // 3
    colNum = teamNumber % 3
    # print(f"row: {rowNum}, col: {colNum}")
    frame.grid(column=colNum, row=rowNum, pady=8, padx=8, sticky='nsew')


def addTeam():
    global teamName_string
    global teams
    global currentTeam

    teamName = teamName_string.get()
    teamNumber = len(teams)

    if currentTeam == -1:
        currentTeam = teamNumber

    teams[teamNumber] = {"name": teamName, "score": tk.IntVar(), "h2hScore": tk.IntVar(), "teamFrame": None, "teamScoreElement": None, "out": False}
    teamBoxFrame = tk.Frame(teamBoxesFrame, highlightbackground="blue", highlightthickness=2)
    placeTeamWidget(teamBoxFrame, teamNumber)
    teamBoxLabel = tk.Label(teamBoxFrame, text=teamName)
    teamBoxLabel.pack()
    teamScoreLabel = tk.Label(teamBoxFrame, textvariable=teams[teamNumber]["score"])
    teamScoreLabel.pack()
    teamH2HScoreLabel = tk.Label(teamBoxFrame, textvariable=teams[teamNumber]["h2hScore"])
    teamH2HScoreLabel.pack()
    teams[teamNumber]["teamFrame"] = teamBoxFrame
    teams[teamNumber]["teamScoreElement"] = teamBoxFrame


def checkH2HAnswer(answer, entry, points):
    print(answer, entry, points)
    time.sleep((random.random() * 1.5 + 1))
    if answer == entry.lower():
        countDown(points)
    else:
        wrongAnswer()


def createClueObject(clueObjects, index, entryVars):
    global data
    global round_number
    global question_string

    questions = data[round_number]["questions"]
    clueObjects[index] = {"frame": None, "label": None, "entry": None, "button": None, "buttonFunc": lambda: checkH2HAnswer(questions[index]["answer"], clueObjects[index]["entry"].get(), questions[index]["points"])}
    clueFrame = tk.Frame(textFrame, highlightbackground="purple", highlightthickness=2)
    clueFrame.pack(fill="both", expand=True)
    clueLabel = tk.Label(clueFrame, text=questions[index]["clue"])
    clueLabel.pack()
    clueEntry = tk.Entry(clueFrame, textvariable=entryVars[index])
    clueEntry.pack()
    clueButton = tk.Button(clueFrame, text="Submit", command=clueObjects[index]["buttonFunc"])
    clueButton.pack()
    clueObjects[index]["frame"] = clueFrame
    clueObjects[index]["label"] = clueLabel
    clueObjects[index]["entry"] = clueEntry
    clueObjects[index]["button"] = clueButton
    return clueObjects


def displayClues():
    global data
    global round_number
    global question_string
    global clueObjects

    question_string.set(data[round_number]["question"])
    questions = data[round_number]["questions"]
    entryVars = [tk.StringVar() for i in range(len(questions))]
    clueObjects = {}
    for i in range(len(questions)):
        clueObjects = createClueObject(clueObjects, i, entryVars)
    return None


def scoreH2HRound():
    global teams
    global data

    lowestScore = (math.inf, -1)
    for key, team in teams.items():
        if not team["out"]:
            if team["score"].get() < lowestScore[0]:
                lowestScore = (team["score"].get(), key)
            team["score"].set(0)
    teams[lowestScore[1]]["h2hScore"].set(teams[lowestScore[1]]["h2hScore"].get() + 1)

    # Eliminate other teams if a team gets 3 h2h wins
    if teams[lowestScore[1]]["h2hScore"].get() == 3:
        for key, team in teams.items():
            if key != lowestScore[1]:
                eliminateTeam(key)


def checkJackpotAnswer(answer):
    answers = []
    for question in roundData["questions"]:
        answers.extend(question["answers"])
    answersFiltered = [a for a in answers if a["answer"] == answer]
    time.sleep((random.random() * 1.5 + 1))
    if len(answersFiltered) == 1:
        countDown(answersFiltered[0]["points"], jackpot=True)
    else:
        wrongAnswer()
    return None


def createJackpotEntryObject(index, entryVars):
    global jackpotEntryObjects
    global jackpotEntryFrame

    jackpotEntryObjects[index] = {"entry": None, "button": None, "buttonFunc": lambda: checkJackpotAnswer(jackpotEntryObjects[index]["entry"].get())}
    jackpotEntryEntry = tk.Entry(textFrame, textvariable=entryVars[index])
    jackpotEntryEntry.pack()
    jackpotEntryButton = tk.Button(textFrame, text="Submit", command=jackpotEntryObjects[index]["buttonFunc"])
    jackpotEntryButton.pack()
    jackpotEntryObjects[index]["entry"] = jackpotEntryEntry
    jackpotEntryObjects[index]["button"] = jackpotEntryButton

    return jackpotEntryObjects


def displayJackpot():
    global question_string
    global jackpotEntryObjects
    print("jackpot")

    question_string.set(data[round_number]["topic"])
    for question in data[round_number]["questions"]:
        questionLabel = tk.Label(textFrame, text=question["question"])
        questionLabel.pack()

    jackpotEntryVars = [tk.StringVar() for i in range(3)]
    for i in range(3):
        jackpotEntryObjects = createJackpotEntryObject(i, jackpotEntryVars)



def offsetRoundNumber(offset):
    global round_number
    global jackpotIntroElements
    print("offsetRoundNumber")

    offset = int(offset)
    round_number += offset
    for element in jackpotIntroElements:
        element.pack_forget()

    startRound(round_number)


def displayJackpotIntro():
    global question_string
    global data
    global jackpotIntroElements

    print("displayJackpotIntro")
    print(data[round_number])

    question_string.set(data[round_number]["topic"])
    for topic in data[round_number]["topics"]:
        print(topic)
        topicLabel = tk.Label(textFrame, text=topic)
        jackpotIntroElements.append(topicLabel)
        topicLabel.pack()

    roundOffset = tk.StringVar()
    topicChoice = tk.Entry(textFrame, textvariable=roundOffset)
    topicChoice.pack()
    topicButton = tk.Button(textFrame, text="Submit", command=lambda: offsetRoundNumber(roundOffset.get()))
    topicButton.pack()
    jackpotIntroElements.append(topicChoice)
    jackpotIntroElements.append(topicButton)


def displayQuestionText():
    global question_string
    global roundType
    global labelAnswer
    global answerField
    global buttonS

    if roundType == "guess":
        question_string.set(data[round_number]["question"])
        labelAnswer.pack()
        answerField.pack()
        buttonS.pack()
    elif roundType == "h2h":
        displayClues()
    elif roundType == "jackpot":
        displayJackpot()
    else:
        displayJackpotIntro()


def nextRound():
    global labelAnswer
    global answerField
    global buttonS
    global clueObjects
    global round_number

    labelAnswer.pack_forget()
    answerField.pack_forget()
    buttonS.pack_forget()
    for key, clueObject in clueObjects.items():
        clueObject["frame"].pack_forget()
        clueObject["label"].pack_forget()
        clueObject["entry"].pack_forget()
        clueObject["button"].pack_forget()

    round_number += 1
    startRound(round_number)

    return None


def endRound():
    return None


def startJackpot():
    global round_number
    print("startJackpot")

    labelAnswer.pack_forget()
    answerField.pack_forget()
    buttonS.pack_forget()
    for key, clueObject in clueObjects.items():
        clueObject["frame"].pack_forget()
        clueObject["label"].pack_forget()
        clueObject["entry"].pack_forget()
        clueObject["button"].pack_forget()

    round_number = jackpotRound
    print(data[round_number])
    startRound(round_number)
    return None


def startRound(roundNumber):
    global teams
    global roundType
    global roundData
    print("startRound", roundNumber)

    setMaxProgress()

    for _, team in teams.items():
        if not team["out"]:
            team["score"].set(0)
        
    question_string.set(data[roundNumber]["topic"])
    roundType = data[roundNumber]["type"]
    roundData = data[roundNumber]


def startGame():
    global teams
    global round_number
    global buttonAddTeam
    print(currentTeam)

    buttonAddTeam["state"] = "disabled"

    if currentTeam in teams.keys():
        teams[currentTeam]["teamFrame"].configure(highlightbackground="yellow")
    
    round_number = 1
    startRound(round_number)

    return None


data = {}

window = tk.Tk()
window.geometry("1000x800")

window.columnconfigure(0, weight=1)
window.columnconfigure(1, weight=1)
window.columnconfigure(2, weight=1)

# region variable-initialisation
value_progress = tk.IntVar()
value_string = tk.StringVar()
answer_string = tk.StringVar()
teamName_string = tk.StringVar()
redLine_string = tk.StringVar()
question_string = tk.StringVar()
reset_flag = tk.BooleanVar()
round_number = 0
teams = {}
teamDirection = "asc"
currentTeam = -1
rounds = 5
h2hBestOf = 3  # How many points to win the head-to-head round
jackpotRound = 0  # Start of jackpot round for jumping straight to it
h2hRound = 0  # Start of head-to-head round for determining question type
roundType = "guess"  # Type of round, guess, h2h, jackpot
roundData = None
clueObjects = {}
jackpotIntroElements = []
jackpotEntries = []
jackpotEntryObjects = {}
# endregion variable-initialisation

loadAllQuestions()

barFrame = tk.Frame(window, highlightbackground="red", highlightthickness=2)
barFrame.grid(row=0, column=1, pady=8, padx=8, sticky='nsew')

textFrame = tk.Frame(window, highlightbackground="green", highlightthickness=2)
textFrame.grid(row=0, column=0, pady=8, padx=8, sticky='nsew')

controlFrame = tk.Frame(window, highlightbackground="black", highlightthickness=2)
controlFrame.grid(row=0, column=2, pady=8, padx=8, sticky='nsew')
controlFrame.columnconfigure(0, weight=1)
controlFrame.columnconfigure(1, weight=1)
controlFrame.rowconfigure(0, weight=1)
controlFrame.rowconfigure(1, weight=1)
controlFrame.rowconfigure(2, weight=1)
controlFrame.rowconfigure(3, weight=1)
controlFrame.rowconfigure(4, weight=1)
controlFrame.rowconfigure(5, weight=1)

teamFrame = tk.Frame(window, highlightbackground="blue", highlightthickness=2)
teamFrame.grid(row=1, column=0, columnspan=2, pady=8, padx=8, sticky='nsew')

teamFrame.columnconfigure(0, weight=1)
teamFrame.columnconfigure(1, weight=1)

teamBoxesFrame = tk.Frame(teamFrame)
teamBoxesFrame.grid(row=3, column=0, columnspan=2, pady=8, padx=8, sticky='nsew')
teamBoxesFrame.columnconfigure(0, weight=1)
teamBoxesFrame.columnconfigure(1, weight=1)
teamBoxesFrame.columnconfigure(2, weight=1)

labelProgress = tk.Label(barFrame, textvariable=value_string)
labelProgress.pack()

s = Style()
s.theme_use('clam')
s.configure("score.Vertical.TProgressbar", foreground='blue', background='blue')

setMaxProgress(initial=True)

progressbar = Progressbar(barFrame, orient=tk.VERTICAL,
                          length=400, mode="determinate",
                          variable=value_progress,value=100,
                          style="score.Vertical.TProgressbar"
                          )
progressbar.pack(ipadx=30)

redLineFrame = tk.Frame(barFrame, background="red", height=1)
redLineLabel = tk.Label(barFrame, textvariable=redLine_string)

buttonReset = tk.Button(barFrame, text="Reset", command=setMaxProgress)
buttonReset.pack(padx=8, pady=8)

labelQuestion = tk.Label(textFrame, textvariable=question_string)
labelQuestion.pack()

labelAnswer = tk.Label(textFrame, text="Answer")
answerField = tk.Entry(textFrame, textvariable=answer_string, width=30)
buttonS = tk.Button(textFrame, text="Check Answer", command=lambda: checkAnswer(getRoundAnswers(), answer_string.get()))

buttonDisplayQuestion = tk.Button(controlFrame, text="Display Question", command=displayQuestionText)
buttonDisplayQuestion.grid(row=0, column=1, padx=8, pady=8)

teamEntry = tk.Entry(teamFrame, textvariable=teamName_string, width=40)
teamEntry.grid(column=0, row=0, pady=8, padx=8)

buttonAddTeam = tk.Button(teamFrame, text="Add Team", command=addTeam)
buttonAddTeam.grid(column=0, row=1, pady=8, padx=8)

buttonStartGame = tk.Button(controlFrame, text="Start Game", command=startGame)
buttonStartGame.grid(column=0, row=0, pady=8, padx=8)

buttonEliminateTeam = tk.Button(controlFrame, text="Eliminate Team", command=eliminateHighestTeam)
buttonEliminateTeam.grid(column=0, row=1, pady=8, padx=8)

buttonDisplayRedLine = tk.Button(controlFrame, text="Display Red Line", command=placeRedLine)
buttonDisplayRedLine.grid(column=0, row=2, pady=8, padx=8)

buttonChooseRound = tk.Button(controlFrame, text="Next Round", command=nextRound)
buttonChooseRound.grid(column=0, row=3, pady=8, padx=8)

buttonStartJackpot = tk.Button(controlFrame, text="Start Jackpot", command=startJackpot)
buttonStartJackpot.grid(column=0, row=4, pady=8, padx=8)

buttonEndRound = tk.Button(controlFrame, text="End Round", command=endRound)
buttonEndRound.grid(column=0, row=5, pady=8, padx=8)

buttonScoreH2HRound = tk.Button(controlFrame, text="Score H2H Round", command=scoreH2HRound)
buttonScoreH2HRound.grid(column=1, row=1, pady=8, padx=8)

buttonNextTeam = tk.Button(controlFrame, text="Next Team", command=nextTeam)
buttonNextTeam.grid(column=1, row=2, pady=8, padx=8)

window.update()
print(progressbar.winfo_width(), progressbar.winfo_x())
print(progressbar.winfo_height(), progressbar.winfo_y())
print(progressbar.winfo_geometry())

window.mainloop()


