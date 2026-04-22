#!/usr/bin/env python3
"""
Find stream url in har file saved with the F12 devtools method.
from sites (non Youtube) like:
https://www.skylinewebcams.com/ is Google
https://www.earthcam.com/
https://explore.org/livecams works
https://www.panomax.com/en
https://www.google.com/search?q=https://www.roundshot.com/en/webcams.html
https://webcam.nl/live_streaming/ is Youtube
http://www.insecam.org/ is Youtube


Location               Platform         View Description
Venice, Italy          SkylineWebcams   St. Mark's Basin & Rialto Bridge (incredible at sunrise).
ISS (Space)	NASA Live  High-definition  views of Earth from the International Space Station.
Zermatt, Switzerland   Zermatt.ch       Direct HD streams of the Matterhorn from multiple altitudes.
New York City          EarthCam         4K Panoramic "Skyline" view from across the river.
Amsterdam              DamSquare.nl     Rotating HD views of Dam Square and the Royal Palace.

Youtube likes to complain about detected bot activity.
search example skipping youtube and facebook:
city name live webcam -site:youtube.com -site:facebook.com
"""
import re
from CatcherUtilities import service_call,Har_Quick_Reference
import sys
import json
import requests

from icecream import ic
ic.configureOutput(includeContext=True)
import argparse

parser = argparse.ArgumentParser(
	prog='HarUrls.py',
	description='Extract video urls from a "har (HTTP Archive file)\n'\
'a file generated with Firefox or Chrome DevTools (F12)\n'\
'To use in a StreamScreenSaver.py a XScreensaver.' ,
	epilog='Enjoy'
)

parser.add_argument('-v', '--verbose',action='store_true',help="add yt-dlp stream data to the output")
parser.add_argument('-m', '--m3u8'   ,action='store_true',help="look for m3u8 files (default)")
parser.add_argument('-y', '--youtube',action='store_true',help="look for youtube streams")
parser.add_argument('-e', '--explain', action='store_true', help="Some explanation")
parser.add_argument('-p', '--playlist'
                    , action='store_true'
                    , help="Add the contents of a m3u8 file to the output")

parser.add_argument(
    '-l', '--limit',          # The flags
    type=int,                 # Convert input to integer
    default=0,               # If omitted, use 0 no limit
    #choices=range(0, 101),    # Only allow 0 to 100
    help='Onley retrieve limit number of stream urls',
    metavar='N'               # Shows as "--limit N" in help
)
parser.add_argument("infile",nargs='?', help="path to the input file")
parser.add_argument("outfile",default=None,nargs='?',help="path to the file to add the output")
parser.parse_args()

args = parser.parse_args()
m3u8_re=re.compile(r'https://.*\.m3u8')

def Har_M3U8_Urls(file:str,limit:int=0)->list:
	url_set=set()
	url_list=[]
	with open(file, 'r') as file:
		for line in file:
			match=m3u8_re.findall(line)
			if match:
				found_url=match[0]
				if found_url not in url_set:
					print (f'add "{found_url}"')
					url_set.add(found_url)
					new_url={'url':found_url,'name':'No Name'}
					if args.playlist:
						new_url['playlist']=get_playlist(found_url)
					url_list.append(new_url)
					if limit > 0 and len(url_list)>=limit:
						return url_list
	return url_list

def get_playlist(url:str)->str:
	r = requests.get(url)
	if r.status_code == 200:
		return r.text
	print (f'Request for "{url}" failed.')
	error_str= requests.status_codes._codes[r.status_code]
	print(f'{r.status_code} "{error_str}"')
	return error_str
	

def Add_Stream_Info(stream_urls):
	# yt-dlp --dump-json --flat-playlist "https://example.com/playlist.m3u8"
	streams={}
	print ('stream: ',end='')
	for url in stream_urls:
		data=service_call("yt-dlp","--dump-json","--flat-playlist",url)
		print ('x',end='')
		streams[url]= json.loads(data)
	return streams

def output_file_name():
	output_json = args.outfile
	if output_json:
		if output_json[-5:] != '.json':
			output_json += '.json'
		return output_json
	return None
	
def main():
	print(f'{args}')
	if args.explain or not args.infile:
		print (Har_Quick_Reference)
		sys.exit(0)
	streams_url=args.infile
	output_json=args.outfile
	# make m3u8 default
	if not args.m3u8 and not args.youtube:
		args.m3u8=True
	if args.m3u8:
		print ('m3u8')
		streams = Har_M3U8_Urls(streams_url,args.limit)
	if args.youtube:
		print('youtube')
	if args.verbose:
		print('verbose')
		streams = Add_Stream_Info(streams)
		exit(0)
	
	write_file=output_file_name()
	if write_file:
		print ( f'Write results to "{write_file }"')
		with open(write_file, mode="w", encoding="utf-8") as json_file:
			json.dump(streams, json_file,indent=4)
	else:
		print(json.dumps(streams, indent=2))
	
if __name__ == '__main__':
	main()
