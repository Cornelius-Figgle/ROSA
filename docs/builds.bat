py -m pyinstaller --noconfirm --log-level=WARN --clean ^
    --distpath ".\bin\bin" --workpath ".\bin\build" ^
    --name ROSA --onefile ^
    --paths ".\rosa-env\Lib\site-packages" ^
    --hidden-import pyi_splash ^
    --add-binary ".\responses;.\responses" ^
    --splash ".\docs\ico\hotpot-ai.png" --icon ".\docs\ico\hotpot-ai.ico" ^
    .\main.py

py -m pyinstaller --noconfirm --log-level=WARN --clean ^
    --distpath ".\bin\bin" --workpath ".\bin\build" ^
    --name  ROSA-installer_uac --onefile --nowindow --uac-admin ^
    --paths ".\rosa-env\Lib\site-packages" ^
    --hidden-import pyi_splash ^
    --splash ".\docs\ico\hotpot-ai.png" --icon ".\docs\ico\hotpot-ai.ico" ^
    .\UAC-ROSA-installer.py

py -m pyinstaller --noconfirm --log-level=WARN --clean ^
    --distpath ".\bin\bin" --workpath ".\bin\build" ^
    --name ROSA-installer_gui --onefile --nowindow ^
    --paths ".\rosa-env\Lib\site-packages" ^
	 --add-data ".\bin\bin;." --add-data ".\docs\ico;.\ico" ^
    --hidden-import pyi_splash ^
    --splash ".\docs\ico\hotpot-ai.png" --icon ".\docs\ico\hotpot-ai.ico" ^
    .\WIN_ROSA-installer.py