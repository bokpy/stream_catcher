#You  said  I just want to find all streams of explore.org to use in a screensaver and save them in a json file 
#using python a things like yt - dlp, wget, curl etc. with subprocess or popen. 	Gemini 	said  Since you want to automate this for a screensaver, using Python with yt-dlp is the most robust way to handle the modern JavaScript-heavy nature of Explore.org.  While wget or curl can download the HTML, they can 't "click" or run the scripts that reveal the actual .m3u8 stream URLs. yt-dlp handles that heavy lifting for you. 1. Prerequisite  You 'll need yt-dlp installed. You can get it via pip: Bash  pip install yt - dlp  2. Python Script to Extract & Save to JSON  This script uses subprocess to run yt - dlp.It crawls the main livecams page, finds the individual cam links, and then extracts the direct stream URL for each. 	Python  import subprocess import json import re 
# Base URL for Explore.org live cams

import subprocess
import json

BASE_URL = "https://explore.org/livecams"


def get_stream_urls():
	streams_data = []

	print(f"--- Fetching camera links from {BASE_URL} ---")

	# Step 1: Use yt-dlp to find all sub-page links (the individual cams)
	# --get-id just returns the unique IDs/slugs of the cams found on the page
	try:
		cmd_flat = [
			"yt-dlp",
			"--get-id",
			"--flat-playlist",
			BASE_URL
		]
		result = subprocess.run(cmd_flat, capture_output=True, text=True, check=True)
		cam_ids = result.stdout.strip().split('\n')
	except subprocess.CalledProcessError as e:
		print(f"Error fetching cam list: {e}")
		return []

	print(f"Found {len(cam_ids)} potential cameras. Extracting stream URLs...")

	# Step 2: For each cam, get the direct .m3u8 manifest URL
	for cam_id in cam_ids:
		# Construct the full URL for the specific camera
		cam_url = f"https://explore.org/livecams/{cam_id}"

		try:
			# -g: Get the URL (the stream)
			# --format best: Ensure we get the highest quality stream
			cmd_stream = ["yt-dlp", "-g", "--format", "best", cam_url]
			stream_result = subprocess.run(cmd_stream, capture_output=True, text=True)

			if stream_result.returncode == 0:
				stream_url = stream_result.stdout.strip()
				streams_data.append({
					"name": cam_id.replace('-', ' ').title(),
					"page_url": cam_url,
					"stream_url": stream_url
				})
				print(f"Success: {cam_id}")
			else:
				print(f"Skipping: {cam_id} (No stream found)")

		except Exception as e:
			print(f"Failed to process {cam_id}: {e}")

	return streams_data


# Save to JSON
if __name__ == "__main__":
	data = get_stream_urls()

	with open("explore_streams.json", "w") as f:
		json.dump(data, f, indent=4)

	print(f"\nDone! Saved {len(data)} streams to explore_streams.json")

# How this works for your screensaver: 	The 	Crawl: The 	script 	uses - -flat - playlist 	on 	the 	main / livecams 	page.This is like 	a 	"shallow" 	crawl—it 	finds 	the 	links 	to 	all 	the 	specific 	cameras 	without 	actually 	visiting 	them 	yet.  	The 	Extraction: It 	then 	visits 	each 	camera 	URL 	one - by - one.yt - dlp 	acts 	like 	a 	mini - browser 	to 	find 	the 	HLS(.m3u8) stream 	hidden in the 	page 	logic.  	The 	Output: You 	get 	a 	clean 	explore_streams.json 	that 	looks 	like 	this:
# 	JSON
#
# 	[
# 		{
# 			"name": "Grace Gorilla Cam",
# 			"page_url": "https://explore.org/livecams/grace-gorilla-cam",
# 			"stream_url": "https://.../playlist.m3u8"
# 		}
# 	]
#  Important Tips:  Stream Expiration: Direct.m3u8 URLs for live streams often have "tokens" or expiration timestamps in them.If your screensaver stops working after a few hours, you may need to run the Python script again to refresh the URLs.  yt - dlp Updates: Sites like Explore.org change their layout often.If the script stops working, run yt - dlp - U to update the tool to the latest version.  Performance: The script processes cams one by one.If it 's too slow, you could use Python' s concurrent.futures to run multiple subprocess calls at once.
