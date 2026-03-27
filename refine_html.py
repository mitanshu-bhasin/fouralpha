import os
import re

def optimize_html_final(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    new_content = content

    # 1. Ensure <main> landmark
    # If <main> is missing, add it. If already added by previous script, clean it up.
    if '<main' not in new_content and '</nav>' in new_content and '<footer' in new_content:
        new_content = new_content.replace('</nav>', '</nav><main id="main-content">', 1)
        new_content = new_content.replace('<footer', '</main><footer', 1)

    # 2. Fix Accessibility Names (Buttons and Links)
    # Remove existing conflicting aria-labels first to avoid duplicates
    new_content = re.sub(r'\s+aria-label="[^"]*?"', '', new_content)
    
    # Add aria-label to mobile menu button
    new_content = new_content.replace('id="mobile-menu-button"', 'id="mobile-menu-button" aria-label="Open Navigation Menu"')
    
    # Add aria-label to social links (matching by href or icon class)
    new_content = re.sub(r'<a([^>]*?)href="[^"]*?facebook\.com[^"]*?"([^>]*?)>', r'<a\1href="https://facebook.com/4a.aed.lab/"\2 aria-label="Follow us on Facebook">', new_content)
    new_content = re.sub(r'<a([^>]*?)href="[^"]*?x\.com[^"]*?"([^>]*?)>', r'<a\1href="https://x.com/4A_AED_Lab"\2 aria-label="Follow us on X">', new_content)
    new_content = re.sub(r'<a([^>]*?)href="[^"]*?instagram\.com[^"]*?"([^>]*?)>', r'<a\1href="https://instagram.com/4a_aed_lab/"\2 aria-label="Follow us on Instagram">', new_content)
    new_content = re.sub(r'<a([^>]*?)href="[^"]*?linkedin\.com[^"]*?"([^>]*?)>', r'<a\1href="https://linkedin.com/company/4-%CE%B1-aed-lab/"\2 aria-label="Follow us on LinkedIn">', new_content)

    # 3. Fix Contrast: text-gray-500 is too dark on #0A0F24
    new_content = new_content.replace('text-gray-500', 'text-gray-400')
    new_content = new_content.replace('text-gray-600', 'text-gray-300') # Improve footer partner text too

    # 4. Performance: Preload Critical CSS
    # Add <link rel="preload" as="style"> for the main CSS files
    if '<link rel="preload"' not in new_content:
        preload_tags = '\n<link rel="preload" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.6.0/css/all.min.css" as="style" onload="this.onload=null;this.rel=\'stylesheet\'">\n'
        new_content = new_content.replace('<head>', '<head>' + preload_tags, 1)

    # 5. Accessibility: Language attribute
    if '<html lang="en">' not in new_content:
        new_content = new_content.replace('<html', '<html lang="en"', 1)

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
                if optimize_html_final(file_path):
                    count += 1
                    print(f"Optimized {file_path}")
    print(f"Total files improved: {count}")

if __name__ == "__main__":
    main()
