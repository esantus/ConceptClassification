"""

pdf_highlighter.py

This script takes in input a folder with PDF files and a file with the annotations. It generates an output folder
in which the same PDFs appear with their text highlighted according to the annotations.

CALL: USER$ python pdf_highlighter.py -a Annotations -i SourceFolder -o TargetFolder
OUTPUT: TargetFolder containing all the PDFs with highlighted the annotations

"""

import argparse
import os

from tqdm import tqdm

from utils.utils import load_annotations, get_annotations, highlight_pdf

import pdb


if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument('-a', '--annotations', type=str, default='annotations.xlsx', help='Excel file containing the annotations. Default: \"annotations.xlsx\"')
	parser.add_argument('-i', '--input_folder', type=str, default='../Preprocessing/input_pdf/', help='Source folder containing the PDF files. Default: \"../Preprocessing/input_pdf/\"')
	parser.add_argument('-o', '--output_folder', type=str, default='output_highlighted/', help='Target folder containing the parsed xml files. Default: \"output_highlighted/\"')
	args = parser.parse_args()

	if os.path.isdir(args.input_folder):

		# Load the annotations
		#annotations = load_annotations(args.annotations)

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

			# Identifying the appropriate annotation for the file
			#file_annotation = get_annotations(annotations, fname)

			# Highlighting the PDF
			highlight_pdf([{'page':2, 'author':'E.S.', 'contents':'Good stuff', 'x1':100, 'y1':200, 'x2':250, 'y2':350, 'concept':'Warning'}], input_fname, output_fname)
