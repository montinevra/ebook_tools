#!/usr/bin/env python3

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# Converts all numbered .docx files (e.g. "page001.docx", page002.docx")
# in a directory to html. Strips all formatting. 
# Usage: python3 html_from_docs.py [src_dir]
# https://github.com/montinevra/ebook_tools
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

import sys as Sys
import os as OS
import re as Re
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
	if len(Sys.argv) >= 2:
		if not OS.path.isdir(Sys.argv[1]):
			print(Sys.argv[1], "is not a valid directory.")
			Sys.exit()
		return Sys.argv[1]
	else:
		return OS.getcwd()


def main():
	page_num = None
	src_dir = get_src_dir()
	docx_list = OS.listdir(src_dir)
	last_char = "."
	last_page = None

	OS.chdir(src_dir)
	for input_file in docx_list:
		try:
			document = Document(input_file)
			file_name = OS.path.splitext(input_file)[0]
			nums_in_filename = Re.findall("[0-9]+", file_name)
			if len(nums_in_filename) == 1 and nums_in_filename[0] == "000":
				page_num = "0"
			else:
				page_num = Re.findall("[1-9]+[0-9]*", file_name)[-1]
		except:
			continue
		if len(nums_in_filename) > 1 and nums_in_filename[0] == "000":
			page_num = roman_from_int(int(page_num)).lower()
		if (last_char == "."):
			tag = "div"
		else:
			tag = "span"
		while last_page != None and last_page.isnumeric() and int(last_page) + 1 < int(page_num):
			last_page = str(int(last_page) + 1)
			print('<' + tag + ' title="' + last_page + '" id="p' + last_page + '" epub:type="pagebreak"></' + tag + '>')
		print('<' + tag + ' title="' + page_num + '" id="p' + page_num + '" epub:type="pagebreak"></' + tag + '>')
		last_char = print_block_items(document, page_num)
		last_page = page_num


if __name__ == "__main__":
	main()
