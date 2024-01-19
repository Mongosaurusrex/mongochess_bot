from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from mcts import mcts_make_chess_move

app = FastAPI()


class ChessState(BaseModel):
    fen: str


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://mongochess.dygant.com",
        "https://comforting-croissant-0cc459.netlify.app",
        "http://localhost:3000",
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
    return mcts_make_chess_move(chess_state.fen)
