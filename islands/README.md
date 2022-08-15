# JGET Island components

There is at least one place on JGET where an interactive component (via react) would be useful. This subdir encapsulates those projects so they can be bundled to a single file by webpack and placed into the static/scripts/ dir.

---
## fileBrowser
This is a component for use in the JGET web app for browsing a set of files such as those in a package.
This is done in react because a server-side version of this is very slow and inconvienient, especially for deeply nested files.