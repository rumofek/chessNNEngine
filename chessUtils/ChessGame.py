import numpy as np


class ChessGame:
    '''
    empty square = 0
    pawn = 1
    knight = 2
    bishop = 3
    rook = 4
    queen = 5
    king = 6
    '''

    def __init__(self):
        self.fen = None
        self.white_to_move = True
        self.board_array = np.asarray(
            [[-4, -2, -3, -5, -6, -3, -2, -4],
             [-1, -1, -1, -1, -1, -1, -1, -1],
             [0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0],
             [1, 1, 1, 1, 1, 1, 1, 1],
             [4, 2, 3, 5, 6, 3, 2, 4]]
        )
        # white first, long first
        self.castling_rights = np.asarray([1, 1, 1, 1])
        self.enpassant_targets = np.array()
        self.move_count = 0

    def move(self, move):
        piece = 1
        capture = False
        pawnMove = False
        if len(move) > 3:
            capture = True
            move = move[0] + move[2:len(move)]
        if len(move) > 2:
            letter = move[0]
            if (letter.isupper()):
                letter = move[0].lower()
                if letter == 'k':
                    piece = 6
                elif letter == 'q':
                    piece = 5
                elif letter == 'r':
                    piece = 4
                elif letter == 'n':
                    piece = 2
                elif letter == 'b':
                    piece = 3
                else:
                    return False
            else:
                pawmMove = True
                                                                                                                                                          
        return False

    def set_fen(self):
        self.fen = fen;
