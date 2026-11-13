#!/usr/bin/env python3
"""Writes watch/<guide>.html, a page with just one guide's video, for each guide in guides.html.

Evenglade's walkthrough links each step to the guide that shows it, and on a phone a page with one
video, ready to play, is easier than the whole guides page. Run this after changing guides.html:

    python3 tools/watch-pages.py
"""
import html
import textwrap
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
GUIDES = (ROOT / "guides.html").read_text()
OUT = ROOT / "watch"

PAGE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title} · Evenglade</title>
<meta name="description" content="{description}">
<meta name="robots" content="noindex, follow">
<meta name="theme-color" content="#8A9C80">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="canonical" href="https://evenglade.com/guides#{slug}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Google+Sans+Flex:wght@300..700&family=Google+Sans+Code:wght@400..700&display=swap">
<link rel="stylesheet" href="/style.css">
</head>
<body>

<!-- Written by tools/watch-pages.py from guides.html; change that, then run it again. -->
<main class="watch">
  <div class="wrap">
    <a class="mono soft" href="/guides">Evenglade <span aria-hidden="true">//</span> Guides</a>
    <video controls playsinline autoplay muted preload="metadata" poster="/video/{slug}.jpg" width="1080" height="1920" aria-label="{title}, a video without sound"><source src="/video/{slug}.mp4" type="video/mp4"></video>
    <div class="text">
      <p class="mono soft">{length}</p>
      <h1>{title}</h1>
{text}
      <p class="soft back">When you're done, swipe back to return to Evenglade.</p>
      <p class="soft"><a href="/guides#{slug}">All the guides</a></p>
    </div>
  </div>
</main>

</body>
</html>
"""


def main():
    OUT.mkdir(exist_ok=True)
    for slug, body in re.findall(r'<article class="guide" id="([^"]+)">(.*?)</article>', GUIDES, re.S):
        title = re.search(r"<h2>(.*?)</h2>", body, re.S).group(1)
        # "01 / 1 min" on the guides page; here, only the length.
        length = re.search(r'<p class="mono soft">.*?</span>\s*(.*?)</p>', body, re.S).group(1)
        description = re.search(r"</h2>\s*<p>(.*?)</p>", body, re.S).group(1)
        # The description and the steps in words, as they are on the guides page, with links between
        # guides leading to their own pages.
        text = re.search(r'<div class="text">(.*)</div>', body, re.S).group(1)
        text = re.sub(r'\s*<p class="mono soft">.*?</p>\s*<h2>.*?</h2>', "", text, count=1, flags=re.S)
        text = re.sub(r'href="#([^"]+)"', r'href="/watch/\1"', text)
        text = textwrap.indent(textwrap.dedent(text).strip("\n"), " " * 6)
        plain = html.escape(html.unescape(re.sub(r"<[^>]+>", "", description)), quote=True)
        page = PAGE.format(slug=slug, title=title, length=length, description=plain, text=text)
        (OUT / f"{slug}.html").write_text(page)
        print(f"watch/{slug}.html")


if __name__ == "__main__":
    main()
