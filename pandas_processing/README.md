
You need to download the example files and put it somewhere, and you may need to install requirements from requirements.txt. 
(If using linux, run: make)

Then, run python clean_dates.py {path to file} {path to output file} 

with any optional arguments you'd like. 

Clean a file containing dates (with column headers containing "date")

positional arguments:
  file                  path to file
  output_file           path to output file

optional arguments:
  -h, --help            show this help message and exit
  --init_date INIT_DATE
                        initial date as string. Please do not enter an
                        ambiguous date. Default 2020-Feb-01
  --fix_mac FIX_MAC     Whether or not to attempt to fix pre-mac 2011 dates. 0
                        (False) or 1 (True), default 1
  --infer_cols INFER_COLS
                        Whether or not to attempt to infer dates from nearby
                        dates in the same column. 0 (False) or 1 (True),
                        default 1
  --infer_rows INFER_ROWS
                        Whether or not to attempt to infer dates from nearby
                        dates in the same row. 0 (False) or 1 (True), default
                        1
  --searchrx SEARCHRX   Search radius for date inferencing from same column.
                        Default 7