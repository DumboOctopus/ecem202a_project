import os
from os import path
import csv



if __name__ == '__main__':
    folder_of_images = 'origin_dataset'
    files = os.listdir(folder_of_images)

    with open(f'image-sizes-{folder_of_images}.csv', 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for image in files:

            # putting it into memory to make testing set up exactly the same
            # as robot code
            buf = None
            with open(path.join(folder_of_images, image), 'rb') as fh:
                size = len(fh.read())

            csv_writer.writerow([
                image,
                size 
            ])
