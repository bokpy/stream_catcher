#!/usr/bin/env python3
import m3u8
import requests


def get_media_urls(playlist_url):
	"""
	Parses an m3u8 playlist and returns a list of absolute URLs for segments.
	"""
	try:
		# Fetch the content of the m3u8 file
		response = requests.get(playlist_url)
		response.raise_for_status()
		
		# Parse the playlist
		# Passing base_uri allows the library to automatically convert
		# relative segment paths into absolute URLs.
		playlist = m3u8.loads(response.text, uri=playlist_url)
		
		# If this is a master playlist, it contains links to other playlists
		if playlist.is_variant:
			print("Master playlist detected. Extracting first available stream...")
			variant_url = playlist.playlists[0].absolute_uri
			return get_media_urls(variant_url)
		
		# Extract absolute URIs for all media segments (.ts files)
		return [segment.absolute_uri for segment in playlist.segments]
	
	except Exception as e:
		print(f"Error fetching or parsing playlist: {e}")
		return []


# Example Usage:
target_url = "https://outbound-production.explore.org/stream-production-127/.m3u8"
urls = get_media_urls(target_url)

for url in urls[:5]:  # Print first 5 for brevity
	print(url)
