#!/usr/bin/env python3
"""
Gererate or update a cookies.txt file in '~/.mozilla/firefox/xxxxxxxx.default-release-1/"
from file "~/.mozilla/firefox/tm6cn9wu.default-release-1/cookies.sqlite"
"""


import glob
from pathlib import Path
import sys
import requests
import subprocess
import random
import time
import json


HOME=str(Path.home())
GLOBBER="/.mozilla/firefox/*.default-release-1/cookies.sqlite"

from icecream import ic
ic.configureOutput(includeContext=True)

def cookie_monster():
	cookies_sqlite_files = glob.glob(HOME+GLOBBER)
	if len(cookies_sqlite_files) == 0:
		print(f'No cookie file found in: "{HOME+GLOBBER}"')
		sys.exit(1)
	cookie_file = cookies_sqlite_files[0]
	cookie_txt_file = cookie_file.replace("/cookies.sqlite","/cookies.txt")
	if len(cookies_sqlite_files) > 1:
		print(f'found: {cookies_sqlite_files}')
		print (f'use "{cookie_file}"')
	try:
		info = subprocess.check_output(["sqlite3",cookie_file,".headers on",".mode ascii","SELECT * FROM moz_cookies;"]
		,stderr = subprocess.STDOUT)
		str_info = info.decode('utf-8')
		with open(cookie_txt_file,'w') as file:
			file.write(str_info)
		return str_info
	except subprocess.CalledProcessError as sqlite3_error:
		print("Error:", sqlite3_error.returncode)
		print("Output:", sqlite3_error.output.decode('utf-8'))
		if sqlite3_error.returncode == 5:
			print('Close all Firefoxes first and retry.')
		exit(sqlite3_error.returncode)

	except subprocess.SubprocessError as e:
		print(f"Return code: {e.returncode}")
		print(f"Command: {e.cmd}")
		print(f"Output: {e.output}")
		print(f"Stderr: {e.stderr}")
		exit(e.returncode)
	return ''

if __name__ == '__main__':
	cookie_text=cookie_monster()
	ic(cookie_text)
