# generate_isbn_barcode_image

This project takes an ISBN13 number as user input and generates a scannable ISBN13 barcode image.

This can be run as a CLI tool or GUI by default.

If run as GUI, window appears displaying an input field and a "Generate Barcode" submit button.  Once the user puts the ISBN13 number in and clicks "Generate Barcode" a ".png" image is created and saved to the user's desktop.  The barcode can be scanned with a hand scanner, like the kind that you would see in a library.

While there is input validation, it is pretty simple as it only removes dashes, spaces, periods, and checks the overall length of the user input.  If validation fails, a popup appears informing the user that there was an issue with their input.

Every time the script runs, there is a corresponding log file located in the same directory as where the script was executed from.  The log file is overwritten with a new log file each time the script executes; meaning that the log file will only show output from the last time the script was run and not from other times prior.

## Options

  -h, --help            show this help message and exit
  -g {0,1}, --gui {0,1}
                        Turn GUI On (1 default) or Off (0).
  -i ISBN, --isbn ISBN  Specifies the ISBN13 number to use.
  -d {300,400,600,800,1200}, --dpi {300,400,600,800,1200}
                        Specifies DPI of image output.
  -f {png,jpeg}, --file-format {png,jpeg}
                        File output format i.e. png, jpeg.

### python-barcode

This script is built only for ISBN13 numbers, but can be modified using the "python-barcode" library to accept other standards.  I left some of the optional barcode writer options, with its default values, in the scripts as comments which can be uncommented and tweaked to edit the output of the barcode itself.  python-barcode documention: https://python-barcode.readthedocs.io/en/stable/

### PIL

The placement of the final number and the whitespaces at the bottom are defined by PIL.  Adjusting the coordinates.  PIL docutmentation: https://pillow.readthedocs.io/en/stable/
