import pandas as pd
import numpy as np
from datetime import datetime
from os.path import getmtime
from copy import deepcopy
import dateutil

def date_recast(date, start_date, end_date):
    date1 = date
    if pd.isna(date1):
        return np.nan, "" #"Error: Either no value given or not detected as a date."
    modern_date = pd.to_datetime('1899-Dec-30')    
    mac_date = pd.to_datetime('1904-Jan-01')    

    if type(date1) == int:
        date1 = pd.Timedelta(date1, unit='d') + modern_date
    else:
        date1 = pd.to_datetime(date1, errors='coerce')
        if pd.isna(date1):
            return np.nan, "Error: Both modern and mac-pre2011 formats are invalid"

    delta = date1 - modern_date
    internal_integer = int(float(delta.days) + (float(delta.seconds) / 86400))

    dt_modern =  pd.Timedelta(internal_integer, unit='d') + modern_date
    dt_mac = pd.Timedelta(internal_integer, unit='d') + mac_date

    try:
        str_modern = str(dt_modern.date())
        alternative_modern = pd.to_datetime(str_modern[:4] + '-' + str_modern[-2:] + '-' + str_modern[5:7]).date()
        dt_modern_valid = ((dt_modern >= start_date) and (dt_modern <= end_date)) or ((alternative_modern >= start_date) and (alternative_modern <= end_date))
    except dateutil.parser._parser.ParserError:
        dt_modern_valid = ((dt_modern >= start_date) and (dt_modern <= end_date))

    try:
        str_mac = str(dt_mac.date())
        alternative_mac = pd.to_datetime(str_mac[:4] + '-' + str_mac[-2:] + '-' + str_mac[5:7]).date()
        dt_mac_valid = ((dt_mac >= start_date) and (dt_mac <= end_date)) or ((alternative_mac >= start_date) and (alternative_mac <= end_date))
    except dateutil.parser._parser.ParserError:
        dt_mac_valid = ((dt_mac >= start_date) and (dt_mac <= end_date))

    if dt_modern_valid and (not dt_mac_valid):
        return dt_modern.date(), 'modern date'
    elif dt_mac_valid and (not dt_modern_valid):
        return dt_mac.date(), 'mac-pre2011 date'
    elif dt_modern_valid and dt_mac_valid:
        return np.nan, "Error: Both modern and mac-pre2011 formats are valid"
    elif (not dt_modern_valid) and (not dt_mac_valid):
        return np.nan, "Error: Both modern and mac-pre2011 formats are invalid"

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
    explanation_column = []
    this_column = []
    for i, date in enumerate(col):
        converted_first_datetime = pd.to_datetime(date, errors='coerce').date() # Attempt to coerce each cell to datetime format.

        if not pd.isna(converted_first_datetime):  # If time cannot be coerced to datetime, then it cannot be unambiguous.
            is_original_valid = (converted_first_datetime >= initial_valid_date) and (converted_first_datetime <= final_valid_date)

            if converted_first_datetime.day > 12: # If the day > 12, then datetime is not ambiguous as there is no month with number > 12.
                if is_original_valid:
                    this_column.append(converted_first_datetime)
                    explanation_column.append('Unambiguous: day >= 13')
                else:
                    this_column.append(np.nan)
                    explanation_column.append('Error: Both possible date versions are outside of specified date range.')
            elif converted_first_datetime.day == converted_first_datetime.month: # If day == month, we don't care what the exact formatting was.
                if is_original_valid:
                    this_column.append(converted_first_datetime)
                    explanation_column.append('Unambiguous: day number == month number.')
                else:
                    this_column.append(np.nan)
                    explanation_column.append('Error: Both possible date versions are outside of specified date range.')
            else: # We then test for dates being within initial_valid_date and final_valid_date. 
                str_original = str(converted_first_datetime)
                alternative_date = pd.to_datetime(str_original[:4] + '-' + str_original[-2:] + '-' + str_original[5:7]).date()

                is_original_valid = (converted_first_datetime >= initial_valid_date) and (converted_first_datetime <= final_valid_date)
                is_alternative_valid = (alternative_date >= initial_valid_date) and (alternative_date <= final_valid_date)
                
                if is_original_valid and (not is_alternative_valid): # If only original is valid, then infer datetime is original.
                    this_column.append(converted_first_datetime)
                    explanation_column.append('Inferred: Only this MM/DD or DD/MM combination is with in the specified date range.')
                elif (not is_original_valid) and is_alternative_valid: # If only alternative is valid, then infer datetime is alternative.
                    this_column.append(alternative_date)
                    explanation_column.append('Inferred: Only this MM/DD or DD/MM combination is with in the specified date range.')
                elif is_original_valid and is_alternative_valid: # If both are valid, then datetime is ambiguous.
                    this_column.append('%AMBIGUOUS_VALID_DATE%')
                    explanation_column.append('Ambiguous: 2 MM/DD or DD/MM combinations are within the specified date range.')
                elif (not is_original_valid) and (not is_alternative_valid): # If neither are valid, then there must have been an input error.
                    this_column.append(np.nan)
                    explanation_column.append('Error: Both possible date versions are outside of specified date range.')
                else:
                    raise Exception('This line should never run. This is left for debugging purposes.')
        else:
            this_column.append(np.nan)
            explanation_column.append("")#"Error: Either no value given or not detected as a date.")
    return this_column, explanation_column

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
    explanation_column = []
    for i, date in enumerate(ambiguous_column):
        if date == '%AMBIGUOUS_VALID_DATE%':
            original_date = pd.to_datetime(original_column[i], errors='coerce').date() 
            str_original = str(original_date)
            alternative_date = pd.to_datetime(str_original[:4] + '-' + str_original[-2:] + '-' + str_original[5:7]).date()
            
            dates_nearby = np.concatenate([ambiguous_column[max(i-searchradius, 0):i], ambiguous_column[i+1: min(i+1+searchradius, len(ambiguous_column))]]) # Look for dates vertically in the file with a search radius of searchradius

            dates_nearby = sorted(list(filter(lambda x: not pd.isna(pd.to_datetime(x, errors='coerce')), dates_nearby))) # Filter those dates which are actually dates, and non-ambiguous
            # If there exist dates nearby, take the median of these dates.
            if dates_nearby != []: 
                median_date = dates_nearby[int(len(dates_nearby)/2)]
            else:
                median_date = np.nan
            
            # If there doesn't exist dates nearby, we have to leave it ambiguous for now. 
            if pd.isna(median_date):
                new_column.append('%AMBIGUOUS_VALID_DATE%')
                explanation_column.append('Ambiguous: No unambiguous nearby dates in the same column on this iteration.')
            else:
                # If the median date exists, take the possible date which is closer to the median date. 
  
                original_date = pd.to_datetime(original_column[i], errors='coerce').date() 
                str_original = str(original_date)
                alternative_date = pd.to_datetime(str_original[:4] + '-' + str_original[-2:] + '-' + str_original[5:7]).date()
                
                if np.abs(original_date - median_date) < np.abs(alternative_date - median_date):
                    new_column.append(original_date)
                    explanation_column.append('Inferred: this date version is closer to the nearby dates in this column. Confidence: ' + str(np.abs(np.abs(alternative_date - median_date) - np.abs(original_date - median_date))))
                elif np.abs(original_date - median_date) > np.abs(alternative_date - median_date):
                    new_column.append(alternative_date)
                    explanation_column.append('Inferred: this date version is closer to the nearby dates in this column. Confidence: ' + str(np.abs(np.abs(alternative_date - median_date) - np.abs(original_date - median_date))))
                else:
                    new_column.append('%AMBIGUOUS_VALID_DATE%')
                    explanation_column.append('Ambiguous: Both date versions are the same distance from the median nearby date.')
        else:
            new_column.append(date)
            explanation_column.append('')

    return new_column, explanation_column


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
    zero_stamp = pd.to_datetime('Jan 01, 2020')
    explanation_df = deepcopy(new_df)
    explanation_df[:] = ""

    for i_row, row in new_df.iterrows():
        for i_col, date in enumerate(row):
            if date == '%AMBIGUOUS_VALID_DATE%': 
                dates_nearby = [pd.to_datetime(x) for x in list(filter(lambda x: not pd.isna(pd.to_datetime(x, errors='coerce')), row))] # Consider the other, non-ambiguous dates in each row.
                dates_nearby = list(filter(lambda x: (x - zero_stamp).days > 0, dates_nearby))

                if dates_nearby != []:
                    median_date = dates_nearby[int(len(dates_nearby)/2)].date()
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
                    explanation_df.iloc[i_row, i_col] = "Inferred: using nearby dates in same row. Confidence: " + str(np.abs(np.abs(original_date - median_date) - np.abs(alternative_date - median_date)))
                else:
                    new_df.iloc[i_row, i_col] ='%AMBIGUOUS_VALID_DATE%'

    return new_df, explanation_df