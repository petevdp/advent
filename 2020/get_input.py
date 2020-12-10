#!/usr/bin/env python

import sys
import os
import requests as req
from dotenv import load_dotenv
load_dotenv()

day = int(sys.argv[1])
r = req.get(f"https://adventofcode.com/2020/day/{day}/input", cookies={"session": os.getenv('SESSION_TOKEN')})

directory = f"days/{day}"
if not os.path.exists(directory):
    os.mkdir(directory)
    
input_path = f'days/{day}/input'
with open(input_path, 'w+') as f:
    print(f'writing input to {input_path}')
    f.write(r.text)
