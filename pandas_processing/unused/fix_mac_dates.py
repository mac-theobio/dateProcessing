# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
import pandas as pd
import numpy as np
from datetime import datetime
from os.path import getmtime



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



