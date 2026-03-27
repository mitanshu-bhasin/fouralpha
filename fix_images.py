import os
import re

dir_path = r'd:\security-tools\Four Alpha'
for root, dirs, files in os.walk(dir_path):
    for file in files:
        if file.endswith('.html'):
            filepath = os.path.join(root, file)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Add width and height to ipec.jpg if missing
            content = re.sub(r'(<img[^>]*src=[\'\"](?:[^\'\"]*?)ipec\.jpg[\'\"][^>]*)>', lambda m: m.group(1) + ' width=\"40\" height=\"40\">' if 'width=' not in m.group(1) else m.group(0), content)
            
            # Add width and height to logo.jpeg if missing
            content = re.sub(r'(<img[^>]*src=[\'\"](?:[^\'\"]*?)logo\.jpeg[\'\"][^>]*)>', lambda m: m.group(1) + ' width=\"40\" height=\"40\">' if 'width=' not in m.group(1) else m.group(0), content)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
print('Images dimensions added')
