# Installation

ROBOTICALLY OBNOXIOUS SERVING ASSISTANT

An emotional smart assistant that doesn't listen to you

*This guide assumes you have [Python 3](https://www.python.org/downloads/) and [Git](https://git-scm.com/downloads) installed and setup, and a [GitHub](https://github.com) account setup. <br> If you do not, please research how to install these yourself before continuing*

## All Platforms

First you will want to **clone** the repo or [download the zip from GitHub](https://github.com/Cornelius-Figgle/ROSA/zipball/main/)

| *nix | Windows |
| - | - |
|<pre>cd ~/source/projects/<br>git clone https://github.com/Cornelius-Figgle/ROSA.git</pre>|<pre>cd c:\\users\\Cornelius-Figgle\\source\\projects\\<br>git clone https://github.com/Cornelius-Figgle/ROSA.git</pre>|

It is recommended that the dependencies are installed inside a [virtual environment](https://docs.python.org/3/library/venv.html) in your project repo

| *nix | Windows |
| - | - |
|<pre>python3 -m venv ./rosa-env<br>bash ./rosa-env/scripts/activate</pre>|<pre>python3 -m venv ./rosa-env<br>./rosa-env/scripts/activate.bat</pre>|

Replace the last line with the appropriate command from the table below

| OS | file |
| - | - |
| Windows CMD | `.\rosa-env\scripts\actaivate.bat` |
| Powershell | `.\rosa-env\scripts\Activate.ps1` |
| bash/sh | `bash ./rosa-env/scripts/activate` |
| fish | `fish ./rosa-env/scripts/activate.fish` |
| csh/tcsh | `csh ./rosa-env/scripts/activate.csh` |

And the dependencies can be installed via [pip](https://pip.pypa.io/en/stable/) (which is normally installed with Python) when inside your virtual environment

```shell
pip install SpeechRecognition pygame==2.1.3.dev8 PyAudio
```

or alternatively, (when inside repository root)

```shell
pip install -r ./docs/requirements.txt
```

## Linux Only

On Linux, PyAudio may need to be installed via the `python-pyaudio` package (you will also need to install the `flac` library afterwards) using the system's package manager as the [pip](https://pip.pypa.io/en/stable/) version doesn't include the necessary libraries (see [here](https://stackoverflow.com/questions/36681836/pyaudio-could-not-import-portaudio) for more details)

```bash
sudo apt install python-pyaudio flac python3-gst-1.0
```

Just replace `apt` with the package manager for your system (`dpkg`, `apt-get`, `pacman`, etc)
