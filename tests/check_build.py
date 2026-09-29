#!/usr/bin/env python3
"""Check a generated site: python3 themes/yohaku/tests/check_build.py BUILD_DIR."""
import json
import re
import struct
import sys
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urljoin, urlsplit

root = Path(sys.argv[1]).resolve()

class Page(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.links, self.css, self.canonical = [], [], ''
        self.feed(text)
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == 'a' and a.get('href'):
            self.links.append(a['href'])
        if tag == 'link' and 'stylesheet' in a.get('rel', ''):
            self.css.append(a['href'])
        if tag == 'link' and a.get('rel') == 'canonical':
            self.canonical = a['href']

def target(url):
    path = root / unquote(urlsplit(url).path).lstrip('/')
    return path / 'index.html' if path.is_dir() else path

index = json.loads((root / 'index.json').read_text())
urls = [p['permalink'] for p in index]
assert len(urls) == len(set(urls)), 'Duplicate search index entries'
for url in urls:
    assert target(url).is_file(), f'Missing indexed article: {url}'

home = Page((root / 'index.html').read_text())
host = urlsplit(home.canonical).netloc
for file in root.rglob('*.html'):
    page = Page(file.read_text())
    if not page.canonical:  # Redirect aliases have no canonical metadata.
        continue
    for href in page.links:
        url = urljoin(page.canonical, href)
        if urlsplit(url).netloc == host:
            assert target(url).is_file(), f'Broken link in {file}: {url}'
for href in home.css:
    cssfile = target(href)
    css = cssfile.read_text()
    assert css.count('@font-face') == 202, 'Expected 400/500 Unicode font faces'
    assert 'LXGW WenKai'.lower() not in css.lower(), 'Legacy font leaked'
    assert 'alert-heading::before' not in css, 'Legacy alert appearance leaked'
    for url in re.findall(r'url\([\'"]?([^\)\'\"]+)', css):
        assert not url.startswith('http'), f'External stylesheet asset: {url}'
        assert (cssfile.parent / url).resolve().is_file(), f'Missing CSS asset: {url}'

fonts = list((root / 'fonts/noto-serif-sc').glob('*.woff2'))
assert len(fonts) == 101
for file in fonts:
    data = file.read_bytes()
    assert data[:4] == b'wOF2'
    assert struct.unpack('>I', data[8:12])[0] == len(data), f'Truncated font: {file}'
assert 'SIL OPEN FONT LICENSE' in (root/'fonts/noto-serif-sc/OFL.txt').read_text()
ET.parse(root/'index.xml')
assert (root/'404.html').is_file()
print(f'PASS: {len(index)} indexed articles, internal links, CSS assets, 101 WOFF2 files, license, RSS and 404.')
