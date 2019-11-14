from PyPDF2 import PdfFileWriter, PdfFileReader
from PyPDF2.generic import DictionaryObject, NumberObject, FloatObject, NameObject, TextStringObject, ArrayObject

import pdb


concept_color = {'Warning':[0, 0.3, 0.2]}


def createHighlight(x1, y1, x2, y2, meta, color = [1, 0, 0]):
	'''
	Create a highlight object which will be applied to a box in a PDF page (please,
	notice that coordinates start in the bottom left) with specific metadata and
	colors.
	'''
	newHighlight = DictionaryObject()

	newHighlight.update({
		NameObject("/F"): NumberObject(4),
		NameObject("/Type"): NameObject("/Annot"),
		NameObject("/Subtype"): NameObject("/Highlight"),

		NameObject("/T"): TextStringObject(meta["author"]),
		NameObject("/Contents"): TextStringObject(meta["contents"]),

		NameObject("/C"): ArrayObject([FloatObject(c) for c in color]),
		NameObject("/Rect"): ArrayObject([
			FloatObject(x1),
			FloatObject(y1),
			FloatObject(x2),
			FloatObject(y2)
		]),
		NameObject("/QuadPoints"): ArrayObject([
			FloatObject(x1),
			FloatObject(y2),
			FloatObject(x2),
			FloatObject(y2),
			FloatObject(x1),
			FloatObject(y1),
			FloatObject(x2),
			FloatObject(y1)
		]),
	})
	return newHighlight


def addHighlightToPage(highlight, page, output):
	'''
	Add the annotation object to the page
	'''
	highlight_ref = output._addObject(highlight);

	if "/Annots" in page:
		page[NameObject("/Annots")].append(highlight_ref)
	else:
		page[NameObject("/Annots")] = ArrayObject([highlight_ref])


def load_annotations(path):
	'''
	Load an Excel file containing the annotations and processes them
	'''
	return ''


def get_annotations(annotations, fname):
	'''
	Load the annotations related to a specific fname
	'''
	return ''


def highlight_pdf(annotations, input_fname, output_fname):
	'''
	Given the annotations and the name of the input file, generate an ouptut PDF file with the
	annotations highlighted.
	'''
	pdfInput = PdfFileReader(open(input_fname, "rb"))
	pdfOutput = PdfFileWriter()

	for i, page in enumerate(pdfInput.pages):
		for annotation in annotations:
			if annotation['page'] == i:
				highlight = createHighlight(annotation['x1'], annotation['y1'], annotation['x2'], annotation['y2'], {
					"author": annotation['author'],
					"contents": annotation['contents']
				}, color=concept_color[annotation['concept']])

				addHighlightToPage(highlight, page, pdfOutput)

		pdfOutput.addPage(page)

	outputStream = open(output_fname, "wb")
	pdfOutput.write(outputStream)
	return True
