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
        "--replace-tokens",
        metavar="LEXICON",
        type=str,
        help="Replace words based on entries in LEXICON (tab-separated)",
    )
    parser.add_argument(
        "--replace-underscores",
        help="Replace intra-word underscores by spaces ('musst_du' -> 'musst du')",
        action="store_true",
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
    repl_lex = {}
    if args.replace_tokens:
        with open(args.replace_tokens, "r", encoding="utf-8") as fh:
            lines = fh.readlines()
            repl_lex = dict([tuple(line.strip().split("\t")) for line in lines])

    # (3) Whether to remove unwanted spaces
    if args.remove_unwanted_spaces:
        prev_token = ""

    # (4) Do more
    columns = {}  # column tab index
    attrs = []  # tabs per line
    in_s = False  # within sentence (= not first token of sentence)
    with open(args.file, "r", encoding="utf8") as fh:
        for line in fh:
            line = line.strip()

            # Metadata line
            if line.startswith("%%$DDC:index["):
                match = re.split(" |=", line.strip())
                try:
                    i = int(re.search(r"\d+", match[0])[0])
                except ValueError as e:
                    raise ValueError(
                        "Couldn't parse ddc-tabs input file correctly."
                    ) from e
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

            # Token line
            elif not line.startswith("%%") and line:
                attrs = line.split("\t")
                sep = "" if int(attrs[columns["ws"]]) == 0 or not in_s else " "
                token = attrs[columns[args.taste]]

                # Optional: overwrite the token with replacement from lexicon
                if args.replace_tokens:
                    token = repl_lex.get(token, token)

                # Optional: replace intra-word underscores by spaces
                if args.replace_underscores:
                    token = re.sub(r"(\w)_(\w)", r"\1 \2", token)

                # Optional: Remove the seperator if the following condition is met
                # previous token is capitalized AND ends with "-" AND current token is capitalized
                if args.remove_unwanted_spaces:
                    if (
                        (prev_token)
                        and (prev_token[-1] == "-")
                        and prev_token[0].isupper()
                        and token[0].isupper()
                    ):
                        sep = ""

                print(f"{sep}{token}", end="")
                in_s = True
                prev_token = token

            # Empty line
            elif line.strip() == "":
                in_s = False
                prev_token = ""
                print()

    return None


if __name__ == "__main__":
    main()
