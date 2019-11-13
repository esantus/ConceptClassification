"""

pdf_converter.py

This script takes in input a folder with PDF files and generates an output folder with the same files parsed as TXT or XML files.

CALL: USER$ python pdf_converter.py -i SourceFolder -o TargetFolder
OUTPUT: TargetFolder containing all the PDFs parsed as either texts or xmls

"""

import argparse

import os

from tqdm import tqdm

from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter, XMLConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO
from io import BytesIO

import pdb


def change_extension(fname, extension='txt'):
	'''
	Change file extension to .txt
	'''
	return fname[:-3] + extension


def pdf2txt(path, codec='utf-8', password = "", maxpages = 0, caching = True):
	'''
	Given the name of a PDF file, use PDFMiner to extract those pages and return them as TXT (in utf-8 bytes).
	'''
	rsrcmgr = PDFResourceManager()
	retstr = StringIO()
	laparams = LAParams()
	
	device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
	with open(path, 'rb') as fp:
		interpreter = PDFPageInterpreter(rsrcmgr, device)
		pagenos=set()
		for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password,caching=caching, check_extractable=True):
			interpreter.process_page(page)
		text = retstr.getvalue()
	
	device.close()
	retstr.close()
	return text


def pdf2xml(path, codec='utf-8', password = "", maxpages = 0, caching = True):
	'''
    Given the name of a PDF file, use PDFMiner to extract those pages and return them as XML (in utf-8 bytes).
    '''
	rsrcmgr = PDFResourceManager()
	retstr = BytesIO()
	laparams = LAParams()

	device = XMLConverter(rsrcmgr, retstr, codec='utf-8', laparams=laparams)
	with open(path, 'rb') as fp:
		interpreter = PDFPageInterpreter(rsrcmgr, device)
		pagenos=set()
		#pg = 1
		for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password,caching=caching, check_extractable=True):
			interpreter.process_page(page)
			#xml = '%s %s %s' % ('<PAGE {}>'.format(pg), retstr.getvalue(), '</PAGE {}>'.format(pg))
			#pg += 1
		xml = retstr.getvalue()
	
	device.close()
	retstr.close()
	return xml


if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument('-i', '--input_folder', type=str, default='input_pdf/', help='Source folder containing the PDF files. Default: \"input_pdf/\"')
	parser.add_argument('-o', '--output_folder', type=str, default='output_pdf/', help='Target folder containing the parsed PDF files. Default: \"output_pdf/\"')
	parser.add_argument('-f', '--format', type=str, default='xml', choices=['xml', 'txt'], help='Format of the output files. Default: \'xml\'')
	args = parser.parse_args()

	if os.path.isdir(args.input_folder):

		# Checking the files in the input directory
		fnames = os.listdir(args.input_folder)
		print('Found {} files in {}'.format(len(fnames), args.input_folder))
		
		# Creating the output directory if it does not exist
		if not os.path.isdir(args.output_folder):
			os.mkdir(args.output_folder)

		# Parsing every file in the input directory and saving it
		for i in tqdm(range(len(fnames))):
			fname = fnames[i]
			print('Processing {}'.format(fname))
			input_fname = os.path.join(args.input_folder, fname)
			output_fname = os.path.join(args.output_folder, change_extension(fname, args.format))

			if args.format == 'txt':
				output_text = pdf2txt(input_fname)
				with open(output_fname, 'w') as output_file:
					output_file.write(output_text)
			elif args.format == 'xml':
				output_xml = pdf2xml(input_fname)
				with open(output_fname, 'wb') as output_file:
					output_file.write(output_xml)
			else:
				print('Format {} not supported.'.format(args.format))
