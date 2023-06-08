# Need this first to setup Django environment
# Source: https://stackoverflow.com/a/26875729
import os
import sys
import django
import json

# Need this first line since we're in a subdirectory
sys.path.append("../")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "collaboread.settings")

django.setup()

from core.models import Article


def extract_book(filename):
    try:
        with open(filename, "r") as input_file:
            book_json = input_file.read()
            book_raw = json.loads(book_json)
            return book_raw
    except:
        print("File '{}' does not exist".format(filename))
        return ""


def main():
    """Main function"""
    filename = input("Enter name of file to input: ")
    book_raw = extract_book(filename)
    if book_raw:
        Article.load_bulk(book_raw)


main()
