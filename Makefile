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

## Nonsense example for Matt
clean.xlsx: dirty.xlsx script.py
	python3 -f script.py < dirty.xlsx > clean.xlsx
	python3 -f script.py --args rowclean=0 < dirty.xlsx > clean.xlsx

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
