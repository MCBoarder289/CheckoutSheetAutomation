import lib.DataFrameBuilder as DataFrameBuilder
import lib.PageDataExtractor as PersonDataExtractor
import lib.PdfScraper as PdfScraper
import lib.WorkbookBuilder as WorkbookBuilder


def format_pdf_to_excel(input_file):
    text_pages = PdfScraper.convert_pdf_to_txt(input_file)
    page_data = PersonDataExtractor.process_text_pages(text_pages)
    tabs, tabs_df_list = DataFrameBuilder.build_data_frame(page_data)
    return WorkbookBuilder.build_workbook(tabs, tabs_df_list)
