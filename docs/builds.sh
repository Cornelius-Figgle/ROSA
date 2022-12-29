#!/bin/sh

pyinstaller --noconfirm --log-level=WARN --clean \
    --distpath "./bin/bin" --workpath "./bin/build" \
    --name ROSA --onefile \
    --paths "./rosa-env/Lib/site-packages" \
    --hidden-import pyi_splash \
    --add-binary "./src/ROSA/responses:./responses" \
    --splash "./docs/ico/hotpot-ai.png" --icon "./docs/ico/hotpot-ai.ico" \
    ./src/ROSA/main.py