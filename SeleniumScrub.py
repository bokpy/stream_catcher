#!/usr/bin/env python3
import re
import sys
import atexit

import os
import copy
import requests
import subprocess
import random
import time
import json


from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.set_capability("goog:loggingPrefs", {"performance": "ALL"})
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()),options=chrome_options)
driver.execute_cdp_cmd("Network.enable", {})

@atexit.register
def quit_chrome():
	global driver
	if driver == None:
		print( 'Chrome was allready closed')
		return
	print (f'Closing: Chrome webdriver')
	time.sleep(10)
	driver.quit()
	driver = None
	
from icecream import ic
ic.configureOutput(includeContext=True)

# # Add a directory to PATH
# new_path = '/home/bob/python/stream_catcher/chrome/chrome - linux64'
# if new_path not in os.environ['PATH']:
#     os.environ['PATH'] += os.pathsep + new_path
#
# new_path = '/home/bob/python/stream_catcher/chrome/chromedriver-linux64'
# if new_path not in os.environ['PATH']:
#     os.environ['PATH'] += os.pathsep + new_path
# driver=None

class SiteData:
	def __init__(S,site_url,user_name=None,password=None,cookie_file=None):
		S.site_url   = site_url
		S.user_name  = user_name
		S.password   = password
		S.cookie_file= cookie_file
		
	def __repr__(S):
		ret = S.site_url
		if S.user_name:
			ret = ret +'",user_name="' + S.user_name
		if S.password:
			ret = ret +'",password="' + S.password
		if S.cookie_file:
			ret = ret +'",cookie_file="' + S.cookie_file
		return 'SiteData("' + ret + '")'
	
	def url(S):
		return S.site_url
	

def M3U8_Scruber(site:SiteData) -> set:
	m3u8_urls = set()
	global driver
	'''Find m3u8 streams on a site and return the urls in a list'''
	ic(site.url())
	
	driver.get(site.url())
	print(f'{driver.title=}')
	time.sleep(30)
	logs = driver.get_log("performance")
	#print(logs)
	for entry in logs:
		log = json.loads(entry["message"])["message"]
		if log["method"] == "Network.responseReceived":
			url = log["params"]["response"]["url"]
			if ".m3u8" in url:
				m3u8_urls.add(url)
	return m3u8_urls
	

def main():
	global driver
	explore_data = SiteData("https://www.explore.org/livecams/explore-all-cams/seasons",
	                       "son_of_down", "Wild:<{2go")
	evdev_data   = SiteData('https://python-evdev.readthedocs.io/en/latest/')
	
	streams = M3U8_Scruber(explore_data)
	
if __name__ == '__main__':
	main()
