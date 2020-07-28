library(readxl)
library(dplyr)
library(anytime)
library(zoo)

## makeR
source("makestuff/makeRfuns.R")
commandEnvironments()

## Define functions

## Read files
inf <- matchFile("xlsx$")
datef <- read_excel(inf, col_types = "date")
textf <- read_excel(inf, col_types = "text")
date_pos <- which(grepl("date",names(datef),ignore.case=TRUE))

## Close
saveVars(readf)
