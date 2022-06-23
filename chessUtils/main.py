# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import math
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
databaseName = "chessGames"
collectionName = "lichess"

db = client[databaseName]
collection = db[collectionName]


b64 = {
    "A": 0, "B": 1, "C": 2, "D": 3, "E": 4, "F": 5, "G": 6, "H": 7, "I": 8, "J": 9, "K": 10, "L": 11, "M": 12, "N": 13,
    "O": 14, "P": 15, "Q": 16, "R": 17, "S": 18, "T": 19, "U": 20, "V": 21, "W": 22, "X": 23, "Y": 24, "Z": 25,
    "a": 26, "b": 27, "c": 28, "d": 29, "e": 30, "f": 31, "g": 32, "h": 33, "i": 34, "j": 35, "k": 36, "l": 37, "m": 38,
    "n": 39, "o": 40, "p": 41, "q": 42, "r": 43, "s": 44, "t": 45, "u": 46, "v": 47, "w": 48, "x": 49, "y": 50, "z": 51,
    "0": 52, "1": 53, "2": 54, "3": 55, "4": 56, "5": 57, "6": 58, "7": 59, "8": 60, "9": 61, "+": 62, "/": 63
}


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    path = "/media/ekrem/Helium/lichess_files/8_2021/data"
    f = open(path, "r")
    toWrite = open("/home/ekrem/Documents/projects/engine/chessUtils/currentRead", "w")
    gameLimit = 10
    gameCount = 0
    infinite = True
    dismissedCount = 0
    currentGame = {}
    # lines = []
    line = f.readline().strip()
    # lines.append(line+"\n")
    lineNumber = 1
    skip = False
    gameList = []
    while infinite or gameCount < gameLimit:
        currentGame = {}
        moves = ""
        skip = False
        me = False
        exitCond = False
        whiteRating = 0
        blackRating = 0
        while line[0:1] != "[":
            # print("first", line, gameCount)
            line = f.readline().strip()
            lineNumber += 1
        while line[0:1] == "[" and not skip:
            # print("second", line, gameCount)
            spaceIndex = line.find(" ")
            label = line[1:spaceIndex]
            value = line[spaceIndex: -1][2:-1]
            if label == "Termination" and value not in ["Time forfeit", "Normal"]:
                skip = True
            elif label in ["WhiteElo", "BlackElo", "WhiteRatingDiff", "BlackRatingDiff"]:
                value = int(value)
            elif label in ["White", "Black"] and value == "rumofek":
                me = True
            if label == "WhiteElo":
                whiteRating = value
            elif label == "BlackElo":
                blackRating = value
            if whiteRating != 0 and blackRating != 0:
                currentGame["AvgRating"] = (whiteRating + blackRating) // 2
                currentGame["RatingDiff"] = abs(whiteRating - blackRating)
            currentGame[label] = value
            # print(label, value)
            line = f.readline().strip()
            lineNumber += 1
            # lines.append(line+"\n")
        while line == "" and not skip:
            # print("second", line, gameCount)
            line = f.readline().strip()
            lineNumber += 1
            # lines.append(line+"\n")
        while line.find(".") > -1 and not skip:
            # print("third", line, gameCount)
            moves += line
            line = f.readline().strip()
            lineNumber += 1
            # lines.append(line+"\n")
        currentGame["pgn"] = moves
        beforeFourth = 0
        while line == "" and not skip:
            if beforeFourth == 2:
                exitCond = True
                break
            # print("fourth", line, gameCount)
            line = f.readline().strip()
            lineNumber += 1
            beforeFourth += 1
            # lines.append(line+"\n")
        if not skip:
            toIterate = currentGame["pgn"].split()
            moveList = ""
            for move in toIterate:
                if not any(val2 in move for val2 in [".", "[", "]", "{", "}"]):
                    moveList += move + " "
            moveCount = int(math.ceil((len(moveList.split()) - 1) / 2))
            currentGame["moves"] = moveList
            currentGame["moveCount"] = moveCount

            if moveCount > 4:
                gameCount += 1
                timeControl = currentGame["TimeControl"].split("+")
                currentGame["Increment"] = int(timeControl[1]) if len(timeControl) > 1 else 0
                currentGame["BaseTime"] = int(timeControl[0]) if timeControl[0] != "-" else -1
                currentGame["Source"] = "lichess"
                gameList.append(currentGame)
                if len(gameList) > 10000:
                    collection.insert_many(gameList)
                    gameList = []
                    print("inserted")

            else:
                dismissedCount += 1
            # if me:
            #     print(gameCount, currentGame)
            if gameCount % 100000 == 0:
                print(gameCount, dismissedCount, gameCount + dismissedCount)
        if exitCond:
            break
    # for i in range(30):
    #     line = f.readline().strip()
    #     if line != "":
    #         print(i, line)
    # toWrite.writelines(lines)
    if len(gameList) > 0:
        collection.insert_many(gameList)
    print("done")
    print(gameCount, dismissedCount)
    f.close()
    toWrite.close()
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
