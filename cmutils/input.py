# functions to manage user input
import csv
from typing import Tuple

from .exceptions import CmException

def validate_input(input_value: str) -> str:
    domain = "https://www.cardmarket.com"
    if input_value.startswith(domain):
        return input_value.replace(domain, "")
    raise CmException(f"{input_value} is an invalid url. The url must start with https://www.cardmarket.com")

def get_html_filename() -> str:
    input_filename = input(
        "Define html filename [enter for default (index.html); existing files will be overwritten]: ")
    return input_filename if input_filename else "index.html"


def get_urls() -> list:
    try:
        cards_urls = []
        filename = input("Insert the csv filename: ")
        with open(filename, 'r') as csvfile:
            datareader = csv.reader(csvfile)
            # the csv input file contains only a row of comma separated urls
            # so the for loop runs only once
            for row in datareader:
                cards_urls = row
                break

        processed_urls = [validate_input(url) for url in cards_urls]
        return processed_urls

    except FileNotFoundError:
        raise CmException("The specified file was not found. Please check the file path and try again.")
    except csv.Error as e:
        raise CmException(f"CSV error: {e}")
    except Exception as e:
        raise CmException(f"An unexpected error occurred: {e}")

def get_user_input() -> Tuple[list, str]:
    urls = get_urls()
    html_filename = get_html_filename()
    return urls, html_filename

