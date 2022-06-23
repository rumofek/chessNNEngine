import { useState } from 'react';
import Chess from 'chess.js';
import { Chessboard } from 'react-chessboard';
const axios = require('axios');


export default function PlayRandomMoveEngine() {
  const [game, setGame] = useState(new Chess());

  function safeGameMutate(modify) {
    setGame((g) => {
      const update = { ...g };
      modify(update);
      return update;
    });
  }
  // function makeRandomMove() {
  //   const possibleMoves = game.moves();
  //   if (game.game_over() || game.in_draw() || possibleMoves.length === 0) return; // exit if the game is over
  //   const randomIndex = Math.floor(Math.random() * possibleMoves.length);
  //   safeGameMutate((game) => {
  //     game.move(possibleMoves[randomIndex]);
  //   });
  // }

  async function onDrop(sourceSquare, targetSquare) {
    let move = null;
    safeGameMutate((game) => {
      move = game.move({
        from: sourceSquare,
        to: targetSquare,
        promotion: 'q' // always promote to a queen for example simplicity
      });
    });
    if (move === null) return false; // illegal move
    else console.log(sourceSquare + targetSquare)
    let moveResponse = await axios.post("http://localhost:5000/move", {move: sourceSquare+targetSquare})
    let engineMove = moveResponse.data.move
    if (engineMove.length == 4) {
      safeGameMutate((game) => {
        game.move({ from: engineMove.substring(0, 2), to: engineMove.substring(2) })
      }); 
    }
    return true;
  }

  async function startGame() {
    setGame(new Chess())
    let moveResponse = await axios.post("http://localhost:5000/start")
    console.log(moveResponse)
    let move = moveResponse.data.move
    if (move.length == 4) {
      safeGameMutate((game) => {
        game.move({ from: move.substring(0, 2), to: move.substring(2) })
      }); 
    }
    console.log(move)
  }
  async function resetGame() {
    setGame(new Chess())
  }

  return <div>
    <Chessboard position={game.fen()} onPieceDrop={onDrop} boardOrientation='black' />
    <button onClick={startGame}> Start </button>
    <button onClick={resetGame}> Reset </button>
  </div>



}