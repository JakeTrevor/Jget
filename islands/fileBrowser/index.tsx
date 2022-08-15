import React from "react";
import ReactDOM from "react-dom";
import Browser from "./Browser";

ReactDOM.render(
  <React.StrictMode>
    {/* @ts-ignore */}
    <Browser data={data} />
  </React.StrictMode>,
  document.getElementById("fileBrowserRoot")
);
