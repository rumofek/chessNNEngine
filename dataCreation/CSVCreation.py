import ast
import csv
import chess

gameCount = 600000
toRead = open("/home/ekrem/Documents/projects/engine/dataCreation/testing.txt", "r")
toWrite = open("/home/ekrem/Documents/projects/engine/dataCreation/games2.csv", "w")

csvWriter = csv.writer(toWrite)
# firstLine = toRead.readline().strip()
# print(firstLine)
# print(type(ast.literal_eval(firstLine)))
curGameCount = 0
line = toRead.readline().strip()
csvWriter.writerow(["fen", "expectedMove"])
while not line == "":
    # training on white moves only
    moveList = ast.literal_eval(line)
    # create a csv line for each board position
    board = chess.Board()
    for whiteMoveIdx in range(0, len(moveList), 2):
        whiteMove = moveList[whiteMoveIdx]
        csvLine = []
        fenStr = board.board_fen()
        expectedMove = whiteMove[1]
        csvLine.append(fenStr)
        csvLine.append(expectedMove)
        csvWriter.writerow(csvLine)
        board.push_san(whiteMove[0])
        if not whiteMoveIdx + 1 == len(moveList):
            blackMove = moveList[whiteMoveIdx + 1]
            board.push_san(blackMove[0])
    line = toRead.readline().strip()
    curGameCount += 1
    if curGameCount % 10000 == 0:
        print(curGameCount)
toRead.close()
toWrite.close()
