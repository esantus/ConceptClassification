
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter, XMLConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO
from io import BytesIO

import xml.etree.ElementTree as ET

import pdb


# To signal a change in size of the characters in the PDF.
CHANGE_SIZE = ' ~ '


def str2bool(v):
	'''
	Turns a string argument into boolean
	'''
	if isinstance(v, bool):
	   return v
	if v.lower() in ('yes', 'true', 't', 'y', '1'):
		return True
	elif v.lower() in ('no', 'false', 'f', 'n', '0'):
		return False
	else:
		raise argparse.ArgumentTypeError('Boolean value expected.')


def change_extension(fname, extension='txt'):
	'''
	Change file extension to .txt
	'''
	return fname[:-3] + extension


def pdf2txt(path, codec='utf-8', password = "", maxpages = 0, caching = True):
	'''
	Given the name of a PDF file, use PDFMiner to extract its pages and return them as TXT (in utf-8 bytes).
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
	Given the name of a PDF file, use PDFMiner to extract its pages and return them as XML (in utf-8 bytes).
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

	xml = xml.decode('utf-8')
	if not xml.startswith('</pages>'):
		xml += '\n</pages>'

	return xml


def tag_it(tag, attrs=[]):
	'''
	Return the tag and the attributes within brackets
	'''
	return '<' + tag + ' ' + ' '.join(attrs) + '>' if len(attrs)>0 else '<' + tag + '>'


def print_children(node, tabs=''):
	'''
	Given a node, it prints the tag, the attributes and the text, navigating the children,
	breadth-first, before moving to the next node.
	'''
	tabs += '\t'
	for child in node:
		attribs = [(x, child.attrib[x]) for x in child.attrib if x not in ['font', 'colourspace', 'ncolour']]
		print('{}{}: {} - {}'.format(tabs, child.tag, attribs, child.text))

		print_children(child, tabs)



def navigate_children(node, previous='', xml='', tabs='', print_tree=False, print_line=True):
	'''
	Given a node, it saves an xml text file, navigating the children, breadth-first,
	before moving to the next node.
	'''
	if tabs == '':
		xml += tag_it(node.tag)

	tabs += '\t'
	for child in node:

		# Ignoring images and other figures...
		if child.tag in ['figure', 'rect', 'curve', 'line', 'layout']:
			continue

		# Parsing all the other tags
		if child.tag == 'page':
			xml += '\n' + tabs + tag_it('page', ['id={}'.format(child.attrib['id'])])
		elif child.tag == 'textbox':
			xml += '\n' + tabs + tag_it('box', ['id={}'.format(child.attrib['id']), 'pos={}'.format(child.attrib['bbox'])])
		elif child.tag == 'textline' and print_line:
			xml += '\n' + tabs + tag_it('line', ['pos={}'.format(child.attrib['bbox'])])
		elif child.tag == 'text':
			if previous != '' and previous.tag == 'text' and 'size' in previous.attrib and 'size' in child.attrib:
				if float(previous.attrib['size']) != float(child.attrib['size']):
					xml += CHANGE_SIZE

			if '\n' in child.text:
				if previous.text == '-' and not print_line:
					xml = xml[:-1]
				else:
					xml += child.text.strip('\n') + ' '
			else:
				xml += child.text

		if print_tree:
			attribs = [(x, child.attrib[x]) for x in child.attrib if x not in ['font', 'colourspace', 'ncolour']]
			print('{}{}: {} - {}'.format(tabs, child.tag, attribs, child.text))

		previous = child
		xml = navigate_children(child, previous, xml, tabs, print_line=print_line)

	return xml


def parse_xml(path, print_tree=False, print_line=True):
	'''
	Given the name of a XML file, parse it and return it as XML (in utf-8 bytes).
	'''
	content = ET.parse(path)
	root = content.getroot()
	xml = navigate_children(root, print_line=print_line)

	if print_tree:
		print_children(root)

	return xml