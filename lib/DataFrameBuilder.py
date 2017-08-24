import pandas as pd

"""

Builds a pandas dataframe out of the information extracted from PDF data

References:


Creating Pandas Dataframe from list
http://pbpython.com/pandas-list-dict.html
    
Joining dataframes together (like SQL)
https://pandas.pydata.org/pandas-docs/stable/comparison_with_sql.html#compare-with-sql-join

How to subset dataframes in pandas
https://chrisalbon.com/python/pandas_index_select_and_filter.html
"""


def build_data_frame(page_data):
    labels = ['RowType', 'Page', 'Change_Property', 'Counter', 'Value', 'Time']
    df = pd.DataFrame.from_records(page_data, columns=labels)

    # df_deduped = df.drop_duplicates()  # Can't drop duplicates here... second page people won't get the joins...

    df_room = df[df['RowType'] == 'Room']
    df_people = df[df['RowType'] == 'Person']
    df_status = df[df['RowType'] == 'Status']

    # merge_test = pd.merge(df_people, df_room, 'inner', on=['Counter', 'Time', 'Page', 'Change_Property'])

    # merge_test = pd.merge(merge_test, df_status, 'left', on=['Counter', 'Time', 'Page', 'Change_Property'])

    final_df = df_people.merge(df_room, 'inner', on=['Counter', 'Time', 'Page', 'Change_Property'])
    final_df = final_df.merge(df_status, 'left', on=['Counter', 'Time', 'Page', 'Change_Property'])

    # Filter to just these 4 columns
    final_df = final_df.filter(items=['Value_x', 'Time', 'Value_y', 'Value'])
    # Drop all duplicates
    final_df = final_df.drop_duplicates()
    # Filter out Volunteers
    final_df = final_df[final_df['Value'] != 'Volunteer']
    # Rename Columns
    final_df.columns = ['Name', 'Time', 'Room', 'Status']
    # Add Tab Column
    final_df['Tab'] = final_df['Time'] + ' ' + final_df['Room']
    # Replace Colons in Numbers for Tab Names (bad for tab names in excel)
    final_df['Tab'].replace(to_replace=':', value='', regex=True, inplace=True)
    # Resetting the row count
    final_df = final_df.reset_index(drop=True)

    # List Unique Values in a Column #
    tabs = final_df['Tab'].unique().tolist()
    tabs_df_list = {}

    # Loop through each tab, and create a list of dataframes for each tab to be then added into the excel workbook
    for i, tab in enumerate(tabs):
        df = final_df[final_df['Tab'] == tab]
        df = df.filter(items=['Name', 'Time', 'Room'])
        tabs_df_list["{0}".format(tab)] = df

    return tabs, tabs_df_list
