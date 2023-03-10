# Project Structure Planning for ROSA (Python is marginally annoying)

*not to be confused with [TREE.txt](./TREE.txt)*

SEE [GLANCES](https://github.com/nicolargo/glances/tree/develop/glances) REPO STRUCTURE FOR INSPIRATION

## Glances

### CLI Invocation

- Running `glances` directly / running `python -m glances`
  - to do with `pip install`? (hmmm)
  - install loc ig?

### How?

```text
# glances/README.txt

__init__.py                 Global module init
__main__.py                 Entry point for Glances module
config.py                   Manage the configuration file
globals.py                  Share variables upon modules
main.py                     Main script to rule them up...
```

```python
# glances/__main__.py

"""Allow user to run Glances as a module."""

# Execute with:
# $ python -m glances (2.7+)
```

- `__main__.py` imports `glances` and then calls `glances.main()` (under a `__name__` check ofc)
  - this imports the `__init__.py` file (bc, python) and calls its `main()`
  - just so it can be run as a module
- `__init__.py` is actual setup and boot
  - checks version info etc
  - imports `GlancesMain` from `main.py`
  - starts program bases on cfgs/args from `GlancesMain`
  - when specific mode classes are started, they boot the UI stuff from init's inside their class files
- `main.py` parses CLI args & config files
  - also determines mode to start in
  - these are returned to `__init__.py` when class construction is complete? idk right terms here
    - `__init__()` loads `parse_args()` into `args` dict
      - `parse_args()` calls `args = self.init_args().parse_args()` to parse the CLI args in `init_args()`
      - config file loc is checked (set in CLI args)
        - `self.config = Config(args.conf_file)`
      - config file is then parsed

## ROSA

### Invocation

- should be able to run by `ROSA` / `rosa` / whatever
  - also direct file run but is same thing ig
- flags should be passed to this (sort this out **LATER**)
- config file as well (and this ^)
- overall pretty similar approach (thanks @nicolargo)
  - diff file names tho? (help :/)

### How To Accomplish

| Current File | New File | Purpose |
| - | - | - |
| `main.py` | `__init__.py` | Global module init |
| `main.py` | `__main__.py` | Entry point for module |
| `foreign_potato_master.py` | `foreign_potato_master.py` | IO Data |
| `ROSA.py` | `main.py` | Main script to rule them all... (parse args/cfgs here) |

```pwsh
> py -m src.ROSA
python.exe: No module named src.ROSA.__main__; 'src.ROSA' is a package and cannot be directly executed
```
