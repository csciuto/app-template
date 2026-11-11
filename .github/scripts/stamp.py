#!/usr/bin/env python3
"""Stamp a site for publishing. Run in the site folder by the shared workflow (app.yml):

    python3 stamp.py <version> <commit> <date> [page ...]

1. Each page listed gets the version in its <span class="version" title="Version">dev</span>.
2. Every reference from one file of the site to another gets ?v=<version>:
     - in the listed pages: local src, href and poster attributes (scripts, styles, images, fonts, data)
     - in every .js and .html file: relative ES-module imports, dynamic imports, and
       new URL('./x.js', import.meta.url) (how workers and audio worklets are loaded)
   GitHub Pages lets browsers keep files for ten minutes. Without this, a reload after a deploy can run the
   new page with old scripts, or new scripts importing old ones. With it, a new version's files have new
   addresses, so one reload gets all of it.
3. version.json is written: {"version", "commit", "date"}.

Data a script fetches by a built-up address (fetch(`data/${name}.json`)) can't be found this way; an app
adds the version itself, from the page's version span (STANDARDS.md).
"""
import json
import os
import re
import sys

ASSET = r"js|mjs|css|png|jpe?g|webp|gif|svg|ico|woff2?|json|mid|ogg|mp3|wav"
# src="x.js" href="css/a.css" poster="a.png": local (no scheme, not //host, not #anchor), no query yet
ATTR = re.compile(r'''\b(src|href|poster)=(["'])(?!//|/|#)([^"'?#:\s]+\.(?:%s))\2''' % ASSET)
# from './x.js'   import './x.js'   import('./x.js')   new URL('./x.js', ...
IMPORT = re.compile(r'''(\bfrom\s*|\bimport\s*\(?\s*|\bnew\s+URL\(\s*)(["'])(\.{1,2}/[^"'?\s]+\.m?js)\2''')
SPAN = 'title="Version">dev<'


def stamp_page(text, version):
    """A listed page: the version span, then its local references."""
    if SPAN not in text:
        raise SystemExit('no <span class="version" title="Version">dev</span> to stamp')
    text = text.replace(SPAN, 'title="Version">%s<' % version)
    return ATTR.sub(lambda m: '%s=%s%s?v=%s%s' % (m[1], m[2], m[3], version, m[2]), text)


def stamp_imports(text, version):
    """Any script: relative module references."""
    return IMPORT.sub(lambda m: '%s%s%s?v=%s%s' % (m[1], m[2], m[3], version, m[2]), text)


def main(version, commit, date, pages):
    for page in pages:
        with open(page, encoding='utf-8') as f:
            text = f.read()
        try:
            text = stamp_page(text, version)
        except SystemExit as e:
            raise SystemExit('%s: %s' % (page, e))
        with open(page, 'w', encoding='utf-8') as f:
            f.write(text)
    for root, dirs, files in os.walk('.'):
        dirs[:] = [d for d in dirs if d not in ('.git', 'node_modules')]
        for name in files:
            if not name.endswith(('.js', '.mjs', '.html')):
                continue
            path = os.path.join(root, name)
            with open(path, encoding='utf-8') as f:
                text = f.read()
            new = stamp_imports(text, version)
            if new != text:
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(new)
    with open('version.json', 'w', encoding='utf-8') as f:
        json.dump({'version': version, 'commit': commit, 'date': date}, f, separators=(',', ':'))
        f.write('\n')
    print('Stamped', version, 'on', ', '.join(pages) or 'no pages')


if __name__ == '__main__':
    if len(sys.argv) < 4:
        raise SystemExit(__doc__)
    main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4:])
