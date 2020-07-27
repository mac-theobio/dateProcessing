# Imports 
import pandas as pd
import datetime
import numpy as np
# import openpyxl as px

# Load sheet
sheet_0 = pd.read_excel('example1_adj.xlsx')

# Column 'date1' looks like it has no issues, so I infer dates based on this column for now. 
# Inferring dates based on nearby dates is also feasible.
reliable_column = sheet_0['date1']
reliable_column = pd.DatetimeIndex(pd.to_datetime(reliable_column, errors='coerce')).date
sheet_0['date1'] = reliable_column

keep_nondate_descriptors = False

# Main loop.

for col in sheet_0.columns: # Iterate over each column
    if col.find('date') != -1 and col != 'date1': # If the column is a date column and the column is not the column without issues:
        this_column = []
        for i, date in enumerate(sheet_0[col]):
            converted_first_datetime = pd.to_datetime(date, errors='coerce').date() # Attempt to coerce each cell to datetime format.
            
            if pd.isna(converted_first_datetime): # If the cell is not a valid datetime, remove if keep_nondate_descriptors is False.
                if not keep_nondate_descriptors:
                    this_column.append(converted_first_datetime)
                else:
                    this_column.append(date)

            elif converted_first_datetime.day > 12: # If the cell is not possibly ambiguous, don't change anything. 
                # TODO: Fix possible issue: datetimes entered with the month name are not ambiguous, but will be considered as such for now. 
                this_column.append(converted_first_datetime)
            else: # If the cell is possibly ambiguous, determine which format the string is likely to be based on the date's proximity to the date in date1.
                str_original = str(converted_first_datetime)
                comparator_date = reliable_column[i]
                alternative_date = pd.to_datetime(str_original[:4] + '-' + str_original[-2:] + '-' + str_original[5:7]).date()

                if np.abs(converted_first_datetime - comparator_date) < np.abs(alternative_date - comparator_date):
                    this_column.append(converted_first_datetime)
                else:
                    this_column.append(alternative_date)

        sheet_0[col] = this_column
sheet_0.to_excel('cleaned_example1.xlsx', index=False)


# %%
#sheet_0_excelload = px.load_workbook('example1_adj.xlsx')
#ws = sheet_0_excelload.active
#for col in ws.iter_cols():
#    for cell in col:
#        try:
#            if cell.row == 1:
#                cell.value = sheet_0.columns[cell.column-1]
#            else:
#                cell.value = sheet_0[sheet_0.columns[cell.column-1]].iloc[cell.row-2]
#        except KeyError:
#            cell.value = np.nan
#        except IndexError:
#            cell.value = np.nan
#sheet_0_excelload.save('cleaned_format_wip.xlsx')


