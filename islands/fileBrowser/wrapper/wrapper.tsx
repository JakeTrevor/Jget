import React, { useEffect, useState } from "react";
import Browser from "../Browser/Browser";

let Wrapper = () => {
  let package_name = window.location.pathname.split("/")[2];
  let target = `${window.location.origin}/api/get/${package_name}/`;

  let [data, setData] = useState({});
  let [loaded, setLoaded] = useState(false);

  let get_data = async () => {
    let res = await fetch(target).then((res) => res.json());
    let files: string = res.files;
    let processed_data = JSON.parse(files);
    setData(processed_data);
    setLoaded(true);
  };

  useEffect(() => {
    get_data();
  }, []);

  return loaded ? <Browser data={data} /> : <div>loading files...</div>;
};

export default Wrapper;
