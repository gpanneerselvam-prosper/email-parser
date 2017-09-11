from subprocess import call
from string import Template
import codecs
import json
import os


def generate_pdf():
    try:
        # generate the PDF from the ready_for_generation.html
        call(["phantomjs", "rasterize.js", "test.html", "test.pdf"])
    except Exception as e:
        print e

if __name__ == "__main__":
    generate_pdf()