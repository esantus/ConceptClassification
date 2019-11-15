"""

pdf_converter.py

This script takes in input a folder with PDF files and generates an output folder with the same files parsed as TXT or XML files.

CALL: USER$ python pdf_converter.py -i SourceFolder -o TargetFolder -f format=[xml, txt]
OUTPUT: TargetFolder containing all the PDFs parsed as either texts or xmls

"""

import argparse
import os

from tqdm import tqdm

from utils.utils import change_extension, pdf2txt, pdf2xml

import pdb


if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument('-i', '--input_folder', type=str, default='input_pdf/', help='Source folder containing the PDF files. Default: \"input_pdf/\"')
	parser.add_argument('-o', '--output_folder', type=str, default='output_pdf/', help='Target folder containing the parsed PDF files. Default: \"output_pdf/\"')
	parser.add_argument('-f', '--format', type=str, default='xml', choices=['xml', 'txt'], help='Format of the output files. Default: \'xml\'')
	args = parser.parse_args()

	if os.path.isdir(args.input_folder):

		# Checking the files in the input directory
		fnames = os.listdir(args.input_folder)
		print('\nFound {} files in {}\n'.format(len(fnames), args.input_folder))
		
		# Creating the output directory if it does not exist
		if not os.path.isdir(args.output_folder):
			os.mkdir(args.output_folder)

		# Parsing every file in the input directory and saving it
		for i in tqdm(range(len(fnames))):
			fname = fnames[i]
			print('\n\tProcessing {}'.format(fname))
			input_fname = os.path.join(args.input_folder, fname)
			output_fname = os.path.join(args.output_folder, change_extension(fname, args.format))

			# Parsing depending on the desired output format
			if args.format == 'txt':
				output_text = pdf2txt(input_fname)
			elif args.format == 'xml':
				output_xml = pdf2xml(input_fname)
			else:
				print('Format {} not supported.'.format(args.format))

			with open(output_fname, 'w') as output_file:
					output_file.write(output_xml)