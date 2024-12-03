#!/usr/bin/env python
import sys
from pathlib import Path
import os


day = int(sys.argv[1])
dir = Path(f'days/{day}')
input_file_path = len(sys.argv) > 2 and dir / Path(sys.argv[2]) or dir / Path(f'input_d{day}.txt')

script = dir / Path(f'd{day}.py')
cmd = f"python {script} {input_file_path}"
print(cmd)
os.system(cmd)
