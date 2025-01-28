# generate_isbn_barcode_image

Command line utility.  Asks for ISBN13 number of a book, generates a barcodes, and returns a scannable ".png" image.

## python-barcode

This script is built only for ISBN13 numbers, but can be modified using the "python-barcode" library to accept other standards.

python-barcode documention: https://python-barcode.readthedocs.io/en/stable/

## PIL

PIL docutmentation: https://pillow.readthedocs.io/en/stable/

The placement of the final number and the whitespaces at the bottom are defined by PIL.  Adjusting the coordinates.
