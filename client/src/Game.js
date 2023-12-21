import { useState, useMemo, useCallback, useEffect } from "react";
import { Chessboard } from "react-chessboard";
import { Chess } from "chess.js";
import CircularProgress from "@mui/material/CircularProgress";
import CustomDialog from "./components/CustomDialog";
import axios from "axios";

function Game({ orientation }) {
  const chess = useMemo(() => new Chess(), []);
  const [fen, setFen] = useState(chess.fen());
  const [over, setOver] = useState("");
  const [loading, setLoading] = useState(false);
  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);
      const botMove = await requestMoveFromBot();

      chess.move(botMove);
      setFen(chess.fen());
      setLoading(false);
    };
    if (orientation === "b") {
      fetchData();
    }
  }, []);
  function onDrop(sourceSquare, targetSquare) {
    const moveData = {
      from: sourceSquare,
      to: targetSquare,
      color: chess.turn(),
      promotion: "q",
    };

    const move = makeAMove(moveData);

    if (move === null) return false;

    return true;
  }

  const requestMoveFromBot = async () => {
    return (
      await axios.post("http://chess.dygant.com/move", { fen: chess.fen() })
    ).data;
  };

  const makeAMove = useCallback(
    async (move) => {
      try {
        const result = chess.move(move);
        setFen(chess.fen());
        setLoading(true);
        const botMove = await requestMoveFromBot();

        chess.move(botMove);
        setFen(chess.fen());
        setLoading(false);
        if (chess.isGameOver()) {
          if (chess.isCheckmate()) {
            setOver(
              `Checkmate! ${chess.turn() === "w" ? "black" : "white"} wins!`
            );
          } else if (chess.isDraw()) {
            setOver("Draw");
          } else {
            setOver("Game over");
          }
        }

        return result;
      } catch (e) {
        return null;
      }
    },
    [chess, fen, requestMoveFromBot]
  );

  return (
    <>
      <div className="board">
        <Chessboard
          position={fen}
          onPieceDrop={onDrop}
          isDraggablePiece={({ piece }) => piece.includes(orientation)}
          boardOrientation={orientation === "w" ? "white" : "black"}
          customDarkSquareStyle={{ backgroundColor: "#779952" }}
          customLightSquareStyle={{ backgroundColor: "#edeed1" }}
          customBoardStyle={{
            borderRadius: "4px",
            boxShadow: "0 2px 10px rgba(0, 0, 0, 0.5)",
          }}
          boardWidth={700}
        />
        {loading ? (
          <h2>
            <CircularProgress />
            Waiting for the bot to make a move...
          </h2>
        ) : null}
      </div>
      <CustomDialog
        open={Boolean(over)}
        title={over}
        contentText={over}
        handleContinue={() => {
          setOver("");
        }}
      />
    </>
  );
}

export default Game;
