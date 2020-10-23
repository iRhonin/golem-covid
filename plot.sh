#! /bin/sh

set -e

/usr/local/bin/python3 /golem/plot.py --date $1 --data $2 --country-codes $3 --output $4 --parameter $5
