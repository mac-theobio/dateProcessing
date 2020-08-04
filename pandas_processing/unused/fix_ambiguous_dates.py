# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
# Imports 
from date_utils import *
from copy import deepcopy



for sheet_name in ['example1_adj.xlsx']:
    # Load sheet
    sheet_0 = pd.read_excel(sheet_name)

    initial_valid_date = pd.to_datetime('2020-Feb-01') # Initial time specified in Jonathan's email

    final_valid_date = pd.to_datetime(getmtime(sheet_name), unit='s') # Time of last modification

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
            unambiguous_sheet[col] = line_fill_ambiguous_date(unambiguous_sheet[col], sheet_0[col], 5) 
            while not unambiguous_sheet[col].equals(last_col_version):
                last_col_version = deepcopy(unambiguous_sheet[col])
                unambiguous_sheet[col] = line_fill_ambiguous_date(unambiguous_sheet[col], sheet_0[col], 5) 
                i += 1
                if i > 100:
                    break
            print(col +' has been modified '+str(i) + ' times by iterative column fill method')

    unambiguous_sheet = row_fill_ambiguous_date(unambiguous_sheet, sheet_0)

    unambiguous_sheet.to_excel(sheet_name.split('.')[0] +'_cleaned.xlsx', index=False)





# %%
