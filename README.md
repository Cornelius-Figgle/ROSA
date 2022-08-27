
# ROSA

ROBOTICALLY OBNOXIOUS SERVING ASSISTANT

An emotional smart assistant that doesn't listen to you

*If you wish to install the binaries instead of the source, [see here](https://github.com/Cornelius-Figgle/ROSA/blob/main/bin_README.md)*

## Installation

### All Platforms

[Python 3](https://www.python.org/downloads/) will need to be installed if it isn't already

You can then either clone the repo or download the zip from GitHub

```shell
git clone https://github.com/Cornelius-Figgle/ROSA.git
```

And the dependencies can be installed via [pip](https://pip.pypa.io/en/stable/) (which is normally installed with Python)

```shell
pip install playsound==1.2.2 PyAudio SpeechRecognition 
```

It is recommended that these are installed inside a [virtual environment](https://docs.python.org/3/library/venv.html) in your project repo

### Linux Only

On Linux, PyAudio should be installed via the `python-pyaudio` package (you will also need to install the `flac` library afterwards) using the system's package manager as the [pip](https://pip.pypa.io/en/stable/) version doesn't include the necessary libraries (see [here](https://stackoverflow.com/questions/36681836/pyaudio-could-not-import-portaudio) for more details)

The `python3-gst-1.0` package is also needed for `playsound` to work on a RPi and it should also be installed the same way (see [this](https://github.com/TaylorSMarks/playsound/issues/16) for more details)

```bash
sudo apt install python-pyaudio flac 
```

```bash
sudo apt install python3-gst-1.0
```

Just replace `apt` with the package manager for your system (`dpkg`, `apt-get`, `pacman`, `snap`, etc)

## Usage

### Prerequisites

- [ROSA source code](https://github.com/Cornelius-Figgle/ROSA)
- [Python](https://www.python.org/downloads/)
- [SpeechRecognition](https://pypi.org/project/SpeechRecognition/)
- [PyAudio](https://pypi.org/project/PyAudio/) ([See above for Linux](https://github.com/Cornelius-Figgle/ROSA#Linux))
- [playsound](https://pypi.org/project/playsound/) v1.2.2 ([See above for Linux](https://github.com/Cornelius-Figgle/ROSA#Linux))

### Setup

- Please make sure you have connected your mic and speakers
- Your internet connection is stable (used to transcribe speech via Google Speech Recognition)

Then you should be able to run the `main.py` file from wherever you cloned the repo/extracted the zip to

### Dev Notes

- `playsound()` only works without tags/metadata

## License

[MIT](https://github.com/Cornelius-Figgle/ROSA/blob/main/LICENSE)
