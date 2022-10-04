import { useState, useCallback } from "react";

function getQueryParam(key: string): string | null {
  let queryParams = new URLSearchParams(window.location.search);
  return queryParams.get(key);
}

function updateQueryParam(key: string, value: string): void {
  const url = new URL(window.location.href);
  url.searchParams.set(key, value);
  window.history.pushState({}, "", url);
}

function useQueryParam(
  key: string,
  initValue: string = ""
): [string, (newValue: string) => void] {
  let first = getQueryParam(key) || initValue;
  let [value, setValue] = useState<string>(first);

  let update = useCallback(
    (newValue: string) => {
      updateQueryParam(key, newValue);
      setValue(newValue);
    },
    [key]
  );

  return [value, update];
}

export default useQueryParam;
