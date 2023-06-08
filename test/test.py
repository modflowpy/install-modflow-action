import json
import os
from os import environ
from pathlib import Path
from platform import system
from pprint import pprint
import requests
from shutil import which
import sys
from typing import List, Tuple

path = Path(sys.argv[1] if sys.argv[1] else "~/.local/bin/modflow").expanduser().absolute()
repo = sys.argv[2] if (len(sys.argv) > 2 and sys.argv[2]) else "executables"
subset = sys.argv[3] if (len(sys.argv) > 3 and sys.argv[3]) else None

print(f"Path: {path}")
print(f"Repo: {repo}")

expected_exes = {
    'executables': [
        'sutra',
        'mp6',
        'mp7',
        'swtv4',
        'mf6',
        'mt3dusgs',
        'zbud6',
        'zonbudusg',
        'mfusg',
        'mfnwtdbl',
        'crt',
        'mt3dms',
        'mf2005dbl',
        'zonbud3',
        'gridgen',
        'mflgrdbl',
        'mfnwt',
        'mf2005',
        'vs2dt',
        'mflgr',
        'mf2000',
        'triangle',
        'mfusgdbl',
    ],
    'modflow6': [
        'mf6',
        'mf5to6',
        'zbud6',
    ],
    'modflow6-nightly-build': [
        'mf6',
        'mf5to6',
        'zbud6',
    ]
}
expected_libs = {
    "executables": ["libmf6"],
    "modflow6": ["libmf6"],
    "modflow6-nightly-build": ["libmf6"]
}

# apply subset filter, if provided
if subset:
    expected_exes = {k: [vv for vv in v if vv in subset] for k, v in expected_exes.items()}
    expected_libs = {k: [vv for vv in v if vv in subset] for k, v in expected_libs.items()}


# TODO: can flopy also store code.json here (or reproduce it in get_modflow.json)?
# this would allow getting expected files from metadata instead of hardcoding them
flopy_appdata_path = (
    Path(os.path.expandvars(r"%LOCALAPPDATA%\flopy"))
    if sys.platform.startswith("win")
    else Path.home() / ".local" / "share" / "flopy"
)
metadata_path = flopy_appdata_path / "get_modflow.json"


def get_expected_files(repository) -> Tuple[List[str], List[str]]:
    metadata = None
    # metadata = json.load(metadata_path.open())
    if metadata:
        from pprint import pprint
        pprint(metadata)
        exes = []
        libs = []
    else:
        exes = expected_exes[repository]
        libs = expected_libs[repository]

    if system() == "Windows":
        exes = [f"{exe}.exe" for exe in exes]
        libs = [f"{lib}.dll" for lib in libs]
    elif system() == "Linux":
        libs = [f"{lib}.so" for lib in libs]
    else:
        libs = [f"{lib}.dylib" for lib in libs]

    return exes, libs


# check install location exists
assert path.is_dir(), f"Install location {path} doesn't exist"
print(f"Found install location: {path}")

# check bin path environment variable is set
env_var = environ.get("MODFLOW_BIN_PATH")
assert env_var
assert Path(env_var).is_dir()

# check executables exist
found = sorted([p.name for p in path.glob("*")])
exp_exes, exp_libs = get_expected_files(repo)
expected = exp_exes + exp_libs
assert set(found) >= set(exp_exes), f"Executables/libraries missing:\n Found {set(found)}\n Expected {set(exp_exes)}"
print(f"Found all expected executables/libraries:")
pprint(expected)

# check executables are on the PATH
for exe in exp_exes:
    assert which(exe), f"Executable {exe} not found on path"
print(f"Verified executables are on system path")


