# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
# Imports 
import pandas as pd
import datetime
import numpy as np
from os.path import getmtime
from copy import deepcopy
# import openpyxl as px


# %%
def get_unambiguous_date_values(col, initial_valid_date, final_valid_date):
    """
    Given an input date column, return a column cleaned of any invalid dates, while enforcing that each date must be between 
    initial_valid_date and final_valid_date.
    Args:
        col (pd.Series): input date column
        initial_valid_date (pd.Timestamp)
        final_valid_date (pd.Timestamp)
    Returns:
        col (list): output date column, meant to be changed back into pd.Series
    """
    # I would also check whether or not the date (as string) had any of the month strings in it, but read_excel AND openpyxl automatically coerce these to numeric dates. It seems like the only way to get the string input is to deal with the files as csv.abs
    this_column = []
    for i, date in enumerate(col):
        converted_first_datetime = pd.to_datetime(date, errors='coerce').date() # Attempt to coerce each cell to datetime format.

        if not pd.isna(converted_first_datetime):  # If time cannot be coerced to datetime, then it cannot be unambiguous.
            is_original_valid = (converted_first_datetime >= initial_valid_date) and (converted_first_datetime <= final_valid_date)

            if converted_first_datetime.day > 12: # If the day > 12, then datetime is not ambiguous as there is no month with number > 12.
                if is_original_valid:
                    this_column.append(converted_first_datetime)
                else:
                    this_column.append('%COMPLETELY_INVALID_DATE%')
            elif converted_first_datetime.day == converted_first_datetime.month: # If day == month, we don't care what the exact formatting was.
                if is_original_valid:
                    this_column.append(converted_first_datetime)
                else:
                    this_column.append('%COMPLETELY_INVALID_DATE%')
            else: # We then test for dates being within initial_valid_date and final_valid_date. 
                str_original = str(converted_first_datetime)
                alternative_date = pd.to_datetime(str_original[:4] + '-' + str_original[-2:] + '-' + str_original[5:7]).date()

                is_original_valid = (converted_first_datetime >= initial_valid_date) and (converted_first_datetime <= final_valid_date)
                is_alternative_valid = (alternative_date >= initial_valid_date) and (alternative_date <= final_valid_date)
                
                if is_original_valid and (not is_alternative_valid): # If only original is valid, then infer datetime is original.
                    this_column.append(converted_first_datetime)
                elif (not is_original_valid) and is_alternative_valid: # If only alternative is valid, then infer datetime is alternative.
                    this_column.append(alternative_date)
                elif is_original_valid and is_alternative_valid: # If both are valid, then datetime is ambiguous.
                    this_column.append('%AMBIGUOUS_VALID_DATE%')
                elif (not is_original_valid) and (not is_alternative_valid): # If neither are valid, then there must have been an input error.
                    this_column.append('%COMPLETELY_INVALID_DATE%')
                else:
                    raise Exception('This line should never run. This is left for debugging purposes.')
        else:
            this_column.append(np.nan)
    return this_column


# %%
def line_fill_ambiguous_date(ambiguous_column, original_column, searchradius = 5):
    """ 
    Given an input date column output from get_ambiguous_date_values, return a column with possibly fewer ambiguous values as a result of 
    guessing that ambiguous dates are closer in value to nearby dates. May need to be run multiple times.
    Args:
        ambiguous_column (pd.Series): output of get_ambiguous_date_values called on original_column.
        original_column (pd.Series): 
        searchradius (int): Number of cells up/down to search
    Returns:
        list
    """
    new_column = []

    for i, date in enumerate(ambiguous_column):
        if date == '%AMBIGUOUS_VALID_DATE%':
            original_date = pd.to_datetime(original_column[i], errors='coerce').date() 
            str_original = str(original_date)
            alternative_date = pd.to_datetime(str_original[:4] + '-' + str_original[-2:] + '-' + str_original[5:7]).date()
            
            dates_nearby = np.concatenate([ambiguous_column[max(i-searchradius, 0):i], ambiguous_column[i+1: min(i+1+searchradius, len(ambiguous_column))]]) # Look for dates vertically in the file with a search radius of searchradius
            dates_nearby = sorted(list(filter(lambda x: type(x)==datetime.date, dates_nearby))) # Filter those dates which are actually dates, and non-ambiguous
         #   dates_nearby = list(filter(lambda x: (np.abs(x-original_date).days < 365) or (np.abs(x-alternative_date).days < 365), dates_nearby)) # Filter those dates which are within a year of the possible date of comparison
            
            # If there exist dates nearby, take the median of these dates.
            if dates_nearby != []: 
                median_date = dates_nearby[int(len(dates_nearby)/2)]
            else:
                median_date = np.nan
            
            # If there doesn't exist dates nearby, we have to leave it ambiguous for now. 
            if pd.isna(median_date):
                new_column.append('%AMBIGUOUS_VALID_DATE%')
            else:
                # If the median date exists, take the possible date which is closer to the median date. 

                original_date = pd.to_datetime(original_column[i], errors='coerce').date() 
                str_original = str(original_date)
                alternative_date = pd.to_datetime(str_original[:4] + '-' + str_original[-2:] + '-' + str_original[5:7]).date()
                
                if np.abs(original_date - median_date) < np.abs(alternative_date - median_date):
                    new_column.append(original_date)
                else:
                    new_column.append(alternative_date)

        else:
            new_column.append(date)

    return new_column


