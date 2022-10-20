# Developing for JGET

When developing for JGET, I reccomend a specific setup/file structure to ensure you write code that works for the end user.

Require

Lua's built in require is quite annoying to use, as anyone who has used it will know. However, to preserve compatibility I will not change it.
in Computercraft, Require resolves paths relative to the current working directory (CWD). Code, generally, gets run from the home directory ("/"). This means that generally, after install, a file (say 'main') in your package will be located at "/packages/<package name>/main.lua"

You should write your code with this in mind. If say you choose to split your code into multiple files, they will have to follow this convention.

One way to ensure you're programming this correctly is to write your package where it will be installed. So, say i was writing a "hello" package, I would write it in "/packages/hello/". When you want to test, run the code from the home directory. This ensures that your imports are consistent with what they will need to be in distribution.

JGET is written to facilitate this.

You can, of course, still create separate environments to work on different projects. Say you wanted to work on 'hello', which has some set of dependencies, and 'world', which has a completely different set of dependencies. To make it easy to manage, you might create two folders, one for each. You would then treat each folder as if it were the home directory - so you would 'hello' in "hello/packages/hello/", and 'world' in "world/packages/world/", and execute tests/runs/jget commands from the project root ("/world/" and "/home/" respectively). This way, jget addDeps will not pollute the dependency list with irrelevant packages.

# Adding a Binary

JGET was intended as a packaging tool for libaries. But, you may want to distribute executables or binaries - programs the end user would run from the CraftOS terminal.

By default, to execute say, the main file in the 'mine' package, you would have to write "./packages/mine/main". This is not very convenient. However there is an easy way to solve this, detailed below:

When JGET runs the first time it (creates and) injects a line of code into the 'startup.lua' file on the computer. It looks like this:

```Lua
--this section amends the path so that jget can be run anywhere
shell.setPath(shell.path()..":/")
--amend startup from here
```

This line amends the CraftOS path, so that it can always find jget no matter what your CWD. You can edit this line to do the same for your binaries.

To add all files in your package as binaries, you would add ":/packages/<package name>". This is fine if its one or more standalone executables

However, if your package has multiple files, only one or two of which are executable, I suggest creating a "bin" or "exe" folder within your package to contain any binaries - this prevents clutter in the autocomplete.

To add the files in your bin directory to the path, you would amend the line in startup with ":/packages/<package name>/bin/"

In both cases, substituting "package name" with the name of your package. note the ":" at the start - this is how computercraft separates different paths. It is required. So the whole thing would look like this:

```Lua
--this section amends the path so that jget can be run anywhere
shell.setPath(shell.path()..":/:/packages/<package name>/") -- for standalone executables
shell.setPath(shell.path()..":/:/packages/<package name>/bin/") -- for packages with a bin folder
--amend startup from here
```

At some point, I may get around to implementing this as an automatic feature in JGET - but don't hold your breath.
