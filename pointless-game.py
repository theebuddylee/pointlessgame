import tkinter as tk
from tkinter.ttk import *
import time
import math
import random
import json


def loadQuestionJSON(filename, round):
    global data
    # Opens json file and sets jsonData to a dict of the data in the file
    with open(filename, 'r') as file:
        jsonData = json.load(file)
        data[round] = jsonData
    file.close()


def setMaxProgress():
    global value_progress
    global value_string
    global answer_string
    global s
    value_progress.set(100)
    value_string.set("100")
    answer_string.set("")
    s.configure("score.Vertical.TProgressbar", foreground='blue', background='blue')
    

def nextTeam():
    global currentTeam
    global teams
    global teamDirection

    print(f"Before: {currentTeam}")
    print(len(teams))

    teams[currentTeam]["teamFrame"].configure(highlightbackground="blue")

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
    
    print(f"After: {currentTeam}")
    teams[currentTeam]["teamFrame"].configure(highlightbackground="yellow")


def setScore(score):
    global teams
    teams[currentTeam]["score"].set(score)
    nextTeam()


def countDown(stopPoint):
    global value_string
    progress = value_progress.get()
    value_string.set(str(progress))
    if progress != stopPoint:
        progressbar.step(-1)
        window.after(75, lambda: countDown(stopPoint))
    else:
        setScore(stopPoint)

def wrongAnswer():
    global value_string
    s.configure("score.Vertical.TProgressbar", foreground='red', background='red')
    value_string.set("X")
    

def checkAnswer(answers, answer):
    global teams

    answer = answer.lower()
    time.sleep(2)
    if answer in answers:
        countDown(answers[answer])
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
    else:
        redLine_string.set("None")


def eliminateHighestTeam():
    global teams
    maxScore = (math.inf * -1, -1)
    for key, team in teams.items():
        print(team)
        score = team["score"].get()
        if score > maxScore[0]:
            maxScore = (score, key)

    teams[maxScore[1]]["out"] = True
    teams[maxScore[1]]["teamFrame"].configure(highlightbackground="red")


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

    teams[teamNumber] = {"name": teamName, "score": tk.IntVar(), "teamFrame": None, "teamScoreElement": None, "out": False}
    teamBoxFrame = tk.Frame(teamBoxesFrame, highlightbackground="blue", highlightthickness=2)
    print(teamBoxFrame)
    placeTeamWidget(teamBoxFrame, teamNumber)
    teamBoxLabel = tk.Label(teamBoxFrame, text=teamName)
    teamBoxLabel.pack()
    teamScoreLabel = tk.Label(teamBoxFrame, textvariable=teams[teamNumber]["score"])
    teamScoreLabel.pack()
    print(teamBoxFrame)
    teams[teamNumber]["teamFrame"] = teamBoxFrame
    teams[teamNumber]["teamScoreElement"] = teamBoxFrame


def startRound():
    global teams
    for _, team in teams.items():
        if not team["out"]:
            team["score"].set(0)


def startGame():
    global teams
    print(currentTeam)

    if currentTeam in teams.keys():
        teams[currentTeam]["teamFrame"].configure(highlightbackground="yellow")
    return None


answers = {"red": 57, "green": 24, "yellow": 9, "white": 4}
data = {
    1: {
        "question": "",
        "answers": {
            "red": 57,
            "green": 24,
            "yellow": 9,
            "white": 4
        }
    },
    2: {},
    3: {},
    4: {},
    5: {}
}
numberOfTeams = 5

window = tk.Tk()
window.geometry("700x700")

window.columnconfigure(0, weight=1)
window.columnconfigure(1, weight=1)

# region variable-initialisation
value_progress = tk.IntVar()
value_string = tk.StringVar()
answer_string = tk.StringVar()
teamName_string = tk.StringVar()
redLine_string = tk.StringVar()
teams = {}
teamDirection = "asc"
currentTeam = -1
# endregion variable-initialisation

barFrame = tk.Frame(window, highlightbackground="red", highlightthickness=2)
barFrame.grid(row=0, column=1, pady=8, padx=8, sticky='nsew')

textFrame = tk.Frame(window, highlightbackground="green", highlightthickness=2)
textFrame.grid(row=0, column=0, pady=8, padx=8, sticky='nsew')

teamFrame = tk.Frame(window, highlightbackground="blue", highlightthickness=2)
teamFrame.grid(row=1, column=0, columnspan=2, pady=8, padx=8, sticky='nsew')

teamFrame.columnconfigure(0, weight=1)
teamFrame.columnconfigure(1, weight=1)

teamBoxesFrame = tk.Frame(teamFrame, highlightbackground="yellow", highlightthickness=2)
teamBoxesFrame.grid(row=3, column=0, columnspan=2, pady=8, padx=8, sticky='nsew')
teamBoxesFrame.columnconfigure(0, weight=1)
teamBoxesFrame.columnconfigure(1, weight=1)
teamBoxesFrame.columnconfigure(2, weight=1)

labelProgress = tk.Label(barFrame, textvariable=value_string)
labelProgress.pack()

s = Style()
s.theme_use('clam')
s.configure("score.Vertical.TProgressbar", foreground='blue', background='blue')

setMaxProgress()

progressbar = Progressbar(barFrame, orient=tk.VERTICAL,
                          length=400, mode="determinate",
                          variable=value_progress,value=100,
                          style="score.Vertical.TProgressbar"
                          )
progressbar.pack(ipadx=30)

redLineFrame = tk.Frame(barFrame, background="red", height=1)
redLineFrame.place(relx=0.1, rely=0.5, relwidth=1)

redLineLabel = tk.Label(barFrame, textvariable=redLine_string)
redLineLabel.place(relx=0.05, rely=0.5)

buttonReset = tk.Button(barFrame, text="Reset", command=setMaxProgress)
buttonReset.pack()

labelQuestion = tk.Label(textFrame, text="Name a colour on the flag of Suriname")
labelQuestion.pack()

labelAnswer = tk.Label(textFrame, text="Answer")
labelAnswer.pack()

answerField = tk.Entry(textFrame, textvariable=answer_string, width=30)
answerField.pack()

buttonS = tk.Button(textFrame, text="Check Answer", command=lambda: checkAnswer(answers, answer_string.get()))
buttonS.pack()

teamEntry = tk.Entry(teamFrame, textvariable=teamName_string, width=40)
teamEntry.grid(column=0, row=0, pady=8, padx=8)

buttonAddTeam = tk.Button(teamFrame, text="Add Team", command=addTeam)
buttonAddTeam.grid(column=0, row=1, pady=8, padx=8)

buttonStartGame = tk.Button(teamFrame, text="Start Game", command=startGame)
buttonStartGame.grid(column=1, row=0, pady=8, padx=8)

buttonEliminateTeam = tk.Button(teamFrame, text="Eliminate Team", command=eliminateHighestTeam)
buttonEliminateTeam.grid(column=1, row=1, pady=8, padx=8)

buttonDisplayRedLine = tk.Button(teamFrame, text="Display Red Line", command=findRedLineValue)
buttonDisplayRedLine.grid(column=1, row=2, pady=8, padx=8)

window.update()
print(progressbar.winfo_width(), progressbar.winfo_x())
print(progressbar.winfo_height(), progressbar.winfo_y())
print(progressbar.winfo_geometry())

window.mainloop()


