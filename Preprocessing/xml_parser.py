"""

xml_parser.py

This script takes in input a folder with XML files derived from PDFMiner and it generates an output folder with the same files parsed in a more meaningful way.

CALL: USER$ python xml_parser.py -i SourceFolder -o TargetFolder
OUTPUT: TargetFolder containing all the XMLs parsed in a more meaningful way
"""

import argparse
import os

from tqdm import tqdm

from utils.utils import parse_xml

import pdb


if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument('-i', '--input_folder', type=str, default='output_pdf/', help='Source folder containing the XML files. Default: \"output_pdf/\"')
	parser.add_argument('-o', '--output_folder', type=str, default='output_xml/', help='Target folder containing the parsed xml files. Default: \"output_xml/\"')
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
			output_fname = os.path.join(args.output_folder, fname)

			output_text = parse_xml(input_fname)
			with open(output_fname, 'w') as output_file:
				output_file.write(output_text)
