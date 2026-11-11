#!/usr/bin/env python3
"""Tests for stamp.py. Run: python3 .github/scripts/test_stamp.py"""
import json
import os
import subprocess
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from stamp import stamp_page, stamp_imports  # noqa: E402

V = 'v1.42'
SPAN = '<span class="version" title="Version">dev</span>'


def check(name, got, want):
    if got != want:
        raise SystemExit('FAIL %s\n  got:  %r\n  want: %r' % (name, got, want))
    print('ok  ', name)


# pages: the version, and every local file a page loads
check('version span', stamp_page(SPAN, V), '<span class="version" title="Version">v1.42</span>')
page = lambda body: stamp_page(SPAN + body, V)[len(SPAN) + 2:]
check('script and stylesheet', page('<script type="module" src="js/main.js"></script><link rel="stylesheet" href="css/app.css">'),
      '<script type="module" src="js/main.js?v=v1.42"></script><link rel="stylesheet" href="css/app.css?v=v1.42">')
check('images, video poster, data', page('<img src="help/open.webp"><video poster="a.png"></video><a href="songs/canon-in-d.mid" download>x</a>'),
      '<img src="help/open.webp?v=v1.42"><video poster="a.png?v=v1.42"></video><a href="songs/canon-in-d.mid?v=v1.42" download>x</a>')
check('single quotes', page("<img src='a.svg'>"), "<img src='a.svg?v=v1.42'>")
for untouched in ['<a href="help.html">', '<a href="./">', '<a href="#top">', '<a href="https://example.com/a.js">',
                  '<script src="//cdn.example.com/a.js">', '<script src="/abs/a.js">', '<img src="a.png?x=1">',
                  '<meta property="og:image" content="https://corey.sciu.to/app/preview.png">', '<a href="mailto:a@b.co">',
                  '<script src="https://cdnjs.cloudflare.com/ajax/libs/d3/7.9.2/d3.min.js">']:
    check('left alone: ' + untouched, page(untouched), untouched)
try:
    stamp_page('<p>no span</p>', V)
    raise SystemExit('FAIL a page without the span should be an error')
except SystemExit as e:
    if 'FAIL' in str(e):
        raise
    print('ok   a page without the version span is an error')

# scripts: every way one module names another
for src, want in [
    ("import { a } from './a.js';", "import { a } from './a.js?v=v1.42';"),
    ('import{a}from"../utils/a.js"', 'import{a}from"../utils/a.js?v=v1.42"'),
    ("import './side-effect.js';", "import './side-effect.js?v=v1.42';"),
    ("const m = await import('./presets.js');", "const m = await import('./presets.js?v=v1.42');"),
    ("export { keyFor } from './midi.js';", "export { keyFor } from './midi.js?v=v1.42';"),
    ("addModule(new URL('./worklets.js', import.meta.url).href)", "addModule(new URL('./worklets.js?v=v1.42', import.meta.url).href)"),
    ("import {\n  a,\n  b,\n} from './controls.js';", "import {\n  a,\n  b,\n} from './controls.js?v=v1.42';"),
    ("import x from './a.mjs'", "import x from './a.mjs?v=v1.42'"),
]:
    check('import: ' + src.replace('\n', ' ')[:50], stamp_imports(src, V), want)
for untouched in ["import d3 from 'https://cdn.example.com/d3.js';", "import x from 'bare-package';", "const s = './not-an-import.js';",
                  "import a from './a.js?v=old';", "fetch('data.json')", "const important = './x.js';", "x.from('./a.js')" if False else "new URL(location.href)"]:
    check('left alone: ' + untouched, stamp_imports(untouched, V), untouched)

# the whole run, in a folder like a site
with tempfile.TemporaryDirectory() as d:
    os.makedirs(os.path.join(d, 'js', 'audio'))
    files = {
        'index.html': SPAN + '<script type="module" src="js/main.js"></script>',
        'help.html': '<p>not listed, no span</p><script type="module">import "./js/main.js";</script>',
        'js/main.js': "import { e } from './audio/engine.js';",
        'js/audio/engine.js': "export const e = new URL('./worklets.js', import.meta.url);",
    }
    for name, text in files.items():
        with open(os.path.join(d, name), 'w') as f:
            f.write(text)
    script = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'stamp.py')
    subprocess.run([sys.executable, script, V, 'abc1234', '2026-11-11', 'index.html'], cwd=d, check=True, stdout=subprocess.DEVNULL)
    read = lambda name: open(os.path.join(d, name)).read()
    check('run: page', read('index.html'), '<span class="version" title="Version">v1.42</span><script type="module" src="js/main.js?v=v1.42"></script>')
    check('run: nested module', read('js/main.js'), "import { e } from './audio/engine.js?v=v1.42';")
    check('run: worklet', read('js/audio/engine.js'), "export const e = new URL('./worklets.js?v=v1.42', import.meta.url);")
    check('run: inline module in an unlisted page', read('help.html'), '<p>not listed, no span</p><script type="module">import "./js/main.js?v=v1.42";</script>')
    check('run: version.json', json.loads(read('version.json')), {'version': V, 'commit': 'abc1234', 'date': '2026-11-11'})
    missing = subprocess.run([sys.executable, script, V, 'abc', '2026-11-11', 'help.html'], cwd=d, capture_output=True, text=True)
    check('run: a listed page without the span fails the deploy', (missing.returncode != 0, 'help.html' in missing.stderr), (True, True))
print('all passed')
