import React, { FC } from "react";

import "../FileBrowser.css";

interface props {
  data: string;
}

let FileDisplay: FC<props> = ({ data }) => {
  return <code>{data}</code>;
};

export default FileDisplay;
