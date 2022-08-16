import React, { FC } from "react";
import { Directory } from "../types";

import "./FileList.css";

import Folder from "../assets/folder.svg";
import File from "../assets/file.svg";

interface props {
  data: Directory;
}

let FileList: FC<props> = ({ data }) => {
  let keys = Object.keys(data);

  let files = keys.filter((each) => typeof data[each] == typeof "");
  return (
    <ul className="list">
      {keys.map((each) => {
        let icon = <Folder />;
        if (typeof data[each] == typeof "") {
          icon = <File />;
        }

        return (
          <li>
            {icon}
            <p>{each}</p>
          </li>
        );
      })}
    </ul>
  );
};

export default FileList;
