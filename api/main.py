import chess
import sys

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()


class ChessState(BaseModel):
    fen: str


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://mongochess.dygant.com/",
        "https://comforting-croissant-0cc459.netlify.app/",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def read_root():
    return "Healthy boi"


@app.post("/move")
def make_chess_move(chess_state: ChessState):
    return make_chess_move(chess_state)


"""
Utils functions
"""


def minimaxRoot(depth, board, isMaximizing):
    possibleMoves = board.legal_moves
    bestMove = -9999
    bestMoveFinal = None
    for x in possibleMoves:
        move = chess.Move.from_uci(str(x))
        board.push(move)
        value = max(
            bestMove, minimax(depth - 1, board, -10000, 10000, not isMaximizing)
        )
        board.pop()
        if value > bestMove:
            bestMove = value
            bestMoveFinal = move
    return bestMoveFinal


def minimax(depth, board, alpha, beta, is_maximizing):
    if depth == 0:
        return -evaluation(board)
    possibleMoves = board.legal_moves
    if is_maximizing:
        bestMove = -9999
        for x in possibleMoves:
            move = chess.Move.from_uci(str(x))
            board.push(move)
            bestMove = max(
                bestMove, minimax(depth - 1, board, alpha, beta, not is_maximizing)
            )
            board.pop()
            alpha = max(alpha, bestMove)
            if beta <= alpha:
                return bestMove
        return bestMove
    else:
        bestMove = 9999
        for x in possibleMoves:
            move = chess.Move.from_uci(str(x))
            board.push(move)
            bestMove = min(
                bestMove, minimax(depth - 1, board, alpha, beta, not is_maximizing)
            )
            board.pop()
            beta = min(beta, bestMove)
            if beta <= alpha:
                return bestMove
        return bestMove


def calculateMove(board):
    possible_moves = board.legal_moves
    if len(possible_moves) == 0:
        print("No more possible moves...Game Over")
        sys.exit()
    bestMove = None
    bestValue = -9999
    n = 0
    for x in possible_moves:
        move = chess.Move.from_uci(str(x))
        board.push(move)
        boardValue = -evaluation(board)
        board.pop()
        if boardValue > bestValue:
            bestValue = boardValue
            bestMove = move

    return bestMove


def evaluation(board):
    i = 0
    evaluation = 0
    x = True
    try:
        x = bool(board.piece_at(i).color)
    except AttributeError as e:
        x = x
    while i < 63:
        i += 1
        evaluation = evaluation + (
            getPieceValue(str(board.piece_at(i)))
            if x
            else -getPieceValue(str(board.piece_at(i)))
        )
    return evaluation


def getPieceValue(piece):
    if piece == None:
        return 0
    value = 0
    if piece == "P" or piece == "p":
        value = 10
    if piece == "N" or piece == "n":
        value = 30
    if piece == "B" or piece == "b":
        value = 30
    if piece == "R" or piece == "r":
        value = 50
    if piece == "Q" or piece == "q":
        value = 90
    if piece == "K" or piece == "k":
        value = 900
    return value


def make_chess_move(chess_state: ChessState):
    print("Making move...")
    board = chess.Board(chess_state.fen)
    move = [*str(minimaxRoot(4, board, True))]
    print(f"Best move calculated: {''.join(move)}")
    result = {
        "from": move[0] + move[1],
        "to": move[2] + move[3],
    }

    if len(move) == 5:
        result["promotion"] = move[4]

    return result
