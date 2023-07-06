import os
from PIL import Image

os.chdir('website/static/assets/product_images/')
for d in os.scandir('./'):
    image = Image.open(d.name)

    width, height = image.size
    new_width = int(width * 0.125)
    new_height = int(height * 0.125)

    resized_image = image.resize((new_width, new_height))

    
    resized_image.save(f'thumb-{d.name}')
