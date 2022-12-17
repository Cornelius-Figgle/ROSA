# Installation

ROBOTICALLY OBNOXIOUS SERVING ASSISTANT

An emotional smart assistant that doesn't listen to you

*This guide assumes you have [Python 3](https://www.python.org/downloads/) and [Git](https://git-scm.com/downloads) installed and setup, and a [GitHub](https://github.com) account setup. <br> If you do not, please research how to install these yourself for your platform before continuing*

## All Platforms

Any shell commands in this guide are to executed using an appropriate `sh`ell. This could be `Command Prompt`, `Powershell`, `bash`, `Git CMD` or any others of your choice ¯\\( ツ )/¯

First you will want to **clone** the repo (or download the [zip](https://github.com/Cornelius-Figgle/ROSA/zipball/main/) or the [tarball](https://github.com/Cornelius-Figgle/ROSA/tarball/main/) from GitHub):

| *nix | Windows |
| - | - |
|<pre>cd /path/to/some/folder/<br>git clone https://github.com/Cornelius-Figgle/ROSA.git</pre>|<pre>cd c:\\path\\to\\some\\folder\\<br>git clone https://github.com/Cornelius-Figgle/ROSA.git</pre>|

It is recommended that the dependencies are installed inside a [virtual environment](https://docs.python.org/3/library/venv.html) in your project repo

| *nix | Windows |
| - | - |
|<pre>python3 -m venv ./rosa-env<br>source ./rosa-env/scripts/activate</pre>|<pre>python -m venv .\\rosa-env<br>.\\rosa-env\\scripts\\activate.bat</pre>|

Replace the last line with the appropriate command from the table below

| OS | file |
| - | - |
| Windows CMD | `.\rosa-env\scripts\activate.bat` |
| Powershell | `.\rosa-env\scripts\Activate.ps1` |
| sh | `source ./rosa-env/scripts/activate` |

And the dependencies can be installed via [pip](https://pip.pypa.io/en/stable/) (which is normally installed with Python) when inside your virtual environment

*Side note: I could only get `pygame` to work with version `2.1.3.dev8`, however others may not have this issue*

| *nix | Windows |
| - | - |
|<pre>python3 -m pip --version<br>python3 -m pip install --user SpeechRecognition pygame==2.1.3.dev8 PyAudio</pre>|<pre>python -m pip --version<br>python -m pip install SpeechRecognition pygame==2.1.3.dev8 PyAudio</pre>|

Or alternatively, (when inside repository root):

| *nix | Windows |
| - | - |
|<pre>python3 -m pip install --user -r ./docs/requirements.txt</pre>|<pre>python -m pip install -r .\\docs\\win_requirements.txt</pre>|

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
