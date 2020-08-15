import argparse
from date_utils import *
from copy import deepcopy

parser = argparse.ArgumentParser(description='Clean a file containing dates (with column headers containing "date")')
parser.add_argument('file', action='store', type=str, help='path to file')
parser.add_argument('output_file', action='store', type=str, help='path to output file')
parser.add_argument('--sheet_name', dest='sheet_name', nargs=1, action='store', type=str, help='name of worksheet sheet', default=['Sheet1'])
parser.add_argument('--init_date', dest='init_date', nargs=1, action='store', type=str, help='initial date as string. Please do not enter an ambiguous date. Default 2020-Feb-01', default=['2020-Feb-01'])
parser.add_argument('--fix_mac', dest='fix_mac', nargs=1, action='store', type=int, help='Whether or not to attempt to fix pre-mac 2011 dates. 0 (False) or 1 (True), default 1', default=[1])
parser.add_argument('--infer_cols', dest='infer_cols', nargs=1, action='store', type=int, help='Whether or not to attempt to infer dates from nearby dates in the same column.  0 (False) or 1 (True), default 1', default=[1])
parser.add_argument('--infer_rows', dest='infer_rows', nargs=1, action='store', type=int, help='Whether or not to attempt to infer dates from nearby dates in the same row.  0 (False) or 1 (True), default 1', default=[1])
parser.add_argument('--searchrx', dest='searchrx', nargs=1, action='store', type=int, help='Search radius for date inferencing from same column. Default 7', default=[7])
args = parser.parse_args()

infile = args.file
print('Reading excel file... ')
## sheet_0 = pd.read_excel(infile)
sheet_0 = ((pd.read_excel(infile, args.sheet_name)).values)[0]

start_date = pd.to_datetime(args.init_date[0])
end_date = pd.to_datetime(getmtime(infile), unit='s') # Time of last modification

if args.fix_mac[0]:
    print('Casting mac-pre2011 dates to modern dates')
    for col in sheet_0:
        if col.find('date') != -1:
            print('Working on column: ' + col)
            recasted = []
            for date in sheet_0[col]:
                recasted.append(date_recast(date, start_date, end_date))
            sheet_0[col] = recasted
    unambiguous_sheet = sheet_0

if args.infer_cols[0] or args.infer_rows[0]:
    print('Inferring columns or rows.')

    print('Getting unambiguous dates.')
    unambiguous_sheet = pd.DataFrame()
    for col in sheet_0.columns:
        if col.find('date') != -1:
            unambiguous_sheet[col] =get_unambiguous_date_values(sheet_0[col], start_date, end_date)
        else: 
            unambiguous_sheet[col] = sheet_0[col]


    if args.infer_cols[0]:
        print('Inferring columns.')
        for col in sheet_0.columns:
            i = 0
            if col.find('date') != -1:
                last_col_version = deepcopy(unambiguous_sheet[col]).tolist()
                new_col = line_fill_ambiguous_date(unambiguous_sheet[col], sheet_0[col], args.searchrx[0])

                while not new_col == last_col_version:
                    last_col_version = deepcopy(new_col)
                    new_col = line_fill_ambiguous_date(new_col, sheet_0[col], args.searchrx[0]) 
                    i += 1
                    if i > 100:
                        break
                unambiguous_sheet[col] = new_col
                print(col +' has been modified '+str(i) + ' times by iterative column fill method')
    if args.infer_rows[0]:
        print('Inferring rows.')
        unambiguous_sheet = row_fill_ambiguous_date(unambiguous_sheet, sheet_0)
else:
    print('Skipping column/row inference.')

unambiguous_sheet.to_excel(args.output_file, index=False)




