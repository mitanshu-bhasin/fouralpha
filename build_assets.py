import os
import subprocess
import re

dir_path = r"d:\security-tools\Four Alpha"

print("Building Assets...")
print("Running Tailwind Build with minify...")
subprocess.run(["npx", "tailwindcss", "-o", "tailwind-output.min.css", "--minify"], cwd=dir_path, check=False, shell=True)

print("Minifying regular CSS (styles.css)...")
subprocess.run(["npx", "postcss", "styles.css", "-u", "cssnano", "-o", "styles.min.css"], cwd=dir_path, check=False, shell=True)

print("Minifying JS files...")
js_files = ["script.js", "auth.js", "cms.js", "admin-cms.js", "contact.js", "chatbot.js"]
for js in js_files:
    js_path = os.path.join(dir_path, js)
    if os.path.exists(js_path):
        min_js = js.replace(".js", ".min.js")
        print(f"Minifying {js} -> {min_js}")
        subprocess.run(["npx", "terser", js, "-o", min_js, "-c", "-m"], cwd=dir_path, check=False, shell=True)

print("Updating HTML attributes to point to minified files...")

def replace_in_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Replace css
    content = re.sub(r'href="([^"]*)tailwind-output\.css[^"]*"', r'href="\1tailwind-output.min.css"', content)
    content = re.sub(r'href="([^"]*)styles\.css[^"]*"', r'href="\1styles.min.css"', content)

    # Replace JS mappings
    for js in js_files:
        min_js = js.replace(".js", ".min.js")
        # Ensure we don't accidentally replace already minified files
        pattern = r'src="([^"]*(?<!\.min)\/?)' + re.escape(js) + r'[^"]*"'
        content = re.sub(pattern, r'src="\1' + min_js + '"', content)

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

for root, _, files in os.walk(dir_path):
    for file in files:
        if file.endswith(".html"):
            replace_in_file(os.path.join(root, file))

print("Asset Bundling Complete! You can run this whenever you finish modifying assets locally.")
