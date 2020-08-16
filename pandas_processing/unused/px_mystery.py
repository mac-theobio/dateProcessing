# %%
import openpyxl as px

wb = px.load_workbook('example2_adj.xlsx')
ws =wb.active

# These should, in theory, be different!

for i in range(1, 100):
    print(ws['B'+ str(i)].base_date)

# %%
