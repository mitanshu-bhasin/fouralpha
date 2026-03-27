from PIL import Image
import os

images = ['ipec.jpg', 'logo.jpeg']
for img_path in images:
    if os.path.exists(img_path):
        with Image.open(img_path) as img:
            print(f"{img_path}: {img.width}x{img.height}")
    else:
        print(f"{img_path} not found")
