import logging
from tkinter import *
import tkinter.messagebox
import os
from pathlib import Path
import sys
import argparse

import barcode
from barcode.writer import ImageWriter
from PIL import Image, ImageDraw, ImageFont

logging.basicConfig(
    filename="generate_isbn13.log",
    level=logging.INFO,
    filemode="w",
    datefmt="%m/%d/%Y %I:%M:%S %p",
    format="%(levelname)s - %(asctime)s: %(message)s",
)

def setup_check():
    try:
        logging.info("Checking install path.")
        app_data = Path(os.getenv("APPDATA"))
        install_location = app_data.parent.joinpath("Local", "generate_isbn13")
        if install_location.exists() == False:
            os.makedirs(install_location,exist_ok=True)
            logging.info("New install location created.")
            sys.exit()
        logging.info("Install path has existed previously.")
        return install_location
    except Exception as e:
        logging.error("Failed to check the install location.")
        logging.debug(e)
        
def clean_isbn_number(user_input):
    try:
        logging.info("Cleaning user input.")
        cleaned_number = user_input.strip().replace("-","").replace(" ","").replace(".","")
        if int(cleaned_number) and len(cleaned_number) == 13:
            return cleaned_number
            #generate_barcode(validated_num=cleaned_number)
        else:
            logging.error(f"The ISBN13 # was not 13 digits long or contained a character other than a number.")
            raise
    except Exception as e:
        error = logging.error("Failed to clean user input.")
        logging.error("Entry might have been empty.")
        logging.debug(e)
        tkinter.messagebox.showinfo("Error!", "Entry might have been empty.\nFailed to clean user input.")
        exit()

def generate_barcode(validated_num, dpi=600, output_file_format="png"):
    """Generates & formats ISBN barcode .png from the given ISBN#"""
    try:
        logging.info("Setting file name.")
        file_name = f"{validated_num}_barcode"
        file_format = output_file_format
        file_name_with_ext = f"{file_name}.{file_format}"
        desktop = Path(os.getenv("USERPROFILE")).joinpath("Desktop")
        final_file_location = desktop.joinpath(file_name_with_ext)
    except Exception as e:
        logging.error("Failed to set filename.")
        logging.debug(e)
        exit()

    try:
        logging.info("Generating barcode.")
        ISBN13 = barcode.get_barcode_class("ISBN13")
        image_file = ISBN13(validated_num, writer=ImageWriter())

        writer_options = {
            "module_width": 0.9, #0.2
            "module_height":45 , #15
            "quiet_zone": 10, #5
            # "font_path": "",
            # "font_size": 10,#10
            # "text_distance":20,#5
            # "background":"#44ff33",
            # "foreground": "#44ff33",
            "write_text": False,
            "center_text": True,
            "format": file_format.upper(),
            "margin_top":6,#10
            "margin_bottom": 8,
        }
        image_file.save(desktop.joinpath(file_name), options=writer_options)
    except Exception as e:
        logging.error("Failed to generated barcode.")
        logging.debug(e)
        exit()

    try:
        logging.info("Slicing string into three fields.")
        image_text = str(image_file)
        first_num = image_text[0]
        second_nums = image_text[1:7]
        third_nums = image_text[7:]
    except Exception as e:
        logging.error("Failed to slice string.")
        logging.debug(e)
        exit()

    try:
        logging.info("Editing image to format text fields.")
        # Uses Pillow to open the file.
        img_edit = Image.open(final_file_location)
        draw = ImageDraw.Draw(img_edit)

        # Sets base locations and fonts.
        logging.info("Setting the font type and size.")
        use_font = ImageFont.truetype(font="arial.ttf", size=42*3)
        print(img_edit.size)
        #position = (100, 536)
        position = (img_edit.size[0]//12, img_edit.size[1]*.78)
        left, top, right, bottom = draw.textbbox((position), text=image_text, font=use_font)
        print(f"position: {position}")
        print(f"left: {left}")
        print(f"top: {top}")
        print(f"right: {right}")
        print(f"bottom: {bottom}")


        # Draws first number to image.
        logging.info("Drawing first digit to the image.")
        draw.text((25,position[1]), text=first_num, font=use_font, fill="black")

        # Draws number 2-6 and the white space to the image.
        logging.info("Drawing numbers 2-6 and the white space to the image.")
        draw.rectangle((left+55, top-15, left+480, bottom+10), fill="white")
        draw.text((left+60, top-30), text=second_nums, font=use_font, fill="black")

        # Draws number 7-13 and the white space to the image.
        logging.info("Drawing numbers 7-13 and the white space to the image.")
        draw.rectangle((left+545, top-15, left+980, bottom+10), fill="white")
        draw.text((left+560, top-30), text=third_nums, font=use_font, fill="black")

        # Saves image at specific DPI.
        logging.info("Saving image at specific DPI.")
        img_edit.save(fp=final_file_location, dpi=(dpi,dpi))
        
        tkinter.messagebox.showinfo("New barcode generated!", f"Check your desktop for the barcode's PNG image.\n File Name:'{file_name_with_ext}'")
                
    except Exception as e:
        logging.error("Failed to format barcode image output.")
        logging.debug(e)
        tkinter.messagebox.showinfo("Error!", f"Failed to format barcode image output.")
        exit()

def start_gui():
    icon = setup_check()
    root = Tk()
    root.title("ISBN Barcode Generator")
    x_screen_center = root.winfo_screenwidth() // 2
    y_screen_center = root.winfo_screenheight() // 2
    x_window = 400
    y_window = 200
    root.configure(background="#dfdfdf")
    root.geometry(f"{x_window}x{y_window}+{x_screen_center}+{y_screen_center}")
    root.resizable(0,0)
    try:
        root.iconbitmap(f"{icon}\\icon.ico")
    except:
        logging.error("No icon image available.")

    isbn_instructions = Label(root, text="Please enter ISBN13 #:", font=("Arial", 20), background="#dfdfdf")
    isbn_num_input = Entry(root, font=("Arial", 20))
    isbn_submit_button = Button(
        root,text="Generate Barcode",
        font=("Arial", 20),
        relief="ridge",
        borderwidth=5,
        command=lambda:generate_barcode(clean_isbn_number(user_input=isbn_num_input.get()),
        ))

    isbn_instructions.grid(row=0, column=1, padx=x_window//7, pady=(20,0))
    isbn_num_input.grid(row=1, column=1, padx=x_window//45, pady=10)
    isbn_submit_button.grid(row=2, column=1, pady=10)
    root.mainloop()

def cli_only(isbn, ext, dpi):
    logging.info("Starting in 'command line only' mode.")
    return generate_barcode(validated_num=clean_isbn_number(isbn), dpi=dpi, output_file_format=ext)
    

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-g", "--gui", type=int, choices=[0,1], default=1, help="Turn GUI On (1 default) or Off (0).")
    parser.add_argument("-i", "--isbn", help="Specifies the ISBN13 number to use.")
    parser.add_argument("-d", "--dpi", type=int, choices=[300, 400, 600, 800, 1200], default=600, help="Specifies DPI of image output.")
    parser.add_argument("-f", "--file-format", choices=["png", "jpeg"], default="png", help="File output format i.e. png, jpeg.")

    args = parser.parse_args()
    print(args)
    if args.gui:
        start_gui()
    elif not args.gui:
        cli_only(isbn=args.isbn, ext=args.file_format, dpi=args.dpi)

    

    logging.info("Script completed.")

if __name__ == "__main__":
    main()