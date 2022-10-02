import React from "react";
import { createRoot } from "react-dom/client";

import Wrapper from "./wrapper/wrapper";

const container = document.getElementById("fileBrowserRoot");
const root = createRoot(container);

root.render(<Wrapper />);
