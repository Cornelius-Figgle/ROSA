# Installation

ROBOTICALLY OBNOXIOUS SERVING ASSISTANT

An emotional smart assistant that doesn't listen to you

*This guide assumes you have [Python 3](https://www.python.org/downloads/) and [Git](https://git-scm.com/downloads) installed and setup, and a [GitHub](https://github.com) account setup. <br> If you do not, please research how to install these yourself for your platform before continuing*

## All Platforms

Any shell commands in this guide are to executed using an appropriate `sh`ell. This could be `Command Prompt`, `Powershell`, `bash`, `Git CMD` or any others of your choice ¯\\( ツ )/¯

First you will want to **clone** the repo (or download the [zip](https://github.com/Cornelius-Figgle/ROSA/zipball/main/)/[tarball](https://github.com/Cornelius-Figgle/ROSA/tarball/main/) from GitHub):

[Python 3](https://www.python.org/downloads/) and [poetry](https://python-poetry.org/) will need to be installed if it isn't already

You can then either clone the repo or download the zip from GitHub

```shell
git clone https://github.com/Cornelius-Figgle/ROSA.git
```

The dependencies can be installed via [poetry](https://python-poetry.org/)

```shell
poetry install --without dev
```

*side note: I could only get `pygame` to work with version `2.1.3.dev8`, however others may not have this issue*

## *nix Only

On *nix systems, the package `python3-sdl2` may need to be installed using the system's package manager as the [pip](https://pip.pypa.io/en/stable/) version seems to have errors importing the shared objects (see [here](https://stackoverflow.com/a/37749807/19860022) for more details)

```bash
sudo apt install python3-sdl2
```

PyAudio also may need to be installed via the `python-pyaudio` package (you will also need to install the `flac` library afterwards) using the system's package manager as the [pip](https://pip.pypa.io/en/stable/) version doesn't include the necessary libraries (see [here](https://stackoverflow.com/questions/36681836/pyaudio-could-not-import-portaudio) for more details)

```bash
sudo apt install python-pyaudio flac python3-gst-1.0
```

Replace `apt` with the package manager for your system (`dpkg`, `apt-get`, `pacman`, etc)
