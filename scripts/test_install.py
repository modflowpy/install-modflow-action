from os import environ
from pathlib import Path
from platform import system
from pprint import pprint
import requests
from shutil import which
import sys


def get_expected_files():
    api_url = environ.get("GITHUB_API_URL")
    if not api_url:
        api_url = "https://api.github.com"

    token = environ.get("GITHUB_TOKEN")
    headers = {"Accept": "application/vnd.github+json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"

    # check release assets for code.json
    response = requests.get(f"{api_url}/repos/MODFLOW-USGS/executables/releases/latest", headers=headers)
    release = response.json()
    metadata = next(iter([a for a in release['assets'] if a['name'] == 'code.json']), None)

    if metadata:
        # TODO download code.json (once added to release assets)
        exp = []
        pass
    else:
        exp = [
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
        ]

    if system() == "Windows":
        exp = [f"{exe}.exe" for exe in exp]
    else:
        # TODO remove if PRMS is added to Windows distribution
        exp += ["prms"]

    return exp


path = Path(sys.argv[1])
if not path:
    raise ValueError(f"Must specify install location")

# check install location exists
assert path.is_dir()
print(f"Found install location: {path}")

# check executables exist
found = sorted([p.name for p in path.glob("*")])
expected = sorted(get_expected_files())
assert set(found) >= set(expected)
print(f"Found all expected executables:")
pprint(expected)

# check executables are on the PATH
for exe in expected:
    assert which(exe)
print(f"Verified executables are on system path")
