import WhiteKing from "../assets/w_king.png";
import BlackKing from "../assets/b_king.png";

export default function KingIcon({ color }) {
  const src = color === "white" ? WhiteKing : BlackKing;
  return <img style={{ width: "50px" }} src={src} alt="Piece selector" />;
}
