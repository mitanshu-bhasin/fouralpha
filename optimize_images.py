import os
from PIL import Image

def optimize_images():
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                file_path = os.path.join(root, file)
                size_kb = os.path.getsize(file_path) / 1024
                
                if size_kb > 100: # Threshold for optimization
                    print(f"Optimizing {file_path} ({size_kb:.1f} KB)...")
                    try:
                        img = Image.open(file_path)
                        # Save as webp
                        webp_path = os.path.splitext(file_path)[0] + '.webp'
                        img.save(webp_path, 'WEBP', quality=80)
                        print(f"  Created {webp_path}")
                    except Exception as e:
                        print(f"  Error optimizing {file_path}: {e}")

if __name__ == "__main__":
    optimize_images()
