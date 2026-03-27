import os
import re

def fix_img_tag(tag, src_name, target_w, target_h):
    # Remove any existing width/height
    tag = re.sub(r'\s+\bwidth="[^"]*"', '', tag)
    tag = re.sub(r'\s+\bheight="[^"]*"', '', tag)
    # Add them back correctly after src
    tag = re.sub(r'(src="' + re.escape(src_name) + r'")', r'\1 width="' + str(target_w) + r'" height="' + str(target_h) + r'"', tag)
    return tag

def fix_footer_images(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    new_content = content
    
    # Find all img tags with ipec.jpg or logo.jpeg
    img_tags = re.findall(r'<img[^>]+src="(?:ipec\.jpg|logo\.jpeg)"[^>]*>', new_content, re.IGNORECASE | re.DOTALL)
    
    for tag in img_tags:
        fixed_tag = tag
        if 'ipec.jpg' in tag.lower():
            fixed_tag = fix_img_tag(tag, 'ipec.jpg', 70, 40)
        elif 'logo.jpeg' in tag.lower():
            fixed_tag = fix_img_tag(tag, 'logo.jpeg', 40, 40)
        
        if fixed_tag != tag:
            # Escape the original tag for regex replacement
            # Tag might have newlines, so we use DOTALL
            new_content = new_content.replace(tag, fixed_tag)

    if new_content != content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True
    return False

# List all HTML files
html_files = []
for root, dirs, files in os.walk('.'):
    for file in files:
        if file.endswith('.html'):
            html_files.append(os.path.join(root, file))

modified_count = 0
for file_path in html_files:
    if fix_footer_images(file_path):
        print(f"Fixed: {file_path}")
        modified_count += 1

print(f"Total files modified: {modified_count}")
