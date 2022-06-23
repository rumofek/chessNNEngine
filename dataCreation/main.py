from pymongo import MongoClient
from UCIMoveGeneration import generateUCIMoves
import io
import chess
import chess.pgn

client = MongoClient('localhost', 27017)
dbName = "chessGames"
colName = "lichess"
db = client[dbName]
collec = db[colName]
# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

ratingRange = [2200, 2900]
timeFormat = 60 * 3
ratingDiffMax = 50
moveCountMin = 20

# Press the green button in the gutter to run the script.

if __name__ == '__main__':

    movesList = generateUCIMoves()

    toWrite = open("/home/ekrem/Documents/projects/engine/dataCreation/testingMax.txt", "w")
    docs = collec.find(
        {"AvgRating": {"$gt": ratingRange[0], "$lt": ratingRange[1]},
         "BaseTime": {"$gt": timeFormat, "$lt": timeFormat + 7 * 60},
         "moveCount": {"$gt": moveCountMin}, "RatingDiff": {"$lt": ratingDiffMax}}).limit(1000000).max_await_time_ms(5 * 60000)
    count = 0
    for doc in docs:
        count += 1
        pgn = io.StringIO(doc["pgn"])
        game = chess.pgn.read_game(pgn)
        uciMoveList = []
        for move in game.mainline_moves():
            uciMoveList.append((str(move), movesList.index(move.__str__())))
        toWrite.write(str(uciMoveList) + "\n")
        if count % 10000 == 0:
            print(count)

    # count = 0
    # for doc in docs:
    #     count += 1
    #     print(count, doc)
    toWrite.close()
