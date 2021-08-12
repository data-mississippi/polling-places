import sys
from pdf2image import convert_from_path

infile = sys.argv[1]
outstem = sys.argv[2]

images = convert_from_path(infile, dpi=300, grayscale=True)

for index, image in enumerate(images):
    print(outstem)
    path = f'{outstem}_{index}.jpg'
    image.save(path, 'JPEG')
