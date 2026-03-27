import os
import re
import glob

def reconstruct_footer(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Determine prefix
    depth = file_path.replace('\\', '/').count('/')
    prefix = '../' * depth

    # 1. REMOVE THE STRAY DUPLICATED BLOCKS
    # We will search for the specific duplicated strings observed in the minified output
    
    # Pattern 1: The stray copyright div that appears above the partnership block
    stray_copyright_pattern = r'<div class="text-\[10px\] text-gray-500 uppercase tracking-widest font-mono text-center md:text-right">\s*&copy; 2026 Four Alpha AED Lab. All rights reserved.\s*</div>'
    content = re.sub(stray_copyright_pattern, '', content, flags=re.IGNORECASE | re.DOTALL)

    # Pattern 2: The previous version of the partnership block (to ensure no double overhaul)
    previous_overhaul_pattern = r'<div class="max-w-7xl mx-auto w-full px-4 sm:px-6 lg:px-8 py-12">\s*<div class="flex flex-col items-center justify-center text-xs text-gray-600 border-t border-white/5 pt-12.*?</div>\s*</div>'
    content = re.sub(previous_overhaul_pattern, '', content, flags=re.IGNORECASE | re.DOTALL)

    # Pattern 3: Any other partnership variants
    partnership_variants = [
        r'<div class="w-full border-t border-white/5 mt-8 pt-8 pb-4"><div class="max-w-7xl mx-auto px-4.*?</div></div>',
        r'<div class="flex flex-col md:flex-row justify-between items-center text-xs text-gray-600 mt-10 border-t border-white/5 pt-8 gap-8.*?</div>',
        r'<div class="max-w-7xl mx-auto w-full px-4 sm:px-6 lg:px-8">\s*<div class="flex flex-col items-center justify-center text-xs text-gray-600 border-t border-white/5 mt-10 pt-10 pb-\d+.*?</div>\s*</div>'
    ]
    for p in partnership_variants:
        content = re.sub(p, '', content, flags=re.IGNORECASE | re.DOTALL)

    # 2. CONSTRUCTION OF THE FINAL PREMIUM FOOTER
    # We will attach this at the very end of the <footer> content
    
    final_footer_html = f'''<div class="max-w-7xl mx-auto w-full px-4 sm:px-6 lg:px-8 py-16">
    <div class="flex flex-col items-center justify-center border-t border-white/5 pt-16 opacity-90 hover:opacity-100 transition-opacity duration-700">
        <div class="flex flex-col md:flex-row items-center justify-center gap-10 md:gap-32 mb-12 w-full">
            <div class="flex items-center gap-5 group">
                <div class="relative">
                    <div class="absolute -inset-1 bg-white/5 rounded blur opacity-25 group-hover:opacity-50 transition duration-1000"></div>
                    <img src="{prefix}ipec.jpg" class="relative h-12 rounded shadow-2xl border border-white/10" alt="IPEC">
                </div>
                <div class="flex flex-col">
                    <span class="text-[12px] font-black tracking-[0.3em] uppercase text-gray-200 group-hover:text-white transition-colors">International Process Excellence Council</span>
                    <span class="text-[9px] text-gray-500 uppercase tracking-widest mt-1">Strategic Standards Partner</span>
                </div>
            </div>
            <div class="hidden md:block w-px h-16 bg-gradient-to-b from-transparent via-white/10 to-transparent"></div>
            <div class="flex items-center gap-5 group">
                <div class="relative">
                    <div class="absolute -inset-1 bg-gold/10 rounded-full blur opacity-25 group-hover:opacity-50 transition duration-1000"></div>
                    <img src="{prefix}logo.jpeg" class="relative h-12 rounded-full shadow-2xl border border-white/10" alt="Four Alpha">
                </div>
                <div class="flex flex-col">
                    <span class="text-[12px] font-black tracking-[0.3em] uppercase text-gray-200 group-hover:text-white transition-colors">Four Alpha AED Lab</span>
                    <span class="text-[9px] text-gold/40 uppercase tracking-widest mt-1">Foundational Framework Provider</span>
                </div>
            </div>
        </div>
        
        <div class="flex flex-col items-center gap-8">
            <div class="flex flex-col md:flex-row items-center gap-6 md:gap-12 text-[11px] text-gray-400 uppercase tracking-[0.5em] font-mono">
                <span>&copy; 2026 All Rights Reserved</span>
                <span class="hidden md:block text-white/5">|</span>
                <a href="{prefix}license.html" class="text-gold/50 hover:text-gold transition-all hover:tracking-[0.6em] underline underline-offset-8 decoration-gold/20 hover:decoration-gold">License & Usage Restriction</a>
            </div>
            <div class="bg-red-500/5 border border-red-500/10 px-8 py-3 rounded-full">
                <p class="text-[9px] text-red-400/60 tracking-[0.4em] uppercase font-bold">
                    Notice: Unauthorized reuse or reproduction of architecture is strictly prohibited.
                </p>
            </div>
        </div>
    </div>
</div>'''

    if '</footer>' in content:
        # Surgically remove any remnants before </footer>
        # We look for the closing </footer> and insert our block right before it, 
        # but only if it's the LAST sub-block.
        
        # To be safe, we split by </footer> and reconstruct.
        parts = content.split('</footer>')
        # parts[0] is everything before footer end. 
        # We append our block to parts[0] and then add back the closing tags.
        new_content = parts[0] + final_footer_html + '</footer>' + '</footer>'.join(parts[1:])
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True
        
    return False

html_files = glob.glob('**/*.html', recursive=True)
updated_count = 0
for file in html_files:
    if 'node_modules' in file or '.gemini' in file:
        continue
    if reconstruct_footer(file):
        updated_count += 1

print(f"Finalized and deduplicated footer in {updated_count} files.")
