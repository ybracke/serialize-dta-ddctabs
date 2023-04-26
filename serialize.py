#!/usr/bin/env python3

import argparse
import re
from typing import List, Optional


def parse_arguments(arguments: Optional[List[str]] = None) -> argparse.Namespace:
    tastes = ["normalized", "lemmatized", "original", "transliterated"]
    parser = argparse.ArgumentParser(
        description="Process a file with tab-separated attributes."
    )
    parser.add_argument(
        "-t", "--taste", type=str, help="Taste to output", choices=tastes, required=True
    )
    parser.add_argument(
        "--replace",
        metavar="LEXICON",
        type=str,
        help="Replace words based on entries in LEXICON (tab-separated)",
    )
    parser.add_argument(
        "--remove-unwanted-spaces",
        help="Remove spaces between two capitalized words where the first one ends with a hypen ('Süd- Westen' -> 'Süd-Westen')",
        action="store_true",
    )
    parser.add_argument("file", type=str, help="File to process")

    return parser.parse_args(arguments)


def main(arguments: Optional[List[str]] = None) -> None:
    # (1) Read arguments
    args = parse_arguments(arguments)

    # (2) Load replacement lexicon
    #TODO

    # (3) Whether to remove unwanted spaces
    #TODO

    # (4) Do more
    columns = {}  # column tab index
    attrs = []  # tabs per line
    in_s = False  # within sentence (= not first token of sentence)
    with open(args.file, "r", encoding="utf8") as fh:
        for line in fh:
            line = line.strip()
            if line.startswith("%%$DDC:index["):
                match = re.split(" |=", line.strip())
                try:
                    i = int(re.search(r"\d+", match[0])[0])
                except:
                    raise Exception("Couldn't parse ddc-tabs input file correctly.")
                long = match[1]
                short = match[2]
                if long == "Token" or short == "w":
                    columns["transliterated"] = i
                elif long == "Utf8" or short == "u":
                    columns["original"] = i
                elif long == "CanonicalToken" or short == "v":
                    columns["normalized"] = i
                elif long == "Lemma" or short == "l":
                    columns["lemmatized"] = i
                elif long == "WordSept" or short == "ws":
                    columns["ws"] = i

            elif not line.startswith("%%") and line:
                attrs = line.split("\t")
                sep = "" if int(attrs[columns["ws"]]) == 0 or not in_s else " "
                token = attrs[columns[args.taste]]
                print(f"{sep}{token}", end="")
                in_s = True

            elif line.strip() == "":
                in_s = False
                print()

    return None


if __name__ == "__main__":
    main()
