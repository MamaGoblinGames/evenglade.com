# evenglade.com

The website for Evenglade, a calm home screen for Android: https://evenglade.com.

This repository holds the finished site, published by GitHub Pages from `docs/`. Everything outside
`docs/` stays in the repository but isn't served.

Each guide on `docs/guides.html` also has a page of its own, with just its video, at
`docs/watch/<guide>.html`. After changing `docs/guides.html`, write those again with:

    python3 tools/watch-pages.py
