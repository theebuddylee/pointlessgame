import tkinter as tk
from tkinter.ttk import *
import time
import math
import random

def setMaxProgress():
    global value_progress
    global value_string
    global answer_string
    global s
    value_progress.set(100)
    value_string.set("100")
    answer_string.set("")
    s.configure("score.Vertical.TProgressbar", foreground='blue', background='blue')
    

def countDown(stopPoint):
    global value_string
    progress = value_progress.get()
    value_string.set(str(progress))
    if progress != stopPoint:
        progressbar.step(-1)
        window.after(75, lambda: countDown(stopPoint))

def wrongAnswer():
    global value_string
    s.configure("score.Vertical.TProgressbar", foreground='red', background='red')
    value_string.set("X")
    

def checkAnswer(answers, answer):
    answer = answer.lower()
    time.sleep(2)
    if answer in answers:
        countDown(answers[answer])
    else:
        wrongAnswer()


def eliminateLowestTeam():
    global teams
    minScore = (math.inf, -1)
    for key, team in teams.items():
        print(team)
        score = team["score"].get()
        if score < minScore[0]:
            minScore = (score, key)

    teams[minScore[1]]["eliminated"] = True
    teams[minScore[1]]["teamFrame"].configure(highlightbackground="red")


def placeTeamWidget(frame, teamNumber):
    rowNum = teamNumber // 3
    colNum = teamNumber % 3
    # print(f"row: {rowNum}, col: {colNum}")
    frame.grid(column=colNum, row=rowNum, pady=8, padx=8, sticky='nsew')


def addTeam():
    global teamName_string
    global teams
    teamName = teamName_string.get()
    teamNumber = len(teams)
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
        if not team["eliminated"]:
            team["score"].set(0)


def startGame():
    return None


answers = {"red": 57, "green": 24, "yellow": 9, "white": 4}
data = {
    1: {},
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

value_progress = tk.IntVar()
value_string = tk.StringVar()
answer_string = tk.StringVar()
teamName_string = tk.StringVar()
teams = {}


barFrame = tk.Frame(window, highlightbackground="red", highlightthickness=2)
barFrame.grid(row=0, column=1, pady=8, padx=8, sticky='nsew')

textFrame = tk.Frame(window, highlightbackground="green", highlightthickness=2)
textFrame.grid(row=0, column=0, pady=8, padx=8, sticky='nsew')

teamFrame = tk.Frame(window, highlightbackground="blue", highlightthickness=2)
teamFrame.grid(row=1, column=0, columnspan=2, pady=8, padx=8, sticky='nsew')

teamFrame.columnconfigure(0, weight=1)
teamFrame.columnconfigure(1, weight=1)

teamBoxesFrame = tk.Frame(teamFrame, highlightbackground="yellow", highlightthickness=2)
teamBoxesFrame.grid(row=2, column=0, columnspan=2, pady=8, padx=8, sticky='nsew')
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

buttonEliminateTeam = tk.Button(teamFrame, text="Eliminate Team", command=eliminateLowestTeam)
buttonEliminateTeam.grid(column=1, row=1, pady=8, padx=8)

window.mainloop()
