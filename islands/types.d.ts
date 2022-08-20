declare module "*.svg" {
  const svg: string;
  export default svg;
}

declare interface Directory {
  [index: string]: string | Directory;
}

declare type setState<T> = React.Dispatch<React.SetStateAction<T>>;
