current: target

all: requirements.out example1_adj.xlsx example2_adj.xlsx example1_cleaned.xlsx example2_cleaned.xlsx rm_out

requirements.out: requirements.txt
	pip3 install -r $< > $@

example1_adj.xlsx:
	wget -O $@ https://uc21db27d4d9cc8d574934133ad9.dl.dropboxusercontent.com/cd/0/get/A80NIay6x1oxTxZMqN3wqXZd33gXoSnjzcGDBeTdedX5nlkCRffBydKZejYfXOB_HUY0D2wOuPmfu6HQod-LeKBkGozWjyuDK-qktUZ4fbDJC_Ig3VsrmZZwr4u8cucatEg/file?_download_id=10553197207513454960554973527669745454949470181373895879079405673&_notify_domain=www.dropbox.com&dl=1

example2_adj.xlsx:
	wget -O $@ https://ucbcbcdcf1cbf1ae759b4cfd5482.dl.dropboxusercontent.com/cd/0/get/A83mOeyEqdFFi7gtyP0LVn6qycSP6SMdrOxrFvLNvYjdP9yBEwNMRI-K0FlEcvZhuei4GdD8Z5VJoX2HnTvsuzPyKaar4_nLhMqD1mYy6b6u1RAcE8zugpjnB3ocu9AM1I8/file?_download_id=30545726771684567305518766315707435129263559165761876397337660669&_notify_domain=www.dropbox.com&dl=1

example1_cleaned.xlsx: example1_adj.xlsx
	python clean_dates.py $< $@ --fix_mac 0

example2_cleaned.xlsx: example2_adj.xlsx
	python clean_dates.py $< $@ --infer_cols 0 --infer_rows 0 

rm_out: requirements.out
	rm $< 

-include target.mk
