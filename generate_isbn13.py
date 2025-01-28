import barcode
from barcode.writer import ImageWriter
from PIL import Image, ImageDraw, ImageFont

def clean_isbn_number(isbn):
    cleaned_number = isbn.replace("-","").replace(" ","").replace(".","")
    return cleaned_number

def generate_barcode(isbn):
    file_name = f"{isbn}_barcode"
    file_format = "png"
    file_name_with_ext = f"{file_name}.{file_format}"

    # ISBN13 = barcode.isxn.InternationalStandardBookNumber13()

    ISBN13 = barcode.get_barcode_class("ISBN13")
    image_file = ISBN13(isbn, writer=ImageWriter())

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

    image_text = str(image_file)
    first_num = image_text[0]
    second_nums = image_text[1:7]
    third_nums = image_text[7:]

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

    # Saves image.
    img_edit.save(fp=file_name_with_ext, dpi=(600,600))

def main():
    isbn_num_input = input(f"What 'ISBN' number will we be using?  ")
    cleaned_isbn = clean_isbn_number(isbn=isbn_num_input)
    generate_barcode(isbn=cleaned_isbn)

if __name__ == "__main__":
    main()