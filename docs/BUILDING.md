# How to Build ROSA

[<img src="../docs/ico/rick_meme.jpg" width="300" align="right"/>](../docs/ico/rick_meme.jpg)

*please read the [CONTRIBUTING guide](./CONTRIBUTING.md), as well as the [Code Of Conduct](./CODE_OF_CONDUCT.md) before proceeding*

## *nix

Make sure the build dependencies are installed:

```shell
poetry install
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
pyinstaller --noconfirm --log-level=WARN --clean --distpath "./bin/bin" --workpath "./bin/build" --name ROSA --onefile --paths "./.venv/Lib/site-packages" --add-binary "./src/ROSA/responses:./responses" --icon "./docs/ico/hotpot-ai.ico" ./src/ROSA/main.py
```

## Windows

Make sure the build dependencies are installed:

```shell
poetry install
```

Then run the following batch file to compile with [pyinstaller](https://pyinstaller.org/en/stable/):

```shell
.\docs\builds.bat
```

Alternatively, the pyinstaller commands can be manually run via:

```shell
pyinstaller --noconfirm --log-level=WARN --clean --distpath ".\bin\bin" --workpath ".\bin\build" --name ROSA --onefile --paths ".\.venv\Lib\site-packages" --add-binary ".\src\ROSA\responses;.\responses" --icon ".\docs\ico\hotpot-ai.ico" .\src\ROSA\main.py

pyinstaller --noconfirm --log-level=WARN --clean --distpath ".\bin\bin" --workpath ".\bin\build" --name  ROSA-installer_uac --onefile --nowindow --uac-admin --paths ".\.venv\Lib\site-packages" --hidden-import pyi_splash --splash ".\docs\ico\hotpot-ai.png" --icon ".\docs\ico\hotpot-ai.ico" .\src\ROSA-installer\UAC-ROSA-installer.py

pyinstaller --noconfirm --log-level=WARN --clean --distpath ".\bin" --workpath ".\bin\build" --name ROSA-installer_gui --onefile --nowindow --paths ".\.venv\Lib\site-packages" --add-data ".\bin\bin;." --add-data ".\docs\ico;.\ico" --hidden-import pyi_splash --splash ".\docs\ico\hotpot-ai.png" --icon ".\docs\ico\hotpot-ai.ico" .\src\ROSA-installer\WIN_ROSA-installer.py
```
