"""make.fun news-image-20261125 entry: writes the day's news image to /output/entry.png.

The image is rendered once by make_image.py and committed; this program copies it
byte for byte, so every run writes the same bytes with no network.
"""
import os
import shutil

here = os.path.dirname(os.path.abspath(__file__))
# Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output.
out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
os.makedirs(out_dir, exist_ok=True)
shutil.copyfile(os.path.join(here, "entry.png"), os.path.join(out_dir, "entry.png"))
