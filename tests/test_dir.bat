REM @echo off
set TAB=    
set NLM=^


set NL=^^^%NLM%%NLM%^%NLM%%NLM%
cls
echo > tree_error.log


CHOICE /N /M "Running batch-compile from '%CD%', are you sure you want to continue? (y/n)"
if %errorlevel% NEQ 1 (
    EXIT /B  REM future: maybe add an exit code here?
) else (
    echo %TAB%Continuing with script%NL%
)

CHOICE /N /M "Do you wish to compile the Windows Installer as well as the main program? (y/n)"
if %errorlevel% EQU 1 (
    echo %TAB%Compiling the installer as well%NL%
    set do_installer=True
) else if %errorlevel% EQU 2 (
    echo %TAB%Not compiling the installer%NL%
    set do_installer=True
)


echo Checking for a valid directory tree structure...

REM note: project root folder name
for %%f in (%CD%) do set final_dir=%%~nxf
if %final_dir% NEQ ROSA (
    if %final_dir% NEQ rosa (
        echo %TAB%WARN: project root folder is not named 'ROSA' or 'rosa', this may cause instability
        (echo WARN: project root folder is not named 'ROSA' or 'rosa', this may cause instability) >> tree_error.log
    ) else (
        echo %TAB%INFO: project root folder is acceptable
        (echo INFO: project root folder is acceptable) >> tree_error.log
    )
) else (
    echo %TAB%INFO: project root folder is acceptable
    (echo INFO: project root folder is acceptable) >> tree_error.log
)
    echo %do_installer% 
    pause

if %do_installer% EQU True 
    (set check_path=.\src\build\create_shortcut.vbs
    REM note: .\src\build\create_shortcut.vbs
    
    echo %check_path%
    pause
    if NOT exist %check_path% (
        set was_error=True
        echo %TAB%ERROR: %check_path% was not found
        (echo ERROR: %check_path% was not found) >> tree_error.log
    ) else (
        echo %TAB%INFO: %check_path% was found
        (echo INFO: %check_path% was found) >> tree_error.log
    )
    )

REM note: .\src\build\README.md
set check_path=.\src\build\README.md
if NOT exist %check_path% (
    set was_error=True
    echo %TAB%ERROR: %check_path% was not found
    (echo ERROR: %check_path% was not found) >> tree_error.log
) else (
    echo %TAB%INFO: %check_path% was found
    (echo INFO: %check_path% was found) >> tree_error.log
)

REM note: .\src\ROSA\responses
set check_path=.\src\ROSA\responses
if NOT exist %check_path% (
    set was_error=True
    echo %TAB%ERROR: %check_path% was not found
    (echo ERROR: %check_path% was not found) >> tree_error.log
) else (
    echo %TAB%INFO: %check_path% was found
    (echo INFO: %check_path% was found) >> tree_error.log
)


if %was_error% EQU True (
    echo %TAB%Exiting with errors%NL%
    EXIT /B 2
)
