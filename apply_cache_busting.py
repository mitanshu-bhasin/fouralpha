import os
import re

def process_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Define the assets and their new version string
    version = "1.0.5"
    
    # Patterns to match script and link tags for our core assets
    # Matches script.js, styles.css, tailwind-output.css potentially with existing query strings
    replacements = [
        (r'script\.js(\?v=[^"\']*)?', f'script.js?v={version}'),
        (r'styles\.css(\?v=[^"\']*)?', f'styles.css?v={version}'),
        (r'tailwind-output\.css(\?v=[^"\']*)?', f'tailwind-output.css?v={version}'),
        (r'auth\.js(\?v=[^"\']*)?', f'auth.js?v={version}'),
        (r'cms\.js(\?v=[^"\']*)?', f'cms.js?v={version}'),
        (r'chatbot\.js(\?v=[^"\']*)?', f'chatbot.js?v={version}')
    ]

    new_content = content
    for pattern, replacement in replacements:
        new_content = re.sub(pattern, replacement, new_content)

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
                if process_file(file_path):
                    count += 1
                    print(f"Updated {file_path}")
    print(f"Total files updated for cache busting: {count}")

if __name__ == "__main__":
    main()
