from PIL import Image
import os
from os import path

folder_of_images = 'images'
folder_of_resize = 'lanczos'
for image in os.listdir(folder_of_images):
   im = Image.open(path.join(folder_of_images, image))

   size = (256, 256)

   out = im.resize(size, resample=Image.LANCZOS)

   out.save(path.join(folder_of_resize, image))
