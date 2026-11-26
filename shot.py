#!/usr/bin/env python3
"""截图检查：python3 shot.py <file> <hash|-> <out.png> [width] [height|full] [dark]"""
import sys, pathlib
from playwright.sync_api import sync_playwright

f, h, out = sys.argv[1], sys.argv[2], sys.argv[3]
w = int(sys.argv[4]) if len(sys.argv) > 4 else 1280
hh = sys.argv[5] if len(sys.argv) > 5 else 'full'
dark = len(sys.argv) > 6 and sys.argv[6] == 'dark'
url = pathlib.Path(f).resolve().as_uri() + ('' if h == '-' else '#' + h)
with sync_playwright() as p:
    b = p.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--no-sandbox'])
    pg = b.new_page(viewport={'width': w, 'height': 900 if hh == 'full' else int(hh)},
                    color_scheme='dark' if dark else 'light', device_scale_factor=1)
    pg.goto(url)
    pg.wait_for_timeout(300)
    pg.screenshot(path=out, full_page=(hh == 'full'))
    b.close()
print(out)
