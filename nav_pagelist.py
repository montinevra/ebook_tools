#!/usr/bin/env python3

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# Parses your epub for pagebreak type elements, then generates html for a page
# list that you can copy/paste into your nav.xhtml 
# Usage: python3 nav_pagelist.py book.epub
# https://github.com/montinevra/ebook_tools
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

import sys
import os
from html.parser import HTMLParser
import ebooklib
from ebooklib import epub


# Generates a list of hrefs for each pagebreak.
class PagebreakFinder(HTMLParser):
	def __init__(self):
		HTMLParser.__init__(self)
		self.m_filename = ""
		self.m_href_list = []

	def handle_starttag(self, tag, attrs):
		if tag == "div" or tag == "span":
			for i in reversed(attrs):
				if i[0] == "epub:type" and i[1] == "pagebreak":
					break
			else:
				return
			for i in attrs:
				if i[0] == "id":
					self.m_href_list.append(self.m_filename + "#" + i[1])
					return


# # Finds where in the nav page the pagelist should go
# class PagelistPosFinder(HTMLParser):
# 	def __init__(self):
# 		HTMLParser.__init__(self)
# 		self.m_pos_toc = {}
# 		self.m_pos_pagelist = {}
# 		self.__m_current_nav_type = None

# 	def get_new_pagelist_pos(self):
# 		if self.m_pos_pagelist:
# 			new_pagelist_pos = self.m_pos_pagelist
# 		elif self.m_pos_toc:
# 			new_pagelist_pos = self.m_pos_toc
# 			new_pagelist_pos["start"] = new_pagelist_pos["end"]
# 		return new_pagelist_pos

# 	def handle_starttag(self, tag, attrs):
# 		if tag == "nav":
# 			for i in attrs:
# 				if i[0] == "epub:type":
# 					self.__m_current_nav_type = i[1]
# 					if self.__m_current_nav_type == "toc":
# 						self.m_pos_toc['start'] = list(self.getpos())
# 					elif self.__m_current_nav_type == "page-list":
# 						self.m_pos_pagelist['start'] = list(self.getpos())
# 					break

# 	def handle_endtag(self, tag):
# 		if tag == "nav":
# 			if self.__m_current_nav_type == "toc":
# 				self.m_pos_toc['end'] = list(self.getpos())
# 				self.m_pos_toc['end'][1] += 6 				#end tag is 6 chars
# 			elif self.__m_current_nav_type == "page-list":
# 				self.m_pos_pagelist['end'] = list(self.getpos())
# 				self.m_pos_pagelist['end'][1] += 6


def validate_epub(epub_file):
	book = None
	nav_page = None	

	try:
		book = epub.read_epub(epub_file)
	except:
		print("Please provide a valid .epub file from which to generate a page-list.", 
			  "(Validate your .epub with epubcheck)",
			  "\nUsage:\tpython3 nav_pagelist.py book.epub")
		sys.exit(1) 
	nav_page = book.get_item_with_href('Text/nav.xhtml')
	try:
		if nav_page is None:
			raise TypeError
	except:
		print("Nav page is missing. Use your epub editor to add a nav page.")
		# sys.exit(1)
	return book, nav_page


# Generates the pagelist html from a list of hrefs
def pagelist_from_href(href_list):
	pagelist = '<nav epub:type="page-list" id="page_list" hidden=""><h1>Page List</h1>\n<ol>\n'
	for i in href_list:
		pagelist += '<li><a href="' + i + '">' + i.split('#', 1)[1] + '</a></li>\n'
	pagelist += '</ol>\n</nav>\n'
	return pagelist


def main():
	book, nav_page = validate_epub(sys.argv[1])
	documents = book.get_items_of_type(ebooklib.ITEM_DOCUMENT)
	pagebreak_finder = PagebreakFinder()
	ENCODING = "utf-8"
	html_pagelist = ""

	for i in documents:
		if i != nav_page:
			pagebreak_finder.m_filename = os.path.basename(i.get_name())
			pagebreak_finder.feed(i.get_body_content().decode(ENCODING))
	html_pagelist = pagelist_from_href(pagebreak_finder.m_href_list)
	print(html_pagelist)

	##
	## I wrote all this before discovering that ebooklib is buggy and doesn't do
	## what I want. So now this script just prints out some copy/pastable html
	## rather than modifying the epub.
	##
	# pagelist_pos_finder = PagelistPosFinder()
	# nav_page_contents = nav_page.get_body_content().decode(ENCODING) 
	# pagelist_pos_finder.feed(nav_page_contents)
	# new_pagelist_pos = pagelist_pos_finder.get_new_pagelist_pos()
	# nav_page_contents_split = nav_page_contents.splitlines(True)
	# new_nav_page_contents = ""
	# for i in range(new_pagelist_pos["start"][0] - 1):
	# 	new_nav_page_contents += nav_page_contents_split[i]
	# new_nav_page_contents += nav_page_contents_split[i + 1][0:new_pagelist_pos["start"][1]] + '\n'
	# new_nav_page_contents += html_pagelist
	# if nav_page_contents_split[new_pagelist_pos["end"][0] - 1][new_pagelist_pos["end"][1]] != '\n':
	# 	new_nav_page_contents += nav_page_contents_split[new_pagelist_pos["end"][0] - 1][new_pagelist_pos["end"][1]:]
	# for i in range(new_pagelist_pos["end"][0], len(nav_page_contents_split)):
	# 	new_nav_page_contents += nav_page_contents_split[i]
	# nav_page.set_content(new_nav_page_contents.encode(ENCODING))
	# epub.write_epub(sys.argv[1], book)


if __name__ == "__main__":
	main()


