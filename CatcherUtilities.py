import os
import subprocess
import os
CONFIG_DIR=os.path.expanduser('~') + '/.config/stream_catcher/'

def service_call(*args):
	sub_name = args[0]
	try:
		info = subprocess.check_output(args, stderr=subprocess.STDOUT)
		str_info = info.decode('utf-8')
		return str_info
	
	except subprocess.CalledProcessError as sub_error:
		print(f'Called {sub_name} Failed.')
		print("Error:", sub_error.returncode)
		print("Output:", sub_error.output.decode('utf-8'))
	except subprocess.SubprocessError as e:
		print(f'{sub_name} Failed.')
		print(f'{args} failed')
		print(f'subprocess.SubprocessError {e}')
	return 1

Har_Quick_Reference='''Quick Guide:\n\nExtracting Streams to .HAR
If you need to capture stream URLs in bulk or save the session for later analysis,
follow this sequence in the

In Firefox or Chrome visit the site you want to extract streams from.
Monitor ➔ press F12:
Network ➔ select the "network" tab
All     ➔ select under the "network" tab "All"
Headers ➔ select under the "All" tab "Header"
          # Clicking on a line in the left panel shows in the right panel among other the url of the stream.
Filter  ➔ Click the funnel icon and type .m3u8 to hide irrelevant traffic.
Clear   ➔ Click the "trash/circle-slash" icon to wipe the current list so you start with a clean slate.
Record  ➔ Ensure the "circle with dot" is red (active). This is the "record" state.
Capture ➔ Play the video/refresh the page. Let the requests populate the list.
Stop    ➔ Click the "circle with dot" again (it will turn grey) to freeze the capture and prevent extra data from cluttering your view.
Export (Chrome)  ➔ Click the "down arrow with horizontal line" icon (Save/Export HAR) to save the entire network log as a .har file.
Export (Firefox) ➔ Right Click "on a line in the left panel" Select "save All as HAR"
'''

Youtube__Reference='''
To extract YouTube video URLs from a search results page using the Developer Tools (**F12**), you have to look for the background **XHR/Fetch** requests that YouTube uses to load its data. YouTube doesn't just send a simple list of links; it sends a complex JSON object called `search`.

Here is the step-by-step procedure to capture these and export them.

### 1. The Capture Procedure (F12)
1.  Open Firefox and go to [youtube.com](https://youtube.com) and perform your search.
2.  Press **F12** and go to the **Network** tab.
3.  **Filter:** In the filter box, type `search?`. This isolates the specific data packets containing video metadata.
4.  **Clear:** Click the **trash/circle-slash** icon to clear old traffic.
5.  **Record:** Scroll down the YouTube page to trigger "Infinite Scroll." You will see new `search?` entries appear in the list.
6.  **Export:** Once you have scrolled enough, click the **down arrow** (Export HAR) to save the file (e.g., `youtube_results.har`).

---

### 2. Extracting URLs from the HAR file
Because YouTube data is nested deep within a JSON structure (under `contents` -> `twoColumnSearchResultsRenderer`), a simple `grep` might fail. Here is a Python script to clean that HAR file and give you a list of full video URLs.

```python
import json
import re

def extract_youtube_urls(har_file_path):
    with open(har_file_path, 'r', encoding='utf-8') as f:
        har_data = json.load(f)

    video_ids = set()
    
    for entry in har_data['log']['entries']:
        # We look for the responses containing the search data
        if 'search?' in entry['request']['url']:
            content = entry['response'].get('content', {}).get('text', '')
            
            # Find videoIds using regex within the JSON text
            # YouTube video IDs are 11 characters
            matches = re.findall(r'"videoId":"([^"]+)"', content)
            for m in matches:
                video_ids.add(m)

    # Print the full URLs
    for v_id in sorted(video_ids):
        print(f"https://www.youtube.com/watch?v={v_id}")

# Usage (ensure you use the raw string r'' if path has brackets!)
extract_youtube_urls(r'path/to/your/youtube_results.har')
```

---

### 3. The "Quick & Dirty" Console Method
If you don't want to deal with a HAR file and just want the links **right now** while the page is open:
1.  Stay in the **F12** tools, but click the **Console** tab.
2.  Paste this code and hit **Enter**:

```javascript
var links = document.querySelectorAll('a#video-title');
var urls = Array.from(links).map(a => "https://www.youtube.com" + a.getAttribute('href').split('&')[0]);
console.log(urls.join('\n'));
```

### Why use the HAR method over the Console?
* **Completeness:** The Console only sees what is currently "rendered" on your screen. The HAR file captures the raw data sent by the server, which often includes more metadata (like view counts, thumbnails, and descriptions) that hasn't even been displayed yet.
* **Automation:** You can save the HAR and process it later with your `stream_catcher` script.

Are you looking to capture just the video links, or do you also need the specific `.m3u8` stream segments for these YouTube videos? (Note: YouTube uses DASH/m4s more commonly than m3u8).
'''
