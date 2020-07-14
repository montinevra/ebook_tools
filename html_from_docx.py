#!/usr/bin/env python3

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# Converts all numbered .docx files (e.g. "page001.docx", page002.docx")
# in a directory to html. Strips all formatting. 
# Usage: python3 html_from_docs.py [src_dir]
# https://github.com/montinevra/ebook_tools
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

import sys
import os
import re
from docx import Document
from docx.document import Document as _Document
from docx.oxml.table import CT_Tbl
from docx.oxml.text.paragraph import CT_P
from docx.table import _Cell, Table
from docx.text.paragraph import Paragraph
from roman_numeral.roman_numeral import roman_from_int


def iter_block_items(t_parent):
    if isinstance(t_parent, _Document):
        parent_elm = t_parent.element.body
    elif isinstance(t_parent, _Cell):
        parent_elm = t_parent._tc
    else:
        raise ValueError("must be document or cell object")
    for child in parent_elm.iterchildren():
        if isinstance(child, CT_P):
            yield Paragraph(child, t_parent)
        elif isinstance(child, CT_Tbl):
            yield Table(child, t_parent)


def print_block_items(t_parent, t_page_num):
	last_char = None

	for item in iter_block_items(t_parent):
		if isinstance(item, Paragraph):
			print("  <p>", end="")
			for run in item.runs:
				if (not (run.text == t_page_num)):
					print(run.text, end="")
					if len(run.text):
						last_char = run.text[-1]
			print("  </p>")
		elif isinstance(item, Table):
			for row in range(len(item.rows)):
				for col in range(len(item.columns)):
					print_block_items(item.cell(row, col), t_page_num)
	return(last_char)


def get_src_dir():
	if len(sys.argv) >= 2:
		if not os.path.isdir(sys.argv[1]):
			print(sys.argv[1], "is not a valid directory.")
			sys.exit()
		return sys.argv[1]
	else:
		return os.getcwd()


def main():
	page_num = None
	src_dir = get_src_dir()
	docx_list = os.listdir(src_dir)
	last_char = "."

	os.chdir(src_dir)
	for input_file in docx_list:
		try:
			document = Document(input_file)
			file_name = os.path.splitext(input_file)[0]
			nums_in_filename = re.findall("[0-9]+", file_name)
			page_num = re.findall("[1-9]+[0-9]*", file_name)[-1]
		except:
			continue
		if nums_in_filename[0] == "000":
			page_num = roman_from_int(int(page_num)).lower()
		if (last_char == "."):
			tag = "div"
		else:
			tag = "span"
		print('<' + tag + ' title="' + page_num + '" id="p' + page_num + '" epub:type="pagebreak"></' + tag + '>')
		last_char = print_block_items(document, page_num)


if __name__ == "__main__":
	main()
