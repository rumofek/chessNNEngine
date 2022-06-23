import keras
import pandas
import chess
import numpy as np
import tensorflow as tf
import os

df = pandas.read_csv("/media/games.csv")

# 0 - empty space
# 1 - white pawn
# 2 - white knight
# 3 - white bishop
# 4 - white rook
# 5 - white queen
# 6 - white king

# create one-hot encoding
# capital is white
blackPieces = "pnbrqk"
whitePieces = blackPieces.upper()


def convert_fen(fen):
    matrix = []
    striped_fen = fen[0: fen.index(" ") if " " in fen else len(fen)]
    rows = striped_fen.split("/")
    for row in rows:
        toAddRow = []
        rowList = list(row)
        for piece in rowList:
            toAddPiece = [0, 0, 0, 0, 0, 0]
            if piece in blackPieces:
                toAddPiece[blackPieces.index(piece)] = -1
            elif piece in whitePieces:
                toAddPiece[whitePieces.index(piece)] = 1
            else:
                count = int(piece)
                for x in range(count - 1):
                    toAddRow.append(np.asarray(toAddPiece).astype("float32"))
            toAddRow.append(np.asarray(toAddPiece).astype("float32"))
        matrix.append(np.asarray(toAddRow))
    return np.asarray(matrix)


subsetDf = df.sample(n=3000000)
#
subsetDf["boardMatrix"] = subsetDf["fen"].map(convert_fen)

from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Flatten, Dropout, Conv2D
import tensorflow.keras

X = np.asarray(list(subsetDf["boardMatrix"]))
y = np.asarray(list(subsetDf["expectedMove"]))
print(np.shape(X))
print(np.shape(y))

print(y[0])

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=101)

# print(np.shape(X[0]))
#
# X[0] = tf.convert_to_tensor(X[0])


# boards = []
#
# boards.append(convert_fen("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"))
# boards.append(convert_fen("rnbqkbnr/ppp1pppp/3p4/8/8/6P1/PPPPPP1P/RNBQKBNR"))
# boards.append(convert_fen("r1bqkbnr/ppp1pppp/2np4/8/8/6P1/PPPPPPBP/RNBQK1NR"))
# boards.append(convert_fen("r2qkbnr/pppbpppp/2np4/8/8/3P2P1/PPP1PPBP/RNBQK1NR"))
# boards.append(convert_fen("r1q1kbnr/pppbpppp/2np4/8/8/3P1NP1/PPP1PPBP/RNBQK2R"))

model = Sequential()

model.add(keras.Input(shape=(8, 8, 6)))
model.add(Conv2D(filters=32, kernel_size=(3, 3), strides=(1, 1)))
model.add(Flatten())
model.add(Dense(2000, activation=tf.nn.tanh))
# model.add(Flatten(input_shape=(8, 8, 6)))
# model.add(Dropout(.2))
# model.add(Dropout(.1))
# model.add(Dense(384, activation=tf.nn.tanh))
# model.add(Dropout(.2))
# model.add(Flatten(input_shape=(8,8,384)))
# model.add(Dense(384, activation=tf.nn.tanh))
# model.add(Dropout(.2))
# model.add(Dense(384, activation=tf.nn.relu))
# model.add(Dropout(.2))
model.add(Dense(1968, activation=tf.nn.sigmoid))

print(model.summary())

model.compile(loss='sparse_categorical_crossentropy', optimizer='adam',
              metrics=["sparse_categorical_accuracy"])

model.fit(x=X_train, y=y_train, epochs=20, batch_size=256, validation_data=(X_test, y_test))
from tensorflow.keras.models import load_model

model.save('/media/ConvAFTF32K3S1_Flatten_D2800AFTANH_FinalSigmoid.h5')

# print(df.columns)
# print(df.head())
# print(df.info)
# print(df.keys())
# df["boardMatrix"] = df.apply(lambda row: convert_fen(row['fen']), axis=1)

# df["boardMatrix"] = df["fen"].map(convert_fen)

# print(df.head())

# print(df.head(10))
