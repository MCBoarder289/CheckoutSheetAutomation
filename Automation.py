
import re
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO


def convert_pdf_to_txt(path):
    # Create variables to make code easier to read
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    # Open the file, begin to interpret the PDF
    fp = open(path, 'rb') # file(path, 'rb')  # file() was Python 2.x, open is Python 3.x
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 0
    caching = True
    pagenos=set()
    fstr = ''
    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password,
                                  caching=caching, check_extractable=True):
        interpreter.process_page(page)

        str = retstr.getvalue()
        fstr += str

    fp.close()
    device.close()
    retstr.close()
    return fstr

print(convert_pdf_to_txt("C:\\Users\\Michael Chapman\\Downloads\\Mike Test - Check-Ins Report.pdf"))

pdftext = convert_pdf_to_txt("C:\\Users\\Michael Chapman\\Downloads\\Mike Test - Check-Ins Report.pdf")

# Returning the regular expression match -- .group(0)
# https://stackoverflow.com/questions/18493677/how-do-i-return-a-string-from-a-regex-match-in-python

# How to iterate through the lines of the long single text string with /n line breaks
# https://stackoverflow.com/questions/22918013/python-iterate-over-a-string-containing-newlines

"""
Lines go from upper left of page in columns all the way down until the last name on the page,
then it goes to the top of the page on the right side and down that column,
and finally it goes through the middle of the page (2 check ins).

Seems to be doubling the number of pages per single instance of "2 check ins" (2 pages = 4 pages)
Pages without "2 check ins" removes doesn't seem to duplicate

"""

regex_list = []

pdftext_split = pdftext.splitlines()

for i in range(len(pdftext_split)):
    if re.search('\d\d:\d\d[ap]', pdftext_split[i]):
        regex_list.append((i, re.search('\d\d:\d\d[ap]', pdftext_split[i])))
    elif re.search('\d:\d\d[ap]', pdftext_split[i]):
        regex_list.append((i, re.search('\d:\d\d[ap]', pdftext_split[i])))
    else:
        continue



""" 
This shows the type of object and LTTextBoxHorizonal had the data I was looking for,
however there the first person value would also be lumped in with the title value, so we probably need to loop
line by line like before

path = "C:\\Users\\Michael Chapman\\Downloads\\Mike Test - Check-Ins Report.pdf"

rsrcmgr = PDFResourceManager()
retstr = StringIO()
codec = 'utf-8'
laparams = LAParams()
device = PDFPageAggregator(rsrcmgr, laparams=laparams)
fp = open(path, 'rb')  # file(path, 'rb')  # file() was Python 2.x, open is Python 3.x
interpreter = PDFPageInterpreter(rsrcmgr, device)
password = ""
maxpages = 0
caching = True
pagenos = set()
fstr = ''
for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password, caching=caching,
                              check_extractable=True):
    interpreter.process_page(page)
    layout = device.get_result()
    for element in layout:
        print(element)

str = retstr.getvalue()
fstr += str

fp.close()
device.close()
retstr.close()

"""


