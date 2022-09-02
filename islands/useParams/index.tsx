import React, { useState, useCallback } from "react";

function getQueryParam(key: string): string | null {
  let queryParams = new URLSearchParams(window.location.search);
  return queryParams.get(key);
}

function updateQueryParam(key: string, value: string): void {
  const url = new URL(window.location.href);
  url.searchParams.set(key, value);
  window.history.pushState({}, "", url);
}

export function useQueryParams(
  key: string,
  initValue: string = ""
): [string, (newValue: string) => void] {
  let first = getQueryParam(key) || initValue;
  let [value, setValue] = useState<string>(first);

  let update = useCallback(
    (newValue: string) => {
      console.log(newValue);
      updateQueryParam(key, newValue);
      setValue(newValue);
    },
    [key]
  );

  return [value, update];
}

export function encodeArr(arr: string[]): string {
  return JSON.stringify(arr);
}

export function decodeArr(arrStr: string): string[] {
  if (arrStr) {
    return JSON.parse(arrStr);
  }
  return [];
}
