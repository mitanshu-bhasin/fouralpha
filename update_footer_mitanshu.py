import os
import re
import glob

def update_footer(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Pattern to find the copyright section
    # <span>&copy; 2026 Four Alpha AED Lab</span>
    copyright_pattern = r'(<span>&copy; 2026 Four Alpha AED Lab</span>)'
    
    # We want to add the developer credit after the copyright span.
    # We'll use a small font size as requested.
    developer_credit = ' <span class="hidden md:block text-white/5">|</span> <span class="text-[10px] text-gray-500 lowercase tracking-widest">Developed and Architected by <a href="https://mitanshubhasin.netlify.app/" target="_blank" class="text-gold/60 hover:text-gold transition-colors">Mitanshu Bhasin</a></span>'

    if re.search(copyright_pattern, content):
        # Check if already added to avoid duplicates
        if 'Mitanshu Bhasin' in content:
            return False
            
        new_content = re.sub(copyright_pattern, r'\1' + developer_credit, content)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True
    return False

html_files = glob.glob('**/*.html', recursive=True)
updated_count = 0
for file in html_files:
    if 'node_modules' in file or '.gemini' in file:
        continue
    if update_footer(file):
        updated_count += 1

print(f"Added developer credit to {updated_count} files.")
