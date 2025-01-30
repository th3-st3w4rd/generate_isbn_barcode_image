import logging
from tkinter import *

import barcode
from barcode.writer import ImageWriter
from PIL import Image, ImageDraw, ImageFont

logging.basicConfig(
    filename="generate_isbn13.log",
    level=logging.INFO,
    filemode="w",
    datefmt="%m/%d/%Y %I/%M/%S %p",
    format="%(levelname)s - %(asctime)s: %(message)s",
)

def clean_isbn_number(user_input):
    try:
        logging.info("Cleaning user input.")
        cleaned_number = user_input.replace("-","").replace(" ","").replace(".","")
        if int(cleaned_number) == False:
            raise
        generate_barcode(validated_num=cleaned_number)
        
        # return cleaned_number
    except Exception as e:
        logging.error("Failed to clean user input.")
        logging.debug(e)
        exit()


def generate_barcode(validated_num):
    """Generates & formats ISBN barcode .png from the given ISBN#"""
    try:
        logging.info("Setting file name.")
        file_name = f"{validated_num}_barcode"
        file_format = "png"
        file_name_with_ext = f"{file_name}.{file_format}"
    except Exception as e:
        logging.error("Failed to set filename.")
        logging.debug(e)
        exit()

    try:
        logging.info("Generating barcode.")
        ISBN13 = barcode.get_barcode_class("ISBN13")
        image_file = ISBN13(validated_num, writer=ImageWriter())

        writer_options = {
            # "module_width": 0.2, #0.2
            # "module_height":15 , #15
            "quiet_zone": 5, #5
            # "font_path": "",
            # "font_size": 10,#10
            # "text_distance":20,#5
            # "background":"#44ff33",
            # "foreground": "#44ff33",
            "write_text": False,
            "center_text": True,
            "format": "PNG",
            # "margin_top":10,
            "margin_bottom": 3,
        }
        image_file.save(file_name, options=writer_options)
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
        img_edit = Image.open(file_name_with_ext)
        draw = ImageDraw.Draw(img_edit)

        # Sets base locations and fonts.
        use_font = ImageFont.truetype(font="SansSerifCollection.ttf", size=42)
        position= (100, 138)
        left, top, right, bottom = draw.textbbox((position), text=image_text, font=use_font)

        # Draws first number to image.
        draw.text((25,position[1]), text=first_num, font=use_font, fill="black")

        # Draws number 2-6 and the white space to the image.
        draw.rectangle((left-30, top-5, 235, bottom+10), fill="white")
        draw.text((position[0]-20, position[1]), text=second_nums, font=use_font, fill="black")

        # Draws number 7-13 and the white space to the image.
        draw.rectangle((250, top-5, right, bottom+10), fill="white")
        draw.text((265, position[1]), text=third_nums, font=use_font, fill="black")

        # Saves image at specific DPI.
        img_edit.save(fp=file_name_with_ext, dpi=(600,600))
    except Exception as e:
        logging.error("Failed to format barcode image output.")
        logging.debug(e)
        exit()



def main():
    root = Tk()
    root.title("ISBN Barcode Generator")
    x_screen_center = root.winfo_screenwidth() // 2
    y_screen_center = root.winfo_screenheight() // 2
    x_window = 400
    y_window = 200

    root.geometry(f"{x_window}x{y_window}+{x_screen_center}+{y_screen_center}")

    isbn_instructions = Label(root, text="Please enter ISBN #:", font=("Arial", 20))#, width=x_window//2)
    isbn_num_input = Entry(root, font=("Arial", 20))
    isbn_submit_button = Button(
        root,text="Generate Barcode",
        font=("Arial", 20),
        command=lambda:clean_isbn_number(user_input=isbn_num_input.get(),
        ))
    isbn_instructions.grid(row=0, column=1, padx=x_window//5.3, pady=(20,0))
    isbn_num_input.grid(row=1, column=1, padx=x_window//40)
    isbn_submit_button.grid(row=2, column=1, pady=10)
    root.mainloop()

    logging.info("Script completed.")

if __name__ == "__main__":
    main()