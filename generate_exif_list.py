import piexif
import glob
from PIL import Image
import os

# Function to get EXIF data from an image file
def get_exif(file):
    img = Image.open(file)
    exif_dict = piexif.load(img.info['exif'])
    return exif_dict

# Specify the folder containing image files
folder = 'folder/images2/*.jpg'
files = glob.glob(folder)

# List of metadata to retrieve
metadata_location = ['Model', 'LensModel', 'ExposureTime', 'FNumber', 'ISOSpeedRatings', 'FocalLength', 'ApertureValue']

# List to store EXIF strings for each image
exif_str_list = []

# Iterate over image files
for file in files:
    exif_dict = get_exif(file)

    # Initialize variables to store metadata
    Model, LensModel, ExposureTime, FNumber, ISOSpeedRatings, FocalLength = "", "", "", "", "", ""

    # Iterate over EXIF tags
    for lfn in exif_dict:
        for tag in exif_dict[lfn]:
            try:
                metadata = piexif.TAGS[lfn][tag]["name"]
                if metadata in metadata_location:
                    tag = exif_dict[lfn][tag]

                    if metadata == 'Model':
                        Model = tag.decode()
                    elif metadata == 'LensModel':
                        LensModel = tag.decode()
                    elif metadata == 'ISOSpeedRatings':
                        ISOSpeedRatings = f'ISO {tag}'
                    elif metadata == 'ExposureTime':
                        ExposureTime = f'{tag[0]}/{tag[1]}s'
                    elif metadata == 'FNumber':
                        num, den = int(tag[0]), int(tag[1])
                        FNumber = f'F/{num/den if num % den != 0 else num//den}'
                    elif metadata == 'FocalLength':
                        num, den = int(tag[0]), int(tag[1])
                        FocalLength = f'{num//den}mm'
            except KeyError:
                pass

    # Combine metadata into a single string
    single_exif = f'{Model} + {LensModel} <br>{ExposureTime} {FNumber} {ISOSpeedRatings} @{FocalLength}'
    exif_str_list.append(single_exif)

# Save the list of EXIF strings to a file
save_file = os.path.join(os.path.dirname(files[0]), 'exif.txt')

# Write the EXIF strings to the file without brackets and single quotes
with open(save_file, 'w') as f:
    formatted_exif_str = ', '.join(exif_str_list)
    f.write(formatted_exif_str)

# Read the cleaned EXIF strings back from the file (optional)
with open(save_file, 'r') as f:
    cleaned_exif_str = f.read()

print("Cleaned EXIF strings:", cleaned_exif_str)