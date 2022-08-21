
# ROSA

ROBOTICALLY OBNOXIOUS SERVING ASSISTANT

An emotional smart assistant that doesn't listen to you

## Installation

You can either clone the repo or download the zip from Github

```shell
git clone https://github.com/Cornelius-Figgle/ROSA.git
```

And the dependencies can be installed via [pip](https://pip.pypa.io/en/stable/)

```shell
pip install playsound PyAudio SpeechRecognition 
```

It is recommended that these are installed inside a [virtual environment](https://docs.python.org/3/library/venv.html) in your project repo

[Python 3](https://www.python.org/downloads/) will also need to be installed if it isn't already

### Linux

On Linux, PyAudio should be installed via the `python-pyaudio` package (you will also need to install the `flac` library) using the system's package manager

```bash
sudo apt install python-pyaudio flac
```

Just replace `apt` with the package manager for your system (`dpkg`, `apt-get`, `pacman`, `snap`, etc)

## Usage

### Prerequisites

- [ROSA source code](https://github.com/Cornelius-Figgle/ROSA)
- [Python](https://www.python.org/downloads/)
- [SpeechRecognition](https://pypi.org/project/SpeechRecognition/)
- [PyAudio](https://pypi.org/project/PyAudio/) ([See above for Linux](https://github.com/Cornelius-Figgle/ROSA#Linux))
- [playsound](https://pypi.org/project/playsound/)

### Setup

- Please make sure you have connected your mic and speakers
- Your internet connection is stable (used to transcribe speech via Google Speech Recognition)

Then you should be able to run the `main.py` file from wherever you cloned the repo/extracted the zip to

## License

[MIT](https://github.com/Cornelius-Figgle/ROSA/blob/main/LICENSE)
