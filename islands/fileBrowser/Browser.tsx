import React, { FC } from "react";

interface directory {
  [index: string]: string | directory;
}

interface props {
  data: directory;
}

let Browser: FC<props> = ({ data }) => {
  // @ts-ignore
  let d: string = data.hello;
  return <div>{d}</div>;
};

export default Browser;
