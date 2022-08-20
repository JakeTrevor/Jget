import React, { FC, useEffect, useState } from "react";

import "../FileBrowser.css";

import Back from "../assets/back.svg";
import FileList from "../FileList/FileList";
import FileDisplay from "../FileDisplay/FileDisplay";

interface props {
  data: Directory;
}

let lookup = (dict: Directory, address: string[]) => {
  return address.reduce((acc, val) => acc[val], dict);
};

let Browser: FC<props> = ({ data }) => {
  let [pointer, setPointer] = useState([]);

  let updatePointer = (newVal: string) => {
    setPointer([...pointer, newVal]);
  };

  let curDisplay = lookup(data, pointer);

  let child =
    typeof curDisplay == "string" ? (
      <FileDisplay data={curDisplay} />
    ) : (
      <FileList data={curDisplay as Directory} update={updatePointer} />
    );

  return (
    <div className="FileBrowser">
      <span>
        <h1>{pointer.at(-1) || "Files"}</h1>
        <button
          onClick={() => {
            setPointer(pointer.slice(0, -1));
          }}
        >
          <Back />
        </button>
      </span>
      {child}
    </div>
  );
};

export default Browser;
