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


def input_format_is_valid(t_driver, t_convert_btn):
	message_box = t_driver.find_element_by_id("message")

	time.sleep(.5)
	while not t_convert_btn.is_enabled():
		if message_box.text == "Filetype not allowed":
			return False
		time.sleep(.5)
	return True


def get_src_dir():
	if len(sys.argv) >= 2:
		for i in range(1, min([len(sys.argv), 3])):
			if os.path.isdir(sys.argv[i]):
				return sys.argv.pop(i)
	print("No directory specified. Using current directory...")
	return os.getcwd()


def get_format():
	class Format(Enum):
		DOCX = 0
		XLSX = 1
		TXT = 2

	format_args = {
		"docx": Format.DOCX,
		".docx": Format.DOCX,
		"word": Format.DOCX,
		"xlsx": Format.XLSX,
		".xlsx": Format.XLSX,
		"excel": Format.XLSX,
		"txt": Format.TXT,
		".txt": Format.TXT,
		"plaintext": Format.TXT,
	}

	if len(sys.argv) >= 2:
		for i in range(1, min([len(sys.argv), 3])):
			if sys.argv[i].lower() in format_args:
				return format_args[sys.argv[i].lower()].value
	print("No format specified. Using docx...")
	return Format.DOCX.value


def main():
	DOWLOAD_DIR = "~/Downloads"
	DOWNLOAD_LIMIT = 15
	downloads = 0
	src_dir = get_src_dir()
	input_list = os.listdir(src_dir)
	scan_list = []
	ocr_list = []
	output_format = get_format()
	output_value = {
		"extension": (".docx", ".xlsx", ".txt"),
		"menu": ("Microsoft Word (docx)", "Microsoft Excel (xlsx)", "Text Plain (txt)")
	}

	for i in range(len(input_list)):
		ocr_list.append(os.path.join(expanduser(DOWLOAD_DIR), os.path.splitext(input_list[i])[0] + output_value["extension"][output_format]))
		scan_list.append(os.path.join(src_dir, input_list[i]))
	driver = webdriver.Chrome()
	driver.get("https://www.onlineocr.net/")
	for i in range(len(scan_list)):
		if os.path.exists(ocr_list[i]):
			print(ocr_list[i] + " exists. Skipping...")
			continue
		if downloads >= DOWNLOAD_LIMIT:
			print("Download limit reached. Please wait an hour before ocr-ing additional files.")
			break
			# driver.delete_all_cookies()
			# driver.refresh()
			# downloads = 0
		print("ocr-ing " + scan_list[i] + "...")
		format_menu = Select(driver.find_element_by_id("MainContent_comboOutput"))
		format_menu.select_by_value(output_value["menu"][output_format])
		upload_btn = driver.find_element_by_id("fileupload")
		upload_btn.send_keys(scan_list[i])
		convert_btn = driver.find_element_by_id("MainContent_btnOCRConvert")
		if not input_format_is_valid(driver, convert_btn):
			print("\tInvalid file format. Skipping...")
			continue
		convert_btn.click()
		time.sleep(.5)
		download_link = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.ID, "MainContent_lnkBtnDownloadOutput")))
		download_link.click()
		while not os.path.exists(ocr_list[i]):
			time.sleep(.5)
		downloads += 1
	driver.quit()


if __name__ == "__main__":
	main()
