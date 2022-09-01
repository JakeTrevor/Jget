import React, { FC } from "react";

import "../FileBrowser.css";

import Folder from "../assets/folder.svg";
import File from "../assets/file.svg";

interface props {
  data: Directory;
  update: (newDir: string) => void;
}

let FileList: FC<props> = ({ data, update }) => {
  let keys = Object.keys(data);

  return (
    <ul className="list">
      {keys.map((each) => {
        let icon = <Folder />;
        if (typeof data[each] == typeof "") {
          icon = <File />;
        }

        return (
          <li key={each}>
            <button
              onClick={() => {
                update(each);
              }}
            >
              {icon}
              <h3>{each}</h3>
            </button>
          </li>
        );
      })}
    </ul>
  );
};

export default FileList;
