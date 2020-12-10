#!/usr/bin/env python

import requests as req
import os
from bs4 import BeautifulSoup
import pypandoc
import html2markdown
import sys
from dotenv import load_dotenv
load_dotenv()

DAYS_AVAILABLE = int(sys.argv[1])
print(DAYS_AVAILABLE)

days = [str(d) for d in range(1, DAYS_AVAILABLE + 1)]
for day in days:
    r = req.get(f"https://adventofcode.com/2020/day/{day}", cookies={"session": os.getenv('SESSION_TOKEN')})
    soup = BeautifulSoup(r.text, 'html.parser')
    parts = soup.find_all(class_="day-desc")
    directory = f"days/{day}"
    if not os.path.exists(directory):
        os.mkdir(directory)
    for i, part in enumerate(parts):
        path = f"days/{day}/part{i+1}.md"
        with open(path, 'w+') as f:
            f.write(pypandoc.convert_text(str(part), 'md', format="html"))
