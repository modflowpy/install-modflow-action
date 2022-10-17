import os
import sys

path = sys.argv[1]
if path.startswith('/'):
    print(path)
elif path.startswith('~'):
    print(os.path.expanduser(path))
else:
    print(os.path.realpath(os.path.join(os.getcwd(), path)))