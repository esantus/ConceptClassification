"""

xml2pdf.py

This script takes in input a folder with XML files from Pharma and it generates an output folder with the same files in PDF.

CALL: USER$ python xml2pdf.py -i SourceFolder -o TargetFolder
OUTPUT: TargetFolder containing all the XMLs turned into PDF
"""

import argparse
import os

from tqdm import tqdm

from utils.utils import change_extension, xml2pdf
import pdb



if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument('-i', '--input_folder', type=str, default='input_xml/', help='Source folder containing the XML files. Default: \"input_xml/\"')
	parser.add_argument('-o', '--output_folder', type=str, default='input_pdf/', help='Target folder containing the parsed xml files. Default: \"input_pdf/\"')
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
			if not fname.endswith('.xml'):
				continue
			print('\n\tProcessing {}'.format(fname))
			input_fname = os.path.join(args.input_folder, fname)
			output_fname = os.path.join(args.output_folder, change_extension(fname, 'pdf'))

			xml2pdf(input_fname, output_fname, print_html=False)