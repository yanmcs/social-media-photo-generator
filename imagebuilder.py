# Importing the PIL library
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import requests

def social_image_builder(image, category, title, logo, branding_text, border=40):

    # Split text into lines based on image width
    def split_text(text, max_width, font):
        lines = []
        line = ""
        for word in text.split(" "):
            if I1.textsize(line + word, font=font)[0] < max_width:
                line += word + " "
            else:
                lines.append(line)
                line = word + " "
        lines.append(line)
        splitted_text = "\n".join(lines)
        return splitted_text
    # Open an Image that will be on the background of the final image
    background_img = Image.open(requests.get(image, stream=True).raw)
    # Resize image based on height
    img = background_img.resize((1080, 1080), Image.ANTIALIAS)    

    # find image height and width
    image_height = img.size[1]
    image_width = img.size[0]

    # Call draw Method to add 2D graphics in an image
    I1 = ImageDraw.Draw(img, "RGBA")

    # We set all variable and resize everything we need first
    # Resize the logo image
    logo_size = 30
    logo_img = Image.open(requests.get(logo, stream=True).raw)
    logo_img = logo_img.resize((int(logo_size), int(logo_size)))
    print(logo_img.mode)
    # Setting category font and style
    category_font = ImageFont.truetype('fonts/Roboto-Bold.ttf', 30)
    category_text_width, category_text_height = I1.textsize(category, font=category_font)
    category_text_width, category_text_height = I1.textsize(category, font=category_font)
    font_branding_text = ImageFont.truetype('fonts/Roboto-Medium.ttf', logo_size)
    font_branding_text_width, font_branding_text_height = I1.textsize(branding_text, font=font_branding_text)
    # Setting title font and style
    font_title = ImageFont.truetype('fonts/Roboto-Bold.ttf', 60)
    # Split text into a specified number of lines
    title = split_text(title, (image_width - border * 2), font_title)
    # Call textsize method to find the size of the title text
    title_width, title_height = I1.textsize(title, font=font_title)

    # Add background color gradient to the image to make title stand out
    rectangle_height_x_position = image_height - title_height - logo_size - border - 50
    transparency = 0
    while rectangle_height_x_position < image_height:
        I1.rectangle(((0, rectangle_height_x_position), (image_width, rectangle_height_x_position)), fill=(0, 0, 0, transparency))
        rectangle_height_x_position += 1
        if transparency < 125:
            transparency += 1
    
    if category != '':
        # Category text first
        # Draw a rectangle around the text with shadow
        I1.rectangle(((border, border+1), (category_text_width + border + 10, category_text_height + border + 5)), fill=(0, 0, 0))
        I1.rectangle(((border, border+2), (category_text_width + border + 10, category_text_height + border + 5)), fill=(120, 120, 120))
        I1.rectangle(((border, border), (category_text_width + border + 15, category_text_height + border + 5)), fill=(255, 255, 255))
        # Draw a rectangle before the text for decoration
        I1.rectangle(((border + 5, border + 5), (border - 5, category_text_height + border)), fill=(0, 0, 0, 120))
        # Add Text to an image
        I1.text((border + 10, border - 2), category, font=category_font, fill =(0, 0, 0))
    
    # Now adding title text
    # Add text shadow
    I1.text((border-1, image_height-title_height-border+1), title, font=font_title, fill=(0, 0, 0,125))
    I1.text((border-2, image_height-title_height-border+2), title, font=font_title, fill=(0, 0, 0,190))
    I1.text((border-3, image_height-title_height-border+3), title, font=font_title, fill=(0, 0, 0,255))
    # Add text to the image
    I1.text((border, image_height-title_height-border), title, font=font_title, fill =(255, 255, 255))
    
    # Now adding branding text and logo image
    # Add logo to the image
    img.paste(logo_img, (border, image_height - title_height - border - logo_size), logo_img)
    # Adding decorative rectangle after logo
    I1.rectangle(((border + logo_size + 12, image_height - title_height - border - logo_size) , (border + logo_size  + 17, image_height - title_height - border)), fill=(255, 255, 255))
    # Adding branding text, it will be either website name or instagram username
    I1.text((border+logo_size+24, image_height-title_height - border - font_branding_text_height -4), branding_text, font=font_branding_text, fill =(0, 0, 0))
    I1.text((border+logo_size+25, image_height-title_height - border - font_branding_text_height -5), branding_text, font=font_branding_text, fill =(255, 255, 255))
    
    return img