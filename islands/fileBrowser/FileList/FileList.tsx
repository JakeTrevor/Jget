import React, { FC } from "react";

import Folder from "../assets/folder.svg";
import File from "../assets/file.svg";

import styles from "./FileList.module.css";

export interface fileListProps {
  data: Directory;
  update: (newDir: string) => void;
}

let FileList: FC<fileListProps> = ({ data, update }) => {
  let keys = Object.keys(data)
    .sort()
    .sort((a, b) => {
      let valA = typeof data[a] === "string" ? 0 : 1;
      let valB = typeof data[b] === "string" ? 0 : 1;
      return valB - valA;
    });

  return (
    <ul className={styles.list}>
      {keys.map((each) => (
        <li key={each} className={styles.item}>
          <button onClick={() => update(each)} className={styles.fileButton}>
            {typeof data[each] === "string" ? (
              // @ts-ignore
              <File className={styles.svg} />
            ) : (
              // @ts-ignore
              <Folder className={styles.svg} />
            )}
            <h3>{each}</h3>
          </button>
        </li>
      ))}
    </ul>
  );
};

export default FileList;
