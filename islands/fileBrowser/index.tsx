import React from "react";
import { createRoot } from "react-dom/client";

import Browser from "./Browser/Browser";

const container = document.getElementById("fileBrowserRoot");
const root = createRoot(container);

declare var data: string;

data = data.replaceAll("\n", "\\n");

let files: Directory = JSON.parse(data);

console.log(files);

root.render(<Browser data={files} />);
