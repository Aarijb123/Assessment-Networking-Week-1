"""A CLI application for interacting with the Postcode API."""

from argparse import ArgumentParser
from postcode_functions import validate_postcode, get_postcode_completions


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", '-m', required=True,
                        choices=["validate", "complete"])
    parser.add_argument("postcode", type=str)
    args = parser.parse_args()

    postcode = args.postcode.strip().upper()

    if args.mode == "validate":
        if validate_postcode(postcode):
            print(f"{postcode} is a valid postcode")
        else:
            print(f"{postcode} is not valid")


if __name__ == "__main__":
    pass
