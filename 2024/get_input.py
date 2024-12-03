#!/usr/bin/env python
from pathlib import Path
import os
import sys
import requests as req
from dotenv import load_dotenv

load_dotenv()
YEAR = 2024

day = int(sys.argv[1])
r = req.get(f"https://adventofcode.com/{YEAR}/day/{day}/input", cookies={"session": os.getenv('SESSION_TOKEN')})

directory = Path(f"days/{day}")
directory.mkdir(exist_ok=True)

## -------- create input file --------
input_filename = Path(f"input_d{day}.txt")
input_path = directory / input_filename
with open(input_path, 'w+') as f:
    print(f'writing input to {input_path}')
    f.write(r.text)

## -------- create script if it doesn't exist yet --------
script_path = directory / Path(f"d{day}.py")
if not script_path.exists():
    with open("./default_template.py") as f:
        script_source = f.read()
    with open(script_path, 'w+') as f:
        f.write(script_source)

os.system('less ' + str(input_path))
os.system(f"zed {script_path}")
