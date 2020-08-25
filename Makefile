## This is MacTheobio dateProcessing

current: target
-include target.mk

-include makestuff/perl.def

vim_session:
	bash -cl "vmt"

######################################################################

Sources += Makefile README.md

######################################################################

Ignore += secret
secret:
	ln -s ~/Dropbox/dateFiles $@

Ignore += example
example:
	ln -s ~/Dropbox/dateProcessing $@
example/%: example ;
	$(lscheck)

######################################################################

## 2020 Jul 24 (Fri)
## JD: Started with perl when subsetting was a problem.
## Didn't really get anywhere

Sources += subset.pl
Ignore += tahawus.subset.xlsx
tahawus.subset.xlsx: secret/tahawus.xlsx subset.pl
	$(PUSH)

######################################################################

Sources += $(wildcard *.R)

## 2020 Jul 28 (Tue)
## JD: If we read twice, we should be able to use R tools

doubleDate.Rout: doubleDate.R example/example1_adj.xlsx
	$(makeR)

denali.xlsx: secret/denali.xlsx pandas_processing/clean_dates.py
	python3 pandas_processing/clean_dates.py $< $@ \
	--sheet_name LineList --skiprows 1

example1_cleaned.xlsx: example/example1_adj.xlsx pandas_processing/clean_dates.py
	python3 pandas_processing/clean_dates.py $< $@

Logan_cleaned.xlsx: example/Logan.xlsx
	python3 pandas_processing/clean_dates.py $< $@

######################################################################

### Makestuff

Ignore += makestuff
msrepo = https://github.com/dushoff

Makefile: makestuff/Makefile
makestuff/Makefile:
	git clone $(msrepo)/makestuff
	ls makestuff/Makefile

-include makestuff/os.mk

-include makestuff/makeR.mk

-include makestuff/git.mk
-include makestuff/visual.mk
