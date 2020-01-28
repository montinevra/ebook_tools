#!/usr/bin/env python3

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Batch ocr processing using https://www.onlineocr.net/.    #
# Run this from a directory full of images you want to ocr  #
# https://github.com/montinevra/ebook_tools                 #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

from enum import Enum
import sys
import os
import os.path
from os.path import expanduser
import time
import selenium
from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

g_download_dir = "~/Downloads"
g_download_limit = 15
g_downloads = 0
g_input_dir = os.getcwd()
g_input_list = os.listdir(g_input_dir)
g_scan_list = []
g_ocr_list = []
g_output = {
	"extension": [".docx", ".xlsx", ".txt"],
	"menu_value": ["Microsoft Word (docx)", "Microsoft Excel (xlsx)", "Text Plain (txt)"]
}
class FormatIndex(Enum):
	DOCX = 0
	XLSX = 1
	TXT = 2
g_args = {
	"docx": FormatIndex.DOCX,
	".docx": FormatIndex.DOCX,
	"word": FormatIndex.DOCX,
	"xlsx": FormatIndex.XLSX,
	".xlsx": FormatIndex.XLSX,
	"excel": FormatIndex.XLSX,
	"txt": FormatIndex.TXT,
	".txt": FormatIndex.TXT,
	"plaintext": FormatIndex.TXT,
}
g_format_index = FormatIndex.DOCX.value

def input_format_is_valid():
	message_box = g_driver.find_element_by_id("message")

	time.sleep(.5)
	while not g_convert_btn.is_enabled():
		if message_box.text == "Filetype not allowed":
			return False
		time.sleep(.5)
	return True

if len(sys.argv) >= 2:
	try:
		g_format_index = g_args[sys.argv[1].lower()].value
	except:
		print("'", sys.argv[1], "' is not a valid output format. Choose 'docx', 'xlsx', or 'txt' instead. Defaulting to 'docx'...")
for i in range(len(g_input_list)):
	g_ocr_list.append(os.path.join(expanduser(g_download_dir), os.path.splitext(g_input_list[i])[0] + g_output["extension"][g_format_index]))
	g_scan_list.append(os.path.join(g_input_dir, g_input_list[i]))
g_driver = webdriver.Chrome()
g_driver.get("https://www.onlineocr.net/")
for i in range(len(g_scan_list)):
	if os.path.exists(g_ocr_list[i]):
		print(g_ocr_list[i] + " exists. Skipping...")
		continue
	if g_downloads >= g_download_limit:
		print("Download limit reached. Please wait an hour before ocr-ing additional files.")
		break
		# g_driver.delete_all_cookies()
		# g_driver.refresh()
		# g_downloads = 0
	print("ocr-ing " + g_scan_list[i] + "...")
	format_menu = Select(g_driver.find_element_by_id("MainContent_comboOutput"))
	format_menu.select_by_value(g_output["menu_value"][g_format_index])
	upload_btn = g_driver.find_element_by_id("fileupload")
	upload_btn.send_keys(g_scan_list[i])
	g_convert_btn = g_driver.find_element_by_id("MainContent_btnOCRConvert")
	if not input_format_is_valid():
		print("    Invalid file format. Skipping...")
		continue
	g_convert_btn.click()
	time.sleep(.5)
	download_link = WebDriverWait(g_driver, 30).until(EC.element_to_be_clickable((By.ID, "MainContent_lnkBtnDownloadOutput")))
	download_link.click()
	while not os.path.exists(g_ocr_list[i]):
		time.sleep(.5)
	g_downloads += 1
g_driver.quit()
