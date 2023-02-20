# How to Build ROSA

[<img src="../docs/ico/rick_meme.jpg" width="300" align="right"/>](../docs/ico/rick_meme.jpg)

*please read the [CONTRIBUTING guide](./CONTRIBUTING.md), as well as the [Code Of Conduct](./CODE_OF_CONDUCT.md) before proceeding*

Make sure the build dependencies are installed:

```shell
poetry install
```

Then run the following Python script to compile with [pyinstaller](https://pyinstaller.org/en/stable/):

```shell
# POSIX
python3 ./src/build/build.py

# WINDOWS
py .\src\build\build.py --installer
```

And that should be everything! For more info about configuration see below

```shell
usage: ./src/build/build.py [-h] [-v] [-i] [-w PATH] [--no-check]
```

| Flag | Description |
| - | - |
| -h, --help | show the help message and exit |
| -v, --version | show version info and exit |
| -i, --installer | whether to build to the Windows installer, defaults to `False` (does nothing on posix) |
| -w PATH, --work-dir PATH | the working directory used for compiling. Should be the project root, defaults to `os.getcwd()` |
|  --no-check | skips the directory checks before compilation, defaults to `False`. (Not recommended) |
