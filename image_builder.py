# Importing the PIL library
from re import T
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from io import BytesIO
import requests

# Split text into lines based on image width
def split_text(text, max_width, font, draw_method):
    lines = []
    line = ""
    for word in text.split(" "):
        if draw_method.textsize(line + word, font=font)[0] < max_width:
            line += word + " "
        else:
            lines.append(line)
            line = word + " "
    lines.append(line)
    splitted_text = "\n".join(lines)
    return splitted_text

def social_image_builder(url, category, title, logo, branding_text, font_size=60, border=40, height=1080, width=1080, color='000000'):
    # Convert hex color to RGBA
    color = tuple(int(color[i:i+2], 16) for i in (0, 2 ,4))
    # Open an Image that will be on the background of the final image
    file = BytesIO(requests.get(url, stream=True).raw.read())
    img = Image.open(file)
    # Convert image to keep transparency
    img = img.convert('RGBA')
    # If image is horizontal we fit to desired height
    if img.size[0] > img.size[1]:
        # Resize image to fit height but keep aspect ratio
        img = img.resize((int(img.size[0] * height / img.size[1]), height), Image.ANTIALIAS)
        # Crop image to fit width centered and keep aspect ratio
        img = img.crop(((img.size[0] - width) / 2, 0, (img.size[0] + width) / 2, height))
    # If image is vertical we fit to desired width
    else:
        # Resize image to fit width but keep aspect ratio
        img = img.resize((width, int(img.size[1] * width / img.size[0])), Image.ANTIALIAS)
        # Crop image to fit height centered and keep aspect ratio
        img = img.crop((0, (img.size[1] - height) / 2, width, (img.size[1] + height) / 2))
    # find image height and width
    image_height = img.size[1]
    image_width = img.size[0]

    # Create a new image that will receive the text and the elements
    new_image = Image.new('RGBA', (image_width, image_height), (255, 255, 255, 0))

    # Call draw Method to add 2D graphics in an image
    I1 = ImageDraw.Draw(new_image, "RGBA")

    # We set all variable and resize everything we need first
    # Resize the logo image
    logo_size = 30
    if logo != '':
        try:
            logo_img = BytesIO(requests.get(logo, stream=True).raw.read())
            logo_img = Image.open(logo_img)
            logo_img = logo_img.convert('RGBA')
            logo_img = logo_img.resize((int(logo_size), int(logo_size)))
        except:
            # Logo image will be a white square with the same size of the logo_size
            logo_img = Image.new('RGBA', (logo_size, logo_size), (255, 255, 255, 0))
    else:
        logo_img = Image.new('RGBA', (logo_size, logo_size), (255, 255, 255, 255))
    # Setting category font and style
    category_font = ImageFont.truetype('fonts/Roboto-Bold.ttf', (font_size//2) )
    category_text_width, category_text_height = I1.textsize(category, font=category_font)
    category_text_width, category_text_height = I1.textsize(category, font=category_font)
    font_branding_text = ImageFont.truetype('fonts/Roboto-Medium.ttf', logo_size)
    font_branding_text_width, font_branding_text_height = I1.textsize(branding_text, font=font_branding_text)
    # Setting title font and style
    font_title = ImageFont.truetype('fonts/Roboto-Bold.ttf', font_size)
    # Split text into a specified number of lines
    title = split_text(title, (image_width - border * 2), font_title, I1)
    # Call textsize method to find the size of the title text
    title_width, title_height = I1.textsize(title, font=font_title)
    
    # Add background color gradient to the image to make title stand out
    rectangle_height_y_position = image_height - title_height - logo_size - border - 80
    transparency = 0
    while rectangle_height_y_position < image_height:
        I1.rectangle(((0, rectangle_height_y_position), (image_width, rectangle_height_y_position)), fill=(0, 0, 0, transparency))
        rectangle_height_y_position += 1
        if transparency < 180: 
            transparency += 1
    
    if category != '':
        # Category text first
        # Draw a rectangle around the text with shadow
        I1.rectangle(((border, border+1), (category_text_width + border + 10, category_text_height + border + 5)), fill=(0, 0, 0, 255))
        I1.rectangle(((border, border+2), (category_text_width + border + 10, category_text_height + border + 5)), fill=(120, 120, 120, 255))
        I1.rectangle(((border, border), (category_text_width + border + 15, category_text_height + border + 5)), fill=(255, 255, 255, 255))
        # Draw a rectangle before the text for decoration
        I1.rectangle(((border + 5, border + 5), (border - 5, category_text_height + border)), fill=(0, 0, 0, 120))
        # Add Text to an image
        I1.text((border + 10, border - 2), category, font=category_font, fill =(0, 0, 0, 255))
    
    # Now adding title text
    # Add text shadow
    I1.text((border-1, image_height-title_height-border+1), title, font=font_title, fill=(0, 0, 0,125))
    I1.text((border-2, image_height-title_height-border+2), title, font=font_title, fill=(0, 0, 0,190))
    I1.text((border-3, image_height-title_height-border+3), title, font=font_title, fill=(0, 0, 0,255))
    # Add text to the image
    I1.text((border, image_height-title_height-border), title, font=font_title, fill =(255, 255, 255))
    # Now adding branding text and logo image
    # Add logo to the image
    new_image.paste(logo_img, (border, image_height - title_height - border - logo_size), logo_img)
    # Adding decorative rectangle after logo
    I1.rectangle(((border + logo_size + 12, image_height - title_height - border - logo_size) , (border + logo_size  + 17, image_height - title_height - border)), fill=(255, 255, 255))
    # Adding branding text, it will be either website name or instagram username
    I1.text((border+logo_size+24, image_height-title_height - border - font_branding_text_height -4), branding_text, font=font_branding_text, fill =(0, 0, 0))
    I1.text((border+logo_size+25, image_height-title_height - border - font_branding_text_height -5), branding_text, font=font_branding_text, fill =(255, 255, 255))
    
    # Alpha composite these two images together to obtain the desired result.
    img = Image.alpha_composite(img, new_image)

    return img