# %%
def row_fill_ambiguous_date(ambiguous_df, original_df):
    """ 
    Given an input dataframe with ambiguous dates, return a dataframe with possibly fewer ambiguous dates as a result of guessing that 
    ambiguous dates are closer in value the median date of cells in its row.
    Args:
        ambiguous_df (pd.DataFrame): output of get_ambiguous_date_values called on every row in original dataframe.
        original_df (pd.DataFrame)
    Returns:
        list
    """
    new_df = deepcopy(ambiguous_df)

    for i_row, row in new_df.iterrows():
        for i_col, date in enumerate(row):
            dates_nearby = sorted(list(filter(lambda x: type(x)==datetime.date, row))) # Consider the other, non-ambiguous dates in each row.

            if date == '%AMBIGUOUS_VALID_DATE%': 
                if dates_nearby != []:
                    median_date = dates_nearby[int(len(dates_nearby)/2)]
                else:
                    median_date = np.nan

                if not pd.isna(median_date):
                    original_date = pd.to_datetime(original_df.iloc[i_row][i_col], errors='coerce').date() 
                    str_original = str(original_date)
                    alternative_date = pd.to_datetime(str_original[:4] + '-' + str_original[-2:] + '-' + str_original[5:7]).date()
                    
                    if np.abs(original_date - median_date) < np.abs(alternative_date - median_date):
                        row[new_df.columns[i_col]] = original_date
                    else:
                        row[new_df.columns[i_col]] = alternative_date
                    new_df.iloc[i_row] = row
                else:
                    new_df.iloc[i_row][i_col] ='%AMBIGUOUS_VALID_DATE%'

    return new_df


for sheet_name in ['example1_adj.xlsx']:
    # Load sheet
    sheet_0 = pd.read_excel(sheet_name)

    initial_valid_date = pd.to_datetime('2020-Feb-01') # Initial time specified in Jonathan's email

    final_valid_date = pd.to_datetime(getmtime(sheet_name), unit='s') # Time of last modification

    # coerce all dates to 2020
    for col in sheet_0.columns:
        replacement_row = []
        if col.find('date') != -1:
            for date in sheet_0[col]:
                converted_first_datetime = pd.to_datetime(date, errors='coerce').date() # Attempt to coerce each cell to datetime format.
                try:
                    if not pd.isna(converted_first_datetime):
                        converted_first_datetime = pd.to_datetime("2020" + str(converted_first_datetime)[4:], errors='coerce').date()
                    else: 
                        converted_first_datetime = pd.NaT
                except IndexError:
                    converted_first_datetime = pd.NaT
                replacement_row.append(converted_first_datetime)
            sheet_0[col]= replacement_row

    unambiguous_sheet = pd.DataFrame()
    for col in sheet_0.columns:
        if col.find('date') != -1:
            unambiguous_sheet[col] =get_unambiguous_date_values(sheet_0[col], initial_valid_date, final_valid_date)
        else: 
            unambiguous_sheet[col] = sheet_0[col]

    for col in sheet_0.columns:
        i = 0
        if col.find('date') != -1:
            last_col_version = deepcopy(unambiguous_sheet[col])
            unambiguous_sheet[col] = line_fill_ambiguous_date(unambiguous_sheet[col], sheet_0[col], 7) 
            while not unambiguous_sheet[col].equals(last_col_version):
                last_col_version = deepcopy(unambiguous_sheet[col])
                unambiguous_sheet[col] = line_fill_ambiguous_date(unambiguous_sheet[col], sheet_0[col], 7) 
                i += 1
                if i > 100:
                    break
            print(i)

    unambiguous_sheet = row_fill_ambiguous_date(unambiguous_sheet, sheet_0)

    unambiguous_sheet.to_excel(sheet_name.split('.')[0] +'_cleaned.xlsx', index=False)



# %%
