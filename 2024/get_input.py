#!/usr/bin/env python
from pathlib import Path

import sys
import os
import requests as req
from dotenv import load_dotenv

load_dotenv()
YEAR = 2024

day = int(sys.argv[1])
r = req.get(f"https://adventofcode.com/{YEAR}/day/{day}/input", cookies={"session": os.getenv('SESSION_TOKEN')})

directory = Path(f"days/{day}")
directory.mkdir(exist_ok=True)

input_filename = Path(f"input_d{day}.txt")
input_path = directory / input_filename
with open(input_path, 'w+') as f:
    print(f'writing input to {input_path}')
    f.write(r.text)
script_path = directory / Path(f"d{day}.py")
with open(script_path, 'w+') as f:
    f.write(f"with open('{input_filename}') as f:\n    pass")
