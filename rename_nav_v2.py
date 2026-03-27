import os
import re

root = '.'
for dirpath, dirnames, filenames in os.walk(root):
    for filename in [f for f in filenames if f.endswith('.html')]:
        filepath = os.path.join(dirpath, filename)
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            
            # 1. Navbar and Mobile menu (robust match)
            content = re.sub(r'Education\s+Policy\s*<i', 'Policy & Governance <i', content)
            
            # 2. Page titles (specifically for education-policy pages)
            content = re.sub(r'>Education Policy - Education Policy', '>Policy & Governance', content)
            
            # 3. Footer link text (look for the link to policy-governance.html)
            content = re.sub(r'href="(\.\./)?policy-governance\.html"([^>]*?)>Policy</a>', r'href="\1policy-governance.html"\2>Policy & Governance</a>', content)

            if content != original_content:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"Updated {filepath}")
        except Exception as e:
            print(f"Error processing {filepath}: {e}")
