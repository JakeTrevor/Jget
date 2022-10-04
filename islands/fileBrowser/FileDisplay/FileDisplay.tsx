import React, { FC, useEffect, useRef } from "react";

import ReactMarkdown from "react-markdown";

import hljs from "highlight.js";
import "highlight.js/styles/atom-one-dark.css";

import styles from "./FileDisplay.module.css";

export interface fileDisplayProps {
  data: string;
  isMarkdown: boolean;
}

let FileDisplay: FC<fileDisplayProps> = ({ data, isMarkdown }) => {
  let codeBlock = useRef<HTMLElement>(null);

  useEffect(() => {
    if (codeBlock.current === null) return;

    hljs.highlightElement(codeBlock.current);
  });

  return (
    <pre className={styles.container}>
      {isMarkdown ? (
        <code className="hljs">
          <ReactMarkdown>{data}</ReactMarkdown>
        </code>
      ) : (
        <code ref={codeBlock}>{data}</code>
      )}
    </pre>
  );
};

export default FileDisplay;
