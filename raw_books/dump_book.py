# Need this first to setup Django environment
# Source: https://stackoverflow.com/a/26875729
import os
import sys
import django
import json

sys.path.append("../")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "collaboread.settings")

django.setup()

from core.models import Article


def get_book_json(uuid):
    """Get book from MP_Node object and return as JSON"""
    try:
        book = Article.objects.get(uuid=uuid)
        book_raw = Article.dump_bulk(book)

        # Need default=str to convert datetime
        # Source: https://stackoverflow.com/a/36142844
        return json.dumps(book_raw, default=str)
    except:
        print("Book with uuid '{}' does not exist".format(uuid))
        return ""


def main():
    """Main function"""
    uuid = input("Enter uuid of book to dump: ")
    book_json = get_book_json(uuid)
    if book_json:
        filename = input("Enter name of file to output: ")
        # Use with to automatically close file after finishing
        # Source: https://stackoverflow.com/q/9282967
        with open(filename, "w") as output_file:
            output_file.write(book_json)


main()
