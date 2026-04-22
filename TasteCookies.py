#!/usr/bin/env python3
import os

COOKIES_FILE=''
"""
It’s a classic "cat and mouse" game. YouTube has significantly ramped up its bot detection lately, specifically targeting automated tools like `yt-dlp`. If you're getting blocked even with a cookies file, it usually means your cookies are either expired, formatted incorrectly, or your IP address has been flagged alongside the session.

Here is how you can systematically test your `cookies.txt` and trace where the handshake is failing.

---

## 1. Verify Cookie Format and Validity
`yt-dlp` is picky about the cookie format. It generally prefers the **Netscape/Mozilla** format.

* **Check the Header:** Open your `.txt` file."""

def header_check():
	global COOKIES_FILE
	with open(COOKIES_FILE,'r') as f:
		first_line = f.readline()
		if "# Netscape HTTP Cookie File" in first_line:
			return
	print("""Header does not start with: `# Netscape HTTP Cookie File`
Your export tool might be the issue.
* **Use a Reliable Extension:** If you're exporting from a browser, use **"Get cookies.txt LOCALLY"** (Chrome/Edge) or **"cookie-editor"** (Firefox). Avoid "copy-paste" methods that might mangle the tabs/spacing.
* **The "Freshness" Test:** Log into YouTube in your browser, click a few videos, and *then* export. If you log out of the browser, the cookies you just exported often become instantly invalid.
""")
	exit(1)
"""
---

## 2. Test with a "Quiet" Command
Before diving into complex traces, run a simple check to see if `yt-dlp` can even "see" your account status.

```bash
yt-dlp --cookies cookies.txt --get-filename -o "%(uploader)s" https://www.youtube.com/watch?v=VIDEO_ID
```
* **Success:** It prints the uploader's name.
* **Failure:** It throws a `403 Forbidden` or a sign-in requirement error.

---

## 3. Trace the Problem (Verbose Mode)
To see exactly what YouTube is saying back to you, use the `--verbose` flag. This is your best diagnostic tool.

```bash
yt-dlp --cookies cookies.txt --verbose https://www.youtube.com/watch?v=VIDEO_ID
```

**What to look for in the output:**
* **`[debug] Loading cookies from...`**: Ensure it actually finds and loads the number of cookies you expect.
* **`HTTP Error 403: Forbidden`**: This usually means your cookies are detected as a bot or your IP is rate-limited.
* **`Sign in to confirm you’re not a bot`**: This indicates the cookies are being ignored or have been invalidated by YouTube's "PoToken" (Proof of Token) requirement.

---

## 4. Advanced Troubleshooting
If your cookies are valid but you're still blocked, YouTube might be demanding a **visitor data token** or using **OAuth2**.

### Try the OAuth2 Plugin
Instead of manual cookies, many users are switching to the `yt-dlp-get-oauth2` flow.
1. Install it (if you use python/pip): `pip install yt-dlp-get-oauth2`
2. Run `yt-dlp --username oauth2 --password ''`.
3. Follow the on-screen instructions to authorize via a code on your phone/browser. This is often more stable than `cookies.txt`.

### Match the User-Agent
Sometimes YouTube blocks you because your browser's cookies don't match the "identity" `yt-dlp` is claiming. Try passing your browser's User-Agent string:
```bash
yt-dlp --cookies cookies.txt --user-agent "YOUR_BROWSER_USER_AGENT_HERE" URL
```

> **A Quick Tip:** If you're on a VPS (like AWS or DigitalOcean), YouTube often blocks those IP ranges entirely regardless of cookies. Testing on a home connection or a high-quality residential proxy is usually the only fix there.

How does the verbose output look when you run it? If you see a specific error code like `429` or `sign-in-requirement`, let me know!

"""

import argparse

parser = argparse.ArgumentParser(
	prog='TasteCookies.py',
	description="Try to find if there is something Youtube/Google doesn't like",
	epilog="Don't dispare"
)
#                , nargs='?'
#                     , help="Saved file format use ffmpeg -codecs to see all"
#                     )
# parser.add_argument('-b', '--bitrate'
#                     , type= int
#                     , default=192
#                     , nargs='?'
#                     , help="Preverded bitrate"
#                     )
# parser.add_argument('-c', '--cookies'
#                     , choices=['saved','brave','chrome','mozilla','firefox']
#                     , default='saved'
#                     , nargs='?'
#                     , help="which cookies to use"
#                     )
#
# parser.add_argument('-C', '--Cookies'
#                     , nargs='?'
#                     , help="full path to a cookies.txt file."
#                     )
# parser.add_argument('-u', '--username'
#                     , nargs='?'
#                     , help="a username for youtube."
#                     )
# parser.add_argument('-p', '--password'
#                     , nargs='?'
#                     , help="a password for youtube."
#                     )

parser.add_argument('cookies',help="Full path + filename of file to check.")
parser.parse_args()
args = parser.parse_args()

def main():
	global COOKIES_FILE
	COOKIES_FILE = args.cookies
	if not os.path.isfile(COOKIES_FILE):
		print (f'No cookies file at "{COOKIES_FILE} found')
		exit(1)
	header_check()
	
if __name__ == "__main__":
	print(args)
	main()
