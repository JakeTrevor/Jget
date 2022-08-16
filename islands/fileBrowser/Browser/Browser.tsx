import React, { FC, useEffect, useState } from "react";
import { Directory } from "../types";

import FileList from "../FileList/FileList";

interface props {
  data: Directory;
}

let lookup = (dict: Directory, address: string[]) => {
  return address.reduce((acc, val) => acc[val], dict);
};

let Browser: FC<props> = ({ data }) => {
  let [pointer, setPointer] = useState([]);

  let curDisplay = lookup(data, pointer);

  let child;

  if (typeof curDisplay == typeof "") {
    child = <p></p>;
  } else {
    child = <FileList data={curDisplay as Directory} />;
  }

  return (
    <div className="FileBrowser">
      <h1>title</h1>
      <p>hello world</p>
      {child}
    </div>
  );
};

export default Browser;
