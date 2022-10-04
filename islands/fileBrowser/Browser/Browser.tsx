import React, { FC } from "react";

import Back from "../assets/back.svg";
import FileList from "../FileList/FileList";
import FileDisplay from "../FileDisplay/FileDisplay";

import styles from "./Browser.module.css";
import useQueryParam from "../useQueryParam/useQueryParam";

export interface browserProps {
  data: Directory;
}

export function encodeArr(arr: string[]): string {
  return JSON.stringify(arr);
}

export function decodeArr(arrStr: string): string[] {
  if (!arrStr) return [];
  return JSON.parse(arrStr);
}

function lookup(dict: Directory, address: string[]): string | Directory {
  let reducer = (acc: Directory | string, val: string) => {
    if (typeof acc === "string") return acc;
    return acc[val];
  };

  return address.reduce(reducer, dict);
}

let Browser: FC<browserProps> = ({ data }) => {
  let [encodedPointer, setPointer] = useQueryParam("dir");
  let pointer = decodeArr(encodedPointer);

  function updatePointer(newVal: string) {
    setPointer(encodeArr([...pointer, newVal]));
  }

  function goUp() {
    let newPointer = pointer.slice(0, -1);
    setPointer(encodeArr(newPointer));
  }

  let curDisplay = lookup(data, pointer);

  let leaf = pointer.at(-1);

  let isMarkdown = false;
  if (leaf) isMarkdown = leaf.endsWith(".md");

  let child =
    typeof curDisplay == "string" ? (
      <FileDisplay data={curDisplay} isMarkdown={isMarkdown} />
    ) : (
      <FileList data={curDisplay as Directory} update={updatePointer} />
    );

  return (
    <div className={styles.browser}>
      <span className={styles.title}>
        <h1>{leaf || "Files"}</h1>
        <button className={styles.button} onClick={goUp}>
          {/* @ts-ignore */}
          <Back className={styles.svg} />
        </button>
      </span>
      {child}
    </div>
  );
};

export default Browser;
