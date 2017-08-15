"""

Mining Checkout PDF and exporting proper file

"""


import re
import pandas as pd
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
    fp = open(path, 'rb')  # file(path, 'rb')  # file() was Python 2.x, open is Python 3.x
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 0
    caching = True
    pagenos = set()
    fstr = ''
    for pagenumber, page in enumerate(PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password,
                                  caching=caching, check_extractable=True)):
        interpreter.process_page(page)

        pagetext = retstr.getvalue()
        fstr += "Python Page:" + str(pagenumber) + " newline \n"  # Enumerate tags the page number
        fstr += pagetext

    fp.close()
    device.close()
    retstr.close()
    return fstr

# print(convert_pdf_to_txt("C:\\Users\\Michael Chapman\\Downloads\\Mike Test - Check-Ins Report.pdf"))

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
counter = 0
# previous_marker = 0
row_type = ""
previous_row_type = ""
page = 0

change_count = 0
change_property = 0

pdftext_split = pdftext.splitlines()

# Loop is in order by time increasing, and spits out key lines:
# NEED TO MAKE SURE THAT WE ALWAYS FOLLOW THESE RULES:
# NEVER PUT A COMMA IN A ROOM NAME OR ROLE NAME, NEVER PUT "Regulars" IN A ROOM NAME OR A ROLE NAME
# NEVER PUT "Python" or "Python Page:" IN A ROOM NAME OR ROLE NAME

# ******** Pages work, but need to make the second page not restart the counter (join/merge causes dupes) **************
# Perhaps all we need to do is have a person counter and a Status Counter, and if the page number hasn't changed
for i in range(len(pdftext_split)):

    text = pdftext_split[i]  # String/text of the individual line

    if re.search('Python Page:', text):
        page = re.search('\d{1,}', text)  # Pulls out the number of the page (can be multiple digits)
        page = int(page.group(0))
        counter = 0
        previous_page = page - 1
        change_count = 0
        person_count = 0
        row_type = ''
        previous_row_type = ''
        continue
    if text == "":  # If it's blank, skip it
        continue
    if re.search('Regulars', text):  # If it has "Regulars", it's an aggregate count row, so skip it
        # counter = 0
        continue
    if re.search(' - ', text):  # If it has " - ", it's the title row "Sunday Morning - <date>", therefore skip
        # counter = 0
        continue
    if re.search('Check-Ins', text):   # Take's out the "2 Check-Ins" property that we don't want
        # counter = 0
        continue
    if re.search('\d\d:\d\d[ap]', text):  # If it has the time, reset the counter, create the time_value to pass on
        counter = 0
        time_value = re.search('\d\d:\d\d[ap]', text)
        time_value = time_value.group(0)
        # regex_list.append((i, counter, text, time_value))
    elif re.search('\d:\d\d[ap]', text):  # If it has the time, reset the counter, create the time_value to pass on
        counter = 0
        time_value = re.search('\d:\d\d[ap]', text)
        time_value = time_value.group(0)
        # regex_list.append((i, counter, text, time_value))
    elif re.search(',', text):  # If it has a comma, it's a name, so add 2 to the counter (2 elements to match)
        row_type = "Person"
        if previous_row_type == "Status":  # previous_marker == 0:  # If the preceeding element was a Status and not a person,
            counter = 0                       #  reset the counter (new page)
            change_count += 1

        if change_count > 1:
            change_count = 0
            change_property += 1

        counter += 2
        previous_row_type = "Person"
        regex_list.append(("Person", page, change_property, counter, text, time_value))

    else:  # Otherwise, simply add one to the counter. Name counter = 2nd value's counter, and 1st values's counter - 1
        row_type = "Status"
        if previous_row_type != row_type:
            previous_row_type = "Status"
            change_count += 1
            # previous_marker = 0
            if change_count > 1:
                change_count = 0
                change_property += 1

            counter = 0
            counter += 1

            regex_list.append(["Status", page, change_property, counter, text, time_value])
        else:
            # counter = 0
            counter += 1
            regex_list.append(["Status", page, change_property, counter, text, time_value])  # Has to be brackets so we can edit later
        # Problem with a page where there isn't a header, there isn't a clean event break, to start counting by 1's
        # and then pairing up the attributes with the people.
        # Potential solution = if the preceeding value had a comma, and this one doesn't, reset the counter
        # Affirmative - This solved it.

# Taking the attributes and adding 1 to the odd numbers so that they match the person in the join later
for item in regex_list:
    if item[0] == 'Status' and item[3] & 1:  # x & 1 -- if True, then number is odd, else false
        item[0] = 'Room'
        item[3] += 1
    else:
        continue

# Creating Pandas Dataframe from list
# http://pbpython.com/pandas-list-dict.html

labels = ['RowType', 'Page', 'Change_Property', 'Counter', 'Value', 'Time']
df = pd.DataFrame.from_records(regex_list, columns=labels)

# df.to_excel('outputtest2.xlsx')


# df_deduped = df.drop_duplicates()  # Can't drop duplicates here... second page people won't get the joins...

# How to subset dataframes in pandas
# https://chrisalbon.com/python/pandas_index_select_and_filter.html
df_room = df[df['RowType'] == 'Room']
df_people = df[df['RowType'] == 'Person']
df_status = df[df['RowType'] == 'Status']

# Joining dataframes together (like SQL)
# https://pandas.pydata.org/pandas-docs/stable/comparison_with_sql.html#compare-with-sql-join
merge_test = pd.merge(df_people, df_room, 'inner', on=['Counter', 'Time', 'Page', 'Change_Property'])

merge_test = pd.merge(merge_test, df_status, 'left', on=['Counter', 'Time', 'Page', 'Change_Property'])

final_df = df_people.merge(df_room, 'inner', on=['Counter', 'Time', 'Page', 'Change_Property'])
final_df = final_df.merge(df_status, 'left', on=['Counter', 'Time', 'Page', 'Change_Property'])

final_df.to_excel('rawoutput.xlsx')

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


