import lib.DataFrameBuilder as DataFrameBuilder
import lib.PageDataExtractor as PersonDataExtractor
import lib.PdfScraper as PdfScraper
import lib.WorkbookBuilder as WorkbookBuilder

# Import statements go to the folder.code, so lib.PdfScraper allows us to use code in the PdfScraper.py file


# This file defines the full end-to-end function of taking the PDF and turning it into the formatted excel sheet
# so that the team can print out the roster.


def format_pdf_to_excel(input_file):
    text_pages = PdfScraper.convert_pdf_to_txt(input_file)
    page_data = PersonDataExtractor.process_text_pages(text_pages)
    tabs, tabs_df_list = DataFrameBuilder.build_data_frame(page_data)
    return WorkbookBuilder.build_workbook(tabs, tabs_df_list)

# First, we scrape the PDF for text and output that text
# Then we loop through the text/PDF pages to extract the data we need, and output that data
# Next we create dataframes with the proper structure, filtered for just who we need and divided into tabs
# Finally, we create an excel workbook from the dataframes that matches the spaced format we need
