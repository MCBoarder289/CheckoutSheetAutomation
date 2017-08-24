import re

"""

Function that takes the pages of text and iterates line by line to grab only the relevant information:
(Person, Attributes about that person like Service Time and Location)

References:

Returning the regular expression match -- .group(0)
https://stackoverflow.com/questions/18493677/how-do-i-return-a-string-from-a-regex-match-in-python

How to iterate through the lines of the long single text string with /n line breaks
https://stackoverflow.com/questions/22918013/python-iterate-over-a-string-containing-newlines

NEED TO MAKE SURE THAT WE ALWAYS FOLLOW THESE RULES:
    NEVER PUT A COMMA IN A ROOM NAME OR ROLE NAME, NEVER PUT "Regulars" IN A ROOM NAME OR A ROLE NAME
    NEVER PUT "Sunday Morning - " IN A ROOM NAME OR ROLE NAME

"""


def process_text_pages(text_pages):
    regex_list = []
    change_property = 0
    for text_page in text_pages:
        page_regex_list = __process_page(change_property, text_page)
        regex_list.extend(page_regex_list)

    print(regex_list)
    # Taking the attributes and adding 1 to the odd numbers so that they match the person in the join later
    for item in regex_list:
        if item[0] == 'Status' and item[3] & 1:  # x & 1 -- if True, then number is odd, else false
            item[0] = 'Room'
            item[3] += 1

    return regex_list


"""
Lines go from upper left of page in columns all the way down until the last name on the page,
then it goes to the top of the page on the right side and down that column,
and finally it goes through the middle of the page (2 check ins).

Seems to be doubling the number of pages per single instance of "2 check ins" (2 pages = 4 pages)
Pages without "2 check ins" don't seem to duplicate

counter = The way we count which propery goes with which person. This will reset upon a page change

"""


def __process_page(change_property, text_page):
    page = text_page.page_number
    counter = 0
    change_count = 0
    previous_row_type = ''
    page_regex_list = []

    for text in text_page.text.splitlines():
        if text == "":  # If it's blank, skip it
            continue
        if re.search('Regulars', text):  # If it has "Regulars", it's an aggregate count row, so skip it
            continue
        if re.search('Sunday Morning - ',
                     text):  # It's the title row "Sunday Morning - <date>", therefore skip
            continue
        if re.search('Check-Ins', text):  # Take's out the "2 Check-Ins" property that we don't want
            continue
        if re.search('\d\d:\d\d[ap]',
                     text):  # If it has the time, reset the counter, create the time_value to pass on
            counter = 0
            time_value = re.search('\d\d:\d\d[ap]', text)
            time_value = time_value.group(0)
        elif re.search('\d:\d\d[ap]',
                       text):  # If it has the time, reset the counter, create the time_value to pass on
            counter = 0
            time_value = re.search('\d:\d\d[ap]', text)
            time_value = time_value.group(0)
        elif re.search(',',
                       text):  # If it has a comma, it's a name, so add 2 to the counter (2 elements to match)
            if previous_row_type == "Status":  # previous_marker == 0:  # If the preceeding element was a Status and not a person,
                counter = 0  # reset the counter (new page)
                change_count += 1

            if change_count > 1:
                change_count = 0
                change_property += 1

            counter += 2
            previous_row_type = "Person"
            page_regex_list.append(("Person", page, change_property, counter, text, time_value))

        else:  # Otherwise, simply add one to the counter. Name counter = 2nd value's counter, and 1st values's counter - 1
            if previous_row_type != "Status":
                previous_row_type = "Status"
                change_count += 1

                if change_count > 1:
                    change_count = 0
                    change_property += 1

                counter = 0
                counter += 1

                page_regex_list.append(["Status", page, change_property, counter, text, time_value])
            else:
                counter += 1
                page_regex_list.append(["Status", page, change_property, counter, text, time_value])
                # Problem with a page where there isn't a header, there isn't a clean event break, to start counting by 1's
                # and then pairing up the attributes with the people.
                # Potential solution = if the preceding value had a comma, and this one doesn't, reset the counter
                # Affirmative - This solved it.

    return page_regex_list
