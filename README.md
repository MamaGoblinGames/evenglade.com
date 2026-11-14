# evenglade.com

The website for Evenglade, a calm home screen for Android: https://evenglade.com.

This repository holds the finished site, published by GitHub Pages from `docs/`. Everything outside
`docs/` stays in the repository but isn't served.

The site is built in the app's repository, from `design/landing`, including each guide's page of its own
with just its video (`docs/watch/<guide>.html`). Build it into this repository's `docs/` with:

    python3 design/landing/build.py --out ../evenglade.com/docs
