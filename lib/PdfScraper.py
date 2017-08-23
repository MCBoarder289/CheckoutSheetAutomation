from io import StringIO

from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage


class PdfScraper:
    def __init__(self):
        return

    def convert_pdf_to_txt(self, input_file):
        pages = PDFPage.get_pages(input_file, set(), maxpages=0, password="", caching=True, check_extractable=True)

        resource_manager = PDFResourceManager()
        retstr = StringIO()
        text_converter = TextConverter(resource_manager, retstr, codec='utf-8', laparams=(LAParams()))
        interpreter = PDFPageInterpreter(resource_manager, text_converter)

        try:
            pdf_as_string = ''
            for page_number, page in enumerate(pages):
                interpreter.process_page(page)
                page_text = retstr.getvalue()
                pdf_as_string += "Python Page:" + str(page_number) + " newline \n"
                pdf_as_string += page_text

            return pdf_as_string

        finally:
            text_converter.close()
            retstr.close()
