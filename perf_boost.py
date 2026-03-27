import os
import re

def boost_performance(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Fix Google Fonts display=swap
    new_content = re.sub(r'family=([^"\'&]+)', r'family=\1&display=swap', content)
    # Avoid duplicate display=swap
    new_content = new_content.replace('&display=swap&display=swap', '&display=swap')

    # 2. Add aria-label to mobile menu button if not present
    if 'id="mobile-menu-button"' in new_content and 'aria-label' not in new_content.split('id="mobile-menu-button"')[1].split('>')[0]:
        new_content = new_content.replace('id="mobile-menu-button"', 'id="mobile-menu-button" aria-label="Toggle Navigation" aria-expanded="false"')

    # 3. Add rel="preconnect" for Google Fonts for faster loading
    if 'fonts.googleapis.com' in new_content and 'preconnect' not in new_content:
        preconnect = '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
        new_content = new_content.replace('<head>', '<head>' + preconnect)

    # 4. Fix images without dimensions (LCP/CLS boost)
    # Using a simple pattern for standard images we know
    new_content = new_content.replace('src="logo.jpeg"', 'src="logo.jpeg" width="40" height="40"')
    new_content = new_content.replace('src="ipec.jpg"', 'src="ipec.jpg" width="40" height="40"')
    # Clean up double attributes if they exist
    new_content = re.sub(r'width="\d+" width="(\d+)"', r'width="\1"', new_content)
    new_content = re.sub(r'height="\d+" height="(\d+)"', r'height="\1"', new_content)

    if new_content != content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True
    return False

def main():
    count = 0
    for root, dirs, files in os.walk('.'):
        if 'node_modules' in root or '.git' in root:
            continue
        for file in files:
            if file.endswith('.html'):
                file_path = os.path.join(root, file)
                if boost_performance(file_path):
                    count += 1
                    print(f"Boosted {file_path}")
    print(f"Total files boosted: {count}")

if __name__ == "__main__":
    main()
