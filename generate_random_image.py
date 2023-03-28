import os
import random
from PIL import Image

def random_pastel_color():
    return tuple(random.randint(128, 255) for _ in range(3))

def generate_random_image(size, color):
    img = Image.new('RGB', size, color)
    return img

def main():
    image_count = 30
    output_dir = 'images3'

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for i in range(image_count):
        width = random.randint(200, 1000)
        height = random.randint(200, 1000)
        pastel_color = random_pastel_color()
        img = generate_random_image((width, height), pastel_color)
        img.save(f"{output_dir}/{i+1:03d}.jpg")

if __name__ == '__main__':
    main()
