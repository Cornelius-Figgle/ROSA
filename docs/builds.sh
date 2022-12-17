#!/bin/sh

cd ..

python3 -m pyinstaller --noconfirm --log-level=WARN --clean \
    --distpath "./bin/bin" --workpath "./bin/build" \
    --name ROSA --onefile \
    --paths "./rosa-env/Lib/site-packages" \
    --hidden-import pyi_splash \
    --add-binary "./responses:./responses" \
    --splash "./docs/ico/hotpot-ai.png" --icon "./docs/ico/hotpot-ai.ico" \
    ./main.py