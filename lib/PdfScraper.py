from io import StringIO

from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage


def convert_pdf_to_txt(input_file):
    pages = PDFPage.get_pages(input_file, set(), maxpages=0, password="", caching=True, check_extractable=True)

    resource_manager = PDFResourceManager()
    retstr = StringIO()
    text_converter = TextConverter(resource_manager, retstr, codec='utf-8', laparams=(LAParams()))
    interpreter = PDFPageInterpreter(resource_manager, text_converter)

    try:
        text_pages = []
        for page_number, page in enumerate(pages):
            interpreter.process_page(page)
            page_text = retstr.getvalue()
            text_pages.append(TextPage(page_number, page_text))
        return text_pages

    finally:
        text_converter.close()
        retstr.close()


class TextPage:
    def __init__(self, page_number, text):
        self.page_number = page_number
        self.text = text
