# `serialize-dta-ddctabs`

Python scripts for serializing DTA documents stored in the [`dcc_tabs`
format](https://kaskade.dwds.de/~moocow/software/ddc/ddc_tabs.html).

## Usage

```bash
source .venv/bin/activate
python3 serialize.py --taste={} [--orthography-replace=LEXICON] [--remove-unwanted-spaces]
```




## Requirements

Python3.8

See `requirements.txt`

Set up virtual environment like this:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

