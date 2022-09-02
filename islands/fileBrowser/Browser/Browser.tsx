import React, { FC } from "react";

import { useQueryParams, encodeArr, decodeArr } from "../../useParams/index";

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
  let [ecodedPointer, setPointer] = useQueryParams("dir");
  let pointer = decodeArr(ecodedPointer);

  let updatePointer = (newVal: string) => {
    setPointer(encodeArr([...pointer, newVal]));
  };

  let goUp = () => {
    let newPointer = pointer.slice(0, -1);
    setPointer(encodeArr(newPointer));
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
        <button onClick={goUp}>
          <Back />
        </button>
      </span>
      {child}
    </div>
  );
};

export default Browser;
