# `serialize-dta-ddctabs`

Python script for serializing DTA documents stored in the [`dcc_tabs`
format](https://kaskade.dwds.de/~moocow/software/ddc/ddc_tabs.html). Files in
`ddc_tabs` format contain DTA documents in a tokenized and annotated form.

The basic serialization is done by joining all sentences on spaces or the empty
string (depending on the preceding word-separation symbol given in the ddc_tabs
entry for the token). This is identical to what
`kira:/home/wiegand/bin/dta2text.pl` does. 

Additionally, in the following modifications can be performed by setting a specific flag:

1. Replace words based on entries in a replacement lexicon. The replacement file
  must have a tab-separated structure, where every line looks like this:  
  `original-type{tab}new-type` (See the project `oldorth-list` for an example of
  how to compile such a lexicon for replacement of old orthography (pre-1996) by
  modern orthography on a type level ("dass" instead of "daß", etc.).)

2. Remove spaces between two capitalized words where the first one ends with a
  hypen ('Süd- Westen' -> 'Süd-Westen') 

3. Replace intra-word underscores by spaces ('musst_du' -> 'musst du')


## Usage

```
usage: serialize.py [-h] -t {normalized,lemmatized,original,transliterated}
                    [--replace-tokens LEXICON] [--replace-underscores] [--remove-unwanted-spaces]
                    file

Process a file with tab-separated attributes.

positional arguments:
  file                  File to process

optional arguments:
  -h, --help            show this help message and exit
  -t {normalized,lemmatized,original,transliterated}, --taste {normalized,lemmatized,original,transliterated}
                        Taste to output
  --replace-tokens LEXICON
                        Replace words based on entries in LEXICON (tab-separated)
  --replace-underscores
                        Replace intra-word underscores by spaces ('musst_du' -> 'musst du')
  --remove-unwanted-spaces
                        Remove spaces between two capitalized words where the first one ends with a
                        hypen ('Süd- Westen' -> 'Süd-Westen')

```

### Example call for an individual file:

```bash
source .venv/bin/activate

python3 serialize.py -t normalized --replace-tokens=/home/bracke/code/oldorth-list/out/dta-replacements.txt --remove-unwanted-spaces --replace-underscores /home/bracke/data/dta/ddc_tabs/dtak/corpus-tabs.d/birken_gespraechspiel_1665.TEI-P5.tabs > birken_gespraechspiel_1665.norm.txt
```

### Bash script for multiple files

Note: Change the values for the variables `DTAPART` and `TASTE` at the top of
the script for the desired version (original vs. normal), part of DTA (DTAK vs.
DTAE) and paths on your machine.

```bash
bash serialize-dta.sh
```

## Requirements

* Python3.8
* See `requirements.txt`

Set up virtual environment like this:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

