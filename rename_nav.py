import os
import re

root = '.'
for dirpath, dirnames, filenames in os.walk(root):
    for filename in [f for f in filenames if f.endswith('.html')]:
        filepath = os.path.join(dirpath, filename)
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Pattern for navbar label replacement
            # Matches "Education Policy" followed by optional whitespace and then the <i> tag
            new_content = re.sub(r'Education\s+Policy\s*<i', 'Policy & Governance <i', content)
            
            if content != new_content:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f"Updated {filepath}")
        except Exception as e:
            print(f"Error processing {filepath}: {e}")
