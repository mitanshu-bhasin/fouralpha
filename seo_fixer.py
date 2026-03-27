import os
import re
import glob

html_files = glob.glob('**/*.html', recursive=True)

def update_meta_tag(content, attribute_name, attribute_value, new_value):
    # Match <meta name="description" content="old"> OR <meta content="old" name="description">
    pattern1 = rf'(<meta[^>]*?{attribute_name}="{attribute_value}"[^>]*?content=")[^"]*(")'
    pattern2 = rf'(<meta[^>]*?content=")[^"]*("[^>]*?{attribute_name}="{attribute_value}")'
    
    content, count1 = re.subn(pattern1, rf'\g<1>{new_value}\g<2>', content, flags=re.IGNORECASE)
    if count1 == 0:
        content, _ = re.subn(pattern2, rf'\g<1>{new_value}\g<2>', content, flags=re.IGNORECASE)
    return content

def get_seo(filepath):
    normalized = filepath.replace('\\', '/')
    parts = normalized.split('/')
    
    if normalized == 'index.html' or (len(parts) == 1 and parts[0] == 'index.html'):
        return (
            "Optimize Your Potential. Eliminate The Friction. | Four Alpha AED Lab",
            "Four Alpha AED Lab synthesizes Lean Six Sigma for Personal Development and ancient wisdom into a Behavioral Excellence Framework. Measure your N* baseline today."
        )
    
    if parts[-1] == 'index.html':
        name_part = parts[-2].replace('-', ' ').title()
    else:
        name_part = parts[-1].replace('.html', '').replace('-', ' ').title()

    if 'education-policy/global/brics' in normalized:
        desc = f"Learn about the {name_part} frameworks within the Global Education Policy (BRICS). Four Alpha AED Lab provides comprehensive insights into the evolution and impact of these educational paradigms on a global scale."
        title = f"{name_part} - BRICS Global Education Policy | Four Alpha AED Lab"
    elif 'education-policy/global/saarc' in normalized:
        desc = f"Explore the {name_part} frameworks within the Global Education Policy (SAARC). Analyze regional educational architectures and strategic alignment with Four Alpha AED Lab."
        title = f"{name_part} - SAARC Global Education Policy | Four Alpha AED Lab"
    elif 'education-policy/national' in normalized:
        name_upper = name_part.upper()
        desc = f"Discover the strategic roadmap of {name_upper}. Four Alpha AED Lab dissects national educational policies and their foundational implications for future optimization."
        title = f"{name_upper} - National Education Policy | Four Alpha AED Lab"
    elif 'education-policy' in normalized:
        desc = f"Explore {name_part} at Four Alpha AED Lab. Understand how macroscopic educational guidelines influence gross operative mechanics and subtle developmental metrics."
        title = f"{name_part} - Education Policy | Four Alpha AED Lab"
    elif 'belt' in normalized.lower():
        prefix = name_part.lower().replace('belt', '').strip().title()
        if not prefix: prefix = name_part.title()
        belt_name = f"{prefix} Belt"
        desc = f"Achieve excellence with the {belt_name} certification. Join Four Alpha AED Lab to master advanced operational strategies, systematic problem-solving, and human potential optimization."
        title = f"{belt_name.title()} Certification | Four Alpha AED Lab"
    elif 'alpha-' in normalized.lower():
        app_name = name_part.replace('Alpha', 'Alpha ')
        desc = f"Discover the {app_name} application sphere. Four Alpha AED Lab explores the dynamics of systemic performance and strategic alignment for this critical human behavioral domain."
        title = f"{app_name.title()} | Four Alpha AED Lab"
    else:
        desc = f"Explore {name_part} at Four Alpha AED Lab. Uncover foundational frameworks, strategic implications, and actionable mechanics for optimizing human trajectory and operational equilibrium."
        title = f"{name_part} | Four Alpha AED Lab"
        
    return title, desc

count = 0
for f in html_files:
    if 'node_modules' in f or '.gemini' in f:
        continue
        
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
        
    title, desc = get_seo(f)
    
    # 1. Update <title>
    content = re.sub(r'(<title[^>]*>).*?(</title>)', rf'\g<1>{title}\g<2>', content, flags=re.IGNORECASE|re.DOTALL)
    
    # 2. Meta tags
    content = update_meta_tag(content, "name", "description", desc)
    content = update_meta_tag(content, "property", "og:title", title)
    content = update_meta_tag(content, "property", "og:description", desc)
    content = update_meta_tag(content, "name", "twitter:title", title)
    content = update_meta_tag(content, "name", "twitter:description", desc)
    
    # 3. JSON-LD schema
    def schema_replacer(match):
        schema_content = match.group(0)
        safe_title = title.replace('"', '\\"')
        safe_desc = desc.replace('"', '\\"')
        schema_content = re.sub(r'("name"\s*:\s*")[^"]*(")', rf'\g<1>{safe_title}\g<2>', schema_content)
        schema_content = re.sub(r'("description"\s*:\s*")[^"]*(")', rf'\g<1>{safe_desc}\g<2>', schema_content)
        return schema_content

    content = re.sub(r'<script type="application/ld\+json">.*?</script>', schema_replacer, content, flags=re.IGNORECASE|re.DOTALL)
    
    with open(f, 'w', encoding='utf-8') as file:
        file.write(content)
    count += 1

print(f"Successfully injected SEO logic across {count} files.")
