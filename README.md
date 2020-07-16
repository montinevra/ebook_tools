# ebook_tools
A collection of scripts for converting digital scans to ebooks

## html_from_docx.py
Converts all numbered .docx files (e.g. "page001.docx", page002.docx") in a directory to html. Strips all formatting. This does *not* create a valid .html file, just some code that you can copy/paste into your epub editor.

Requires python-docx.

	pip3 install python-docx

Usage:

	python3 html_from_docs.py [src_dir]

Uses the current directory if none is specified.

Outputs directly to the shell. Redirect it if you want to save to a file.

	python3 html_from_docs.py [src_dir] > some_file

## nav_pagelist.py
Generates a pagelist section for the nav.xhtml in an epub.

Requires EbookLib.

	pip3 install EbookLib

Usage: 

	python3 nav_pagelist.py ebook

where `ebook` is a `.epub` file. Then copy/paste the output into your nav.xhtml

## ocr_batch.py
Batch ocr processing via https://www.onlineocr.net/.

### Requirements 
#### Selenium

    pip3 install selenium    

#### chromedriver
Install it from your package manager, or manually: https://chromedriver.chromium.org/getting-started

#### Google Chrome

https://www.google.com/chrome/

### Usage
Put all of the images you want to run ocr on into some directory. Then

    python3 ocr_upload.py [src_dir] [format]

`src_dir` should be some directory with ocr-able images. Uses the current directory if omitted.
`format` is one of `txt`, `docx`, or `xlsx`. Defaults to `docx`.

Ocr'ed files will be downloaded to `~/Downloads`.

## rotate_jpgs.sh
    bash rotate_jpgs.sh [arg1] [arg2]
Rotates every other jpg in a directory. By default, rotates odd-numbered images (i.e. filename ends with 1, 3, 5, 7, or 9) by 180 degrees. Add the argument `even` or `all` to rotate even-numbered ones, or all of them. Add a number from 0-360 as an argument to change the rotation angle (degrees, clockwise).
