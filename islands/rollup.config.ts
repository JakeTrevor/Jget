import postCSS from "rollup-plugin-postcss";
import nodeResolve from "@rollup/plugin-node-resolve";
import typescript from "@rollup/plugin-typescript";
import external from "rollup-plugin-peer-deps-external";
import svgr from "@svgr/rollup";
import commonjs from "@rollup/plugin-commonjs";
import nodePolyfills from "rollup-plugin-polyfill-node";

export default {
  input: "fileBrowser/index.tsx",
  output: {
    file: "../static/scripts/fileBrowser.js",
    format: "umd",
  },
  plugins: [
    external(),
    nodeResolve(),
    commonjs(),
    typescript({ tsconfig: "./tsconfig.json" }),
    postCSS({ modules: true }),
    svgr(),
    nodePolyfills(),
  ],
};
