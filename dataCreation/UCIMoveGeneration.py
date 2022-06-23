letters = "abcdefgh"
MAXCOL = 8
def generateUCIMoves():
    # rookMoves
    movesList = []
    for startPosX in range(MAXCOL):
        for startPosY in range(MAXCOL):
            toAdd = letters[startPosX:startPosX + 1] + str(startPosY + 1)
            for endPos in range(MAXCOL):
                if endPos != startPosX:
                    toAddX = toAdd + letters[endPos:endPos + 1] + str(startPosY + 1)
                    movesList.append(toAddX)
                if endPos != startPosY:
                    toAddY = toAdd + letters[startPosX:startPosX + 1] + str(endPos + 1)
                    movesList.append(toAddY)
    # bishopMoves
    for startPosX in range(MAXCOL):
        for startPosY in range(MAXCOL):
            toAdd = letters[startPosX:startPosX + 1] + str(startPosY + 1)
            for endPos in range(startPosX):
                diff = endPos - startPosX
                if not (startPosY + diff < 0):
                    toAddBefore = toAdd + letters[startPosX + diff: startPosX + 1 + diff] + str(startPosY + diff + 1)
                    movesList.append(toAddBefore)
                if startPosY - diff > 7:
                    continue
                toAddBefore = toAdd + letters[startPosX + diff: startPosX + 1 + diff] + str(startPosY - diff + 1)
                movesList.append(toAddBefore)
            for endPos in range(startPosX + 1, MAXCOL):
                diff = endPos - startPosX
                if not (startPosY + diff > 7):
                    toAddBefore = toAdd + letters[startPosX + diff: startPosX + 1 + diff] + str(startPosY + diff + 1)
                    movesList.append(toAddBefore)
                if startPosY - diff < 0:
                    continue
                toAddBefore = toAdd + letters[startPosX + diff: startPosX + 1 + diff] + str(startPosY - diff + 1)
                movesList.append(toAddBefore)
    # knightMoves
    knightMoves = [(1, 2), (1, -2), (-1, 2), (-1, -2), (2, 1), (2, -1), (-2, 1), (-2, -1)]
    for startPosX in range(MAXCOL):
        for startPosY in range(MAXCOL):
            toAdd = letters[startPosX:startPosX + 1] + str(startPosY + 1)
            for move in knightMoves:
                endX = startPosX + move[0]
                endY = startPosY + move[1]
                if 0 <= endX < 8 and 0 <= endY < 8:
                    toAddAfter = toAdd + letters[endX:endX + 1] + str(endY + 1)
                    movesList.append(toAddAfter)
    # pawnPromotion
    pieces = "bnrq"
    for startPosX in range(MAXCOL):
        toAdd = letters[startPosX:startPosX + 1]
        if startPosX != 0:
            for i in range(len(pieces)):
                piece = pieces[i:i + 1]
                movesList.append(toAdd + "7" + letters[startPosX - 1: startPosX] + "8" + piece)
                movesList.append(toAdd + "2" + letters[startPosX - 1: startPosX] + "1" + piece)
        if startPosX != 7:
            for i in range(len(pieces)):
                piece = pieces[i:i + 1]
                movesList.append(toAdd + "7" + letters[startPosX + 1: startPosX + 2] + "8" + piece)
                movesList.append(toAdd + "2" + letters[startPosX + 1: startPosX + 2] + "1" + piece)
        for i in range(len(pieces)):
            piece = pieces[i:i + 1]
            movesList.append(toAdd + "7" + letters[startPosX: startPosX + 1] + "8" + piece)
            movesList.append(toAdd + "2" + letters[startPosX: startPosX + 1] + "1" + piece)

    # queenMoves unnecessary - queen moves like a bishop or a rook at once
    # kingMoves unnecessary - king moves like a queen that can only move a single square
    # pawnMoves unnecessary - mini bishops/rooks
    return movesList

print(generateUCIMoves())
