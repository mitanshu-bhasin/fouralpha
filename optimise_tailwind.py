import os
import re

dir_path = r"d:\security-tools\Four Alpha"

# 1. Update script.js
script_path = os.path.join(dir_path, "script.js")
if os.path.exists(script_path):
    with open(script_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Remove tailwind.config=...;
    content = re.sub(r'tailwind\.config=\{.*?\}\}\};\s*', '', content, flags=re.DOTALL)
    
    with open(script_path, "w", encoding="utf-8") as f:
        f.write(content)

# 2. Update all HTML files
for root, dirs, files in os.walk(dir_path):
    for file in files:
        if file.endswith(".html"):
            file_path = os.path.join(root, file)
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
                
            match = re.search(r'<link[^>]*?href=[\'"]([^\'"]*?)styles\.css[\'"][^>]*>', content)
            prefix = match.group(1) if match else ""
            
            content = re.sub(r'<script\s+src=[\'"]https://cdn\.tailwindcss\.com[\'"][^>]*></script>\s*', '', content)
            
            new_link = f'<link rel="stylesheet" href="{prefix}tailwind-output.css">'
            
            if 'tailwind-output.css' not in content and match:
                content = content.replace(match.group(0), f'{new_link}\n{match.group(0)}')
                
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
                
print("Done!")
