# news-image-20261125

[![make.fun · news-image-20261125](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/bounty/news-image-20261125)

The world's news of Wednesday 25 November 2026 in one image: "The World's Oil Is On Fire".
Houthis strike Saudi Arabia's Ras Tanura refinery, mined tankers burn in the Strait of Hormuz,
Ukraine's refinery strikes go on, plus Libya, Gaza and the WFP's hunger warning.

`make_image.py` renders `entry.png` once (Pillow); `main.py` copies it to `/output/entry.png`,
so every run writes the same bytes with no network.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python main.py
```
