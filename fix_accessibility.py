import os
import re

def fix_accessibility(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    new_content = content
    
    # 1. Add <main> landmark if missing
    if '<main' not in new_content and '<body' in new_content:
        # Wrap the content between navigation and footer in <main>
        # Looking for <nav>...</nav> or similar
        body_start = new_content.find('<body')
        body_tag_end = new_content.find('>', body_start) + 1
        
        # Try to find nav or header end
        nav_end = new_content.find('</nav>', body_tag_end)
        if nav_end != -1:
            nav_end += 6
            # Find footer start
            footer_start = new_content.find('<footer', nav_end)
            if footer_start != -1:
                # Wrap
                new_content = (new_content[:nav_end] + 
                              '<main id="main-content">' + 
                              new_content[nav_end:footer_start] + 
                              '</main>' + 
                              new_content[footer_start:])
        elif body_tag_end != -1:
             # Basic wrap if no nav
             footer_start = new_content.find('<footer', body_tag_end)
             if footer_start != -1:
                 new_content = (new_content[:body_tag_end] + 
                               '<main id="main-content">' + 
                               new_content[body_tag_end:footer_start] + 
                               '</main>' + 
                               new_content[footer_start:])

    # 2. Add aria-labels to buttons and links with icons (Social Icons)
    # Pattern for social links: <a href="..." ...><i class="fab fa-facebook-f"></i></a>
    social_patterns = [
        ('facebook', 'Follow us on Facebook'),
        ('x-twitter', 'Follow us on X'),
        ('instagram', 'Follow us on Instagram'),
        ('linkedin', 'Follow us on LinkedIn'),
        ('compass', 'Home'),
        ('bars', 'Open Menu'),
        ('times', 'Close Menu'),
        ('bolt', 'News Update')
    ]
    
    for icon_class, label in social_patterns:
        # Match <a> or <button> containing the icon but no aria-label
        # Using a regex that tries to find the tag and inject aria-label if missing
        pattern = rf'<(a|button)([^>]*?)(class="[^"]*?"|href="[^"]*?"|id="[^"]*?")[^>]*?>\s*<i class="[^"]*?fa-{icon_class}[^"]*?"></i>\s*</\1>'
        def replace_with_label(match):
            tag = match.group(1)
            attrs = match.group(2) + match.group(3)
            if 'aria-label' in match.group(0):
                return match.group(0)
            return f'<{tag}{match.group(2)}{match.group(3)} aria-label="{label}"><i class="fas fa-{icon_class}"></i></{tag}>'
            
        # Standardize icons to fas/fab as needed (some were fab)
        new_content = re.sub(rf'<(a|button)([^>]*?)>\s*<i class="(fas|fab) fa-{icon_class}[^"]*?"></i>\s*</\1>', 
                             rf'<\1 \2 aria-label="{label}"><i class="\3 fa-{icon_class}"></i></\1>', 
                             new_content)

    # 3. Contrast Issues: Often text-gray-500 on dark background
    # Improve text-gray-500 (#6B7280) to text-gray-400 or higher on dark bg
    # new_content = new_content.replace('text-gray-500', 'text-gray-400')
    # new_content = new_content.replace('text-gray-400', 'text-gray-300')

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
                if fix_accessibility(file_path):
                    count += 1
                    print(f"Fixed Accessibility in {file_path}")
    print(f"Total files improved: {count}")

if __name__ == "__main__":
    main()
