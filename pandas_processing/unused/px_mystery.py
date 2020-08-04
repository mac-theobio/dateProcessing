# %%
import openpyxl as px

wb = px.load_workbook('example2_adj.xlsx')
ws =wb.active

# These should, in theory, be different!
print(ws['B2'].base_date)
print(ws['B3'].base_date)

# %%
