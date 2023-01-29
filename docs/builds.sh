#!/bin/sh

pyinstaller --noconfirm --log-level=WARN --clean \
    --distpath "./bin/bin" --workpath "./bin/build" \
    --name ROSA --onefile \
    --paths "./.venv/Lib/site-packages" \
    --add-binary "./src/ROSA/responses:./responses" \
    --icon "./docs/ico/hotpot-ai.ico" \
    ./src/ROSA/main.py