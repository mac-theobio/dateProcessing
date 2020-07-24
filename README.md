This is a public repo for working on tools to deal with dates entered in various terrible Excel formats. We have had various problems with R conversion programs, including problems with inconsistent formats (even within a column) and also date offsets.

We will build tools in python and maybe other programs to examine these columns, which will be taken from real confidential examples (which means we will also need tools to anonymize and subsample these files while preserving all of the weirdness)

We now have an [example file folder](https://www.dropbox.com/sh/it2bbrnpw28h0lw/AACehUATcoENEaUkeYbu2MaYa?dl=0)

The first goal _was_ a function that can take a Excel file and a list of rows and columns to select, and return an Excel file otherwise identical to the original, but with _only_ the selected rows and columns. This still seems like an interesting goal, and I guess Matthew has made some progress.
