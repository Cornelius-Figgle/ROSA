pyinstaller --noconfirm --log-level=WARN --clean ^
    --distpath ".\bin\bin" --workpath ".\bin\build" ^
    --name ROSA --onefile ^
    --paths ".\rosa-env\Lib\site-packages" ^
    --add-binary ".\src\ROSA\responses;.\responses" ^
    --icon ".\docs\ico\hotpot-ai.ico" ^
    .\src\ROSA\main.py

pyinstaller --noconfirm --log-level=WARN --clean ^
    --distpath ".\bin\bin" --workpath ".\bin\build" ^
    --name  ROSA-installer_uac --onefile --nowindow --uac-admin ^
    --paths ".\rosa-env\Lib\site-packages" ^
    --hidden-import pyi_splash ^
    --splash ".\docs\ico\hotpot-ai.png" --icon ".\docs\ico\hotpot-ai.ico" ^
    .\src\ROSA-installer\UAC-ROSA-installer.py

pyinstaller --noconfirm --log-level=WARN --clean ^
    --distpath ".\bin" --workpath ".\bin\build" ^
    --name ROSA-installer_gui --onefile --nowindow ^
    --paths ".\rosa-env\Lib\site-packages" ^
	 --add-data ".\bin\bin;." --add-data ".\docs\ico;.\ico" ^
    --hidden-import pyi_splash ^
    --splash ".\docs\ico\hotpot-ai.png" --icon ".\docs\ico\hotpot-ai.ico" ^
    .\src\ROSA-installer\WIN_ROSA-installer.py