#!/usr/bin/env python3

# Converts all numbered .docx files (e.g. "page001.docx", page002.docx")
# in a directory to html. Strips all formatting. 
# https://github.com/montinevra/ebook_tools

import os
import re
from roman_numeral.roman_numeral import roman_from_int
from docx import Document
from docx.document import Document as _Document
from docx.oxml.table import CT_Tbl
from docx.oxml.text.paragraph import CT_P
from docx.table import _Cell, Table
from docx.text.paragraph import Paragraph

g_page_num = None


def iter_block_items(parent):
    if isinstance(parent, _Document):
        parent_elm = parent.element.body
    elif isinstance(parent, _Cell):
        parent_elm = parent._tc
    else:
        raise ValueError("must be document or cell object")
    for child in parent_elm.iterchildren():
        if isinstance(child, CT_P):
            yield Paragraph(child, parent)
        elif isinstance(child, CT_Tbl):
            yield Table(child, parent)


def print_block_items(t_parent):
	last_char = None

	for item in iter_block_items(t_parent):
		if isinstance(item, Paragraph):
			print("  <p>", end="")
			for run in item.runs:
				if (not (run.text == g_page_num)):
					print(run.text, end="")
					if len(run.text):
						last_char = run.text[-1]
			print("  </p>")
		elif isinstance(item, Table):
			for row in range(len(item.rows)):
				for col in range(len(item.columns)):
					print_block_items(item.cell(row, col))
	return(last_char)


def main():
	global g_page_num
	input_dir = os.getcwd()
	input_list = os.listdir(input_dir)
	last_char = "."

	for input_file in input_list:
		try:
			document = Document(input_file)
			file_name = os.path.splitext(input_file)[0]
			nums_in_filename = re.findall("[0-9]+", file_name)
			g_page_num = re.findall("[1-9]+[0-9]*", file_name)[-1]
		except:
			continue
		if nums_in_filename[0] == "000":
			g_page_num = roman_from_int(int(g_page_num)).lower()
		if (last_char == "."):
			tag = "div"
		else:
			tag = "span"
		print('<' + tag + ' title="' + g_page_num + '" id="p' + g_page_num + '" epub:type="pagebreak"></' + tag + '>')
		last_char = print_block_items(document)


main()
