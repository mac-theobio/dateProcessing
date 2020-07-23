## This is MacTheobio dateProcessing

current: target
-include target.mk

-include makestuff/perl.def

vim_session:
	bash -cl "vmt"

######################################################################

Sources += Makefile README.md

######################################################################

Ignore += secret/

secret:
	ln -s ~/Dropbox/dateFiles $@

tahawus.subset.xlsx: secret/tahawus.xlsx subset.pl
	$(PUSH)

######################################################################

### Makestuff

Ignore += makestuff
msrepo = https://github.com/dushoff

Makefile: makestuff/Makefile
makestuff/Makefile:
	git clone $(msrepo)/makestuff
	ls makestuff/Makefile

-include makestuff/os.mk

## -include makestuff/wrapR.mk

-include makestuff/git.mk
-include makestuff/visual.mk
