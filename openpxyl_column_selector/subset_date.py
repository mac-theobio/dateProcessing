import openpyxl as px
wb = px.load_workbook('messy_data.xlsx')
ws = wb.active
keep_columns = ['Date', 'arbitrary2']

i = 0
while ws.max_column > len(keep_columns):
    if list(ws.columns)[i][0].value in keep_columns:
        print('Found '+ list(ws.columns)[i][0].value)
        i += 1
    else:
        ws.delete_cols(i+1)
wb.save('clean_data.xlsx')