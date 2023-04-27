#!/bin/bash

# Bash script for serializing the entire dta

DTAPART="dtak" # or "dtae"
TASTE="original" # or "original"
SRCDIR="/home/bracke/data/dta/ddc_tabs/$DTAPART/"
TARGETDIR="/home/bracke/data/dta/txt"/${TASTE:0:4}/$DTAPART
mkdir -p $TARGETDIR

source .venv/bin/activate
for FILE in $SRCDIR/*/*; 
do
    BASE=`basename $FILE`
    BASE_NOEXT="${BASE%%.*}"
    echo "Serializing $BASE_NOEXT ..."
    if [[ $TASTE == "original" ]]; then
        python3 serialize.py -t $TASTE --remove-unwanted-spaces $FILE > $TARGETDIR/$BASE_NOEXT.txt
    elif [[ $TASTE == "normalized" ]]; then
        python3 serialize.py -t $TASTE --replace-tokens=./lex/dta-replacements.txt --remove-unwanted-spaces --replace-underscores $FILE > $TARGETDIR/$BASE_NOEXT.txt
    else
        echo ""
    fi

done

deactivate;