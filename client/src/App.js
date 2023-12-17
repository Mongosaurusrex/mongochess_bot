import { useState } from "react";

import { Container, ToggleButton, ToggleButtonGroup } from "@mui/material";
import Game from "./Game";
import CustomDialog from "./components/CustomDialog";
import KingIcon from "./components/KingIcon";

export default function App() {
  const [orientation, setOrientation] = useState("");

  const [orientationSubmitted, setOrientationSubmitted] = useState(false);

  return (
    <Container
      sx={{
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        flexDirection: "column",
      }}
    >
      <h1>Welcome to MongoChess!</h1>
      <CustomDialog
        open={!orientationSubmitted}
        title="Which side do you want to play?"
        handleContinue={() => {
          if (!orientation) return;
          setOrientationSubmitted(true);
        }}
      >
        <ToggleButtonGroup value={orientation} size="large" variant="text">
          <ToggleButton
            sx={{
              border: "none",
            }}
            value="w"
            onClick={() => {
              setOrientation("w");
            }}
          >
            <KingIcon color={"white"} />
          </ToggleButton>
          <ToggleButton
            sx={{
              border: "none",
            }}
            value="b"
            onClick={() => {
              setOrientation("b");
            }}
          >
            <KingIcon color={"black"} />
          </ToggleButton>
        </ToggleButtonGroup>
      </CustomDialog>
      {orientationSubmitted ? <Game orientation={orientation} /> : null}
    </Container>
  );
}
