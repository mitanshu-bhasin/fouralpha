import re
import glob

count = 0
for f in glob.glob('**/*.html', recursive=True):
    if 'node_modules' in f or '.gemini' in f: continue
    
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
        
    def fix_publisher_name(match):
        schema_content = match.group(0)
        schema_content = re.sub(
            r'("@type"\s*:\s*"Organization",\s*"name"\s*:\s*")[^"]*(")',
            r'\g<1>Four Alpha AED Lab\g<2>',
            schema_content
        )
        return schema_content

    new_content = re.sub(r'<script type="application/ld\+json">.*?</script>', fix_publisher_name, content, flags=re.IGNORECASE|re.DOTALL)
    
    if new_content != content:
        with open(f, 'w', encoding='utf-8') as file:
            file.write(new_content)
        count += 1

print(f"Fixed publisher name in schema for {count} files.")
