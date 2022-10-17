from os import environ
from pathlib import Path
from platform import system
from pprint import pprint
import requests
from shutil import which
import sys

path = Path(sys.argv[1]).expanduser().absolute()
if not path:
    raise ValueError(f"Must specify install location")

repo = sys.argv[2]
if not repo:
    repo = "executables"

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
        'gsflow',
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


def get_expected_files(repository):
    api_url = environ.get("GITHUB_API_URL")
    if not api_url:
        api_url = "https://api.github.com"

    token = environ.get("GITHUB_TOKEN")
    headers = {"Accept": "application/vnd.github+json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"

    # check release assets for code.json
    response = requests.get(f"{api_url}/repos/MODFLOW-USGS/{repository}/releases/latest", headers=headers)
    release = response.json()
    metadata = next(iter([a for a in release['assets'] if a['name'] == 'code.json']), None)

    if metadata:
        # TODO download code.json (once added to release assets)
        exp = []
        pass
    else:
        exp = expected_exes[repository]

    if system() == "Windows":
        exp = [f"{exe}.exe" for exe in exp]
    elif repository == "executables":
        # TODO remove if PRMS is added to Windows distribution
        exp += ["prms"]

    return exp


# check install location exists
assert path.is_dir(), f"Install location {path} doesn't exist"
print(f"Found install location: {path}")

# check executables exist
found = sorted([p.name for p in path.glob("*")])
expected = sorted(get_expected_files(repo))
assert set(found) >= set(expected), f"Executables missing:\n Found {set(found)}\n Expected {set(expected)}"
print(f"Found all expected executables:")
pprint(expected)

# check executables are on the PATH
for exe in expected:
    assert which(exe), f"Executable {exe} not found on path"
print(f"Verified executables are on system path")

# check bin path environment variable is set
env_var = environ.get("MODFLOW_BIN_PATH")
assert env_var
assert Path(env_var).is_dir()
