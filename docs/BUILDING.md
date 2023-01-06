# How to Build ROSA

[<img src="../docs/ico/rick_meme.jpg" width="300" align="right"/>](../docs/ico/rick_meme.jpg)

*please read the [CONTRIBUTING guide](./CONTRIBUTING.md), as well as the [Code Of Conduct](./CODE_OF_CONDUCT.md) before proceeding*

## *nix

Make sure all the usual dependencies are installed:

```bash
python3 -m pip install SpeechRecognition pygame==2.1.3.dev8 PyAudio
sudo apt install python3-sdl2
sudo apt install python-pyaudio flac python3-gst-1.0
```

And the build dependencies:

```bash
python3 -m pip install pyinstaller
```

Then run the following shell script to compile with [pyinstaller](https://pyinstaller.org/en/stable/):

```bash
bash ./docs/builds.sh
```

or:

```bash
source ./docs/builds.sh
```

Alternatively, the pyinstaller command can be manually run via:

```bash
pyinstaller --noconfirm --log-level=WARN --clean --distpath "./bin/bin" --workpath "./bin/build" --name ROSA --onefile --paths "./rosa-env/Lib/site-packages" --add-binary "./src/ROSA/responses:./responses" --icon "./docs/ico/hotpot-ai.ico" ./src/ROSA/main.py
```

## Windows

Make sure all the usual dependencies are installed:

```shell
python -m pip install SpeechRecognition pygame==2.1.3.dev8 PyAudio
```

And the build dependencies:

```shell
python -m pip install pyinstaller pywin32 pywin32-ctypes PyQt5
```

Then run the following batch file to compile with [pyinstaller](https://pyinstaller.org/en/stable/):

```shell
.\docs\builds.bat
```

Alternatively, the pyinstaller commands can be manually run via:

```shell
pyinstaller --noconfirm --log-level=WARN --clean --distpath ".\bin\bin" --workpath ".\bin\build" --name ROSA --onefile --paths ".\rosa-env\Lib\site-packages" --add-binary ".\src\ROSA\responses;.\responses" --icon ".\docs\ico\hotpot-ai.ico" .\src\ROSA\main.py

pyinstaller --noconfirm --log-level=WARN --clean --distpath ".\bin\bin" --workpath ".\bin\build" --name  ROSA-installer_uac --onefile --nowindow --uac-admin --paths ".\rosa-env\Lib\site-packages" --hidden-import pyi_splash --splash ".\docs\ico\hotpot-ai.png" --icon ".\docs\ico\hotpot-ai.ico" .\src\ROSA-installer\UAC-ROSA-installer.py

pyinstaller --noconfirm --log-level=WARN --clean --distpath ".\bin" --workpath ".\bin\build" --name ROSA-installer_gui --onefile --nowindow --paths ".\rosa-env\Lib\site-packages" --add-data ".\bin\bin;." --add-data ".\docs\ico;.\ico" --hidden-import pyi_splash --splash ".\docs\ico\hotpot-ai.png" --icon ".\docs\ico\hotpot-ai.ico" .\src\ROSA-installer\WIN_ROSA-installer.py
```
