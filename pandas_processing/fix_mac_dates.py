# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
import pandas as pd
import numpy as np
from datetime import datetime
from os.path import getmtime


# %%
def date_recast(date, start_date, end_date):
    date1 = date
    if pd.isna(date1):
        return np.nan
    modern_date = pd.to_datetime('1899-Dec-30')    
    mac_date = pd.to_datetime('1904-Jan-01')    

    if type(date1) == int:
        date1 = pd.Timedelta(date1, unit='d') + modern_date
    elif type(date1) == str:
        date1 = pd.to_datetime(date1, errors='coerce')
        if pd.isna(date1):
            return np.nan

    delta = date1 - modern_date
    internal_integer = int(float(delta.days) + (float(delta.seconds) / 86400))

    dt_modern =  pd.Timedelta(internal_integer, unit='d') + modern_date
    dt_mac = pd.Timedelta(internal_integer, unit='d') + mac_date

    dt_modern_valid = (dt_modern >= start_date) and (dt_modern <= end_date)
    dt_mac_valid = (dt_mac >= start_date) and (dt_mac <= end_date)

    if dt_modern_valid and (not dt_mac_valid):
        return dt_modern.date()
    elif dt_mac_valid and (not dt_modern_valid):
        return dt_mac.date()
    elif dt_modern_valid and dt_mac_valid:
        return "%Both formats are valid%"
    elif (not dt_modern_valid) and (not dt_mac_valid):
        return "%Both formats are invalid%"


# %%
sheet_name = 'example2_adj.xlsx'
sheet_0 = pd.read_excel(sheet_name)


# %%

start_date = pd.to_datetime('2020-Feb-01')
end_date = pd.to_datetime(getmtime(sheet_name), unit='s') # Time of last modification


# %%
for col in sheet_0:
    if col.find('date') != -1:
        recasted = []
        for date in sheet_0[col]:
            recasted.append(date_recast(date, start_date, end_date))
        sheet_0[col] = recasted


# %%
sheet_0.to_excel('example2_macdates_fixed.xlsx', index=False)


# %%



