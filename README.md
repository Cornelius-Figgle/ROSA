
# ROSA

[![GitHub license](https://img.shields.io/github/license/Cornelius-Figgle/ROSA)](./LICENSE)
[![CodeQL](https://github.com/Cornelius-Figgle/ROSA/actions/workflows/codeql.yml/badge.svg)](https://github.com/Cornelius-Figgle/ROSA/actions/workflows/codeql.yml)
[![pages-build-deployment](https://github.com/Cornelius-Figgle/ROSA/actions/workflows/pages/pages-build-deployment/badge.svg?branch=gh-pages)](https://github.com/Cornelius-Figgle/ROSA/actions/workflows/pages/pages-build-deployment)

[![Activity](https://img.shields.io/github/commit-activity/m/Cornelius-Figgle/ROSA)](https://github.com/badges/shields/pulse)
[![GitHub commits](https://badgen.net/github/commits/Cornelius-Figgle/ROSA/main)](https://GitHub.com/Cornelius-Figgle/ROSA/commit/)
[![Latest Tag](https://badgen.net/github/tag/Cornelius-Figgle/ROSA)](https://GitHub.com/Cornelius-Figgle/ROSA/tags)

[<img src="./docs/ico/no_idea_rosa.jpg" width="300" align="right"/>](./docs/ico/no_idea_rosa.jpg)

ROBOTICALLY OBNOXIOUS SERVING ASSISTANT

An emotional smart assistant that doesn't listen to you

*If you wish to install the Windows binaries (executables) instead of the source, [see here](https://github.com/cornelius-figgle/ROSA/releases)*

*If you wish to build the Windows binaries (executables), [see here](./docs/BUILDING.md)*

<br>

## Installation

*for a more detailed guide, [see here](https://github.com/Cornelius-Figgle/ROSA/blob/main/docs/INSTALLATION.md)*

### All Platforms

[Python 3](https://www.python.org/downloads/) will need to be installed if it isn't already

You can then either clone the repo or download the zip from GitHub

```shell
git clone https://github.com/Cornelius-Figgle/ROSA.git
```

It is recommended that the dependencies are installed inside a [virtual environment](https://docs.python.org/3/library/venv.html) in your project repo

And the dependencies can be installed via [pip](https://pip.pypa.io/en/stable/) (which is normally installed with Python) when inside your virtual environment

| *nix | Windows |
| - | - |
|<pre>python3 -m pip install SpeechRecognition pygame==2.1.3.dev8 PyAudio</pre>|<pre>py -m pip install SpeechRecognition pygame==2.1.3.dev8 PyAudio</pre>|

or alternatively, (when inside repository root)

| *nix | Windows |
| - | - |
|<pre>python3 -m pip install -r ./docs/requirements.txt</pre>|<pre>py -m pip install -r ./docs/requirements.txt</pre>|

### *nix Only

On *nix systems, the package `python3-sdl2` may need to be installed using the system's package manager as the [pip](https://pip.pypa.io/en/stable/) version seems to have errors importing the shared objects (see [here](https://stackoverflow.com/a/37749807/19860022) for more details)

```bash
sudo apt install python3-sdl2
```

PyAudio also may need to be installed via the `python-pyaudio` package (you will also need to install the `flac` library afterwards) using the system's package manager as the [pip](https://pip.pypa.io/en/stable/) version doesn't include the necessary libraries (see [here](https://stackoverflow.com/questions/36681836/pyaudio-could-not-import-portaudio) for more details)

```bash
sudo apt install python-pyaudio flac python3-gst-1.0
```

Replace `apt` with the package manager for your system (`dpkg`, `apt-get`, `pacman`, etc)

## Usage

### Prerequisites

- [ROSA source code](https://github.com/Cornelius-Figgle/ROSA)
- [Python 3](https://www.python.org/downloads/)
- [SpeechRecognition](https://pypi.org/project/SpeechRecognition/)
- [PyAudio](https://pypi.org/project/PyAudio/) ([See above for Linux](https://github.com/Cornelius-Figgle/ROSA#Linux))
- [pygame==2.1.3.dev8](https://pypi.org/project/pygame/)

### Setup

- If you are on a Raspberry Pi that has LEDs connected to the GPIO header/breadboard/etc, you can write the pin numbers in the `gpio.json` file to let ROSA use the LEDs and buttons connected to the GPIO pins for operation without a monitor [See the file for more info](https://github.com/Cornelius-Figgle/ROSA/blob/19c2df69043d7317d126df6ca36fbc6e90ffcfc4/gpio.json)
- Please make sure you have connected your mic and speakers
- Your internet connection is stable (used to transcribe speech via Google Speech Recognition)

Then you should be able to run the `main.py` file from wherever you cloned the repo/extracted the zip to

## License

[MIT](https://choosealicense.com/licenses/mit/)
