import React from "react";
import { createRoot } from "react-dom/client";

import Browser from "./Browser/Browser";

const container = document.getElementById("fileBrowserRoot");
const root = createRoot(container);

declare var data: string;

let replace = {
  "&lt;": "<",
  "&gt;": ">",
  "&#x27;": "'",
  "&quot;": '"',
  "&amp;": "&",
  "\n": "\\n",
};

for (let [key, val] of Object.entries(replace)) {
  data = data.replaceAll(key, val);
}

let files: Directory = JSON.parse(data);

root.render(<Browser data={files} />);
