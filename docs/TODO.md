# TODO

## Problems

- run on rpi???
- threaded response+playback (locks or smth to cancel any currently running threads)
- sped?
- &#62;dynamic aud resp loading/layouts
  - error checking in loads from aud&text (filling in gaps/warnings??)
  - global data as fallbacks (see comment ab future cfgs/flags)
- fix the cancelling in loaders/etc (CTRL+C / sys stops?? (daemons...maybe.))
- gh-pages title bar in mobile is wrong colours

## Future

- flags for bits and pieces (argparse)
- more lines (ev)
- cfg/flags
  - diff audio files / text dbs
  - silent mode?
  - mic to use
  - force `is_on_RPi` state
- move `gpio.json` to a global cfg
- PyPI pkgs??? (poetry!)
- prog bars etc for build src
