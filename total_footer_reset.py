import os
import re
import glob

def total_footer_reset(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Determine prefix
    depth = file_path.replace('\\', '/').count('/')
    prefix = '../' * depth

    # 1. WIPE ALL PREVIOUS COPYRIGHT AND PARTNERSHIP ATTEMPTS
    # We'll use a very broad collection of patterns
    patterns = [
        # Any div or p with &copy; 2026
        r'<(div|p)[^>]*?>\s*&copy; 2026.*?</\1>',
        # The specific minified blocks we added recently
        r'<div class="max-w-7xl mx-auto w-full px-4 sm:px-6 lg:px-8 py-\d+">.*?</div>\s*</div>',
        # Any partnership variants
        r'<div class="w-full border-t border-white/5 mt-8 pt-8 pb-4">.*?</div></div>',
        r'<div class="flex flex-col md:flex-row justify-between items-center text-xs text-gray-600 mt-10 border-t border-white/5 pt-8 gap-8.*?</div>'
    ]
    
    cleaned_content = content
    for p in patterns:
        cleaned_content = re.sub(p, '', cleaned_content, flags=re.DOTALL | re.IGNORECASE)

    # Secondary sweep for loose &copy; 2026 that might be in different tags
    cleaned_content = re.sub(r'&copy; 2026.*?(?=</p>|</div>|$)', '', cleaned_content, flags=re.IGNORECASE)

    # 2. THE FINAL EXPANDED PREMIUM BLOCK
    # Centered, large, including License link
    final_block = f'''
    <div class="max-w-7xl mx-auto w-full px-4 sm:px-6 lg:px-8 py-24">
        <div class="flex flex-col items-center justify-center border-t border-white/5 pt-20 transition-all duration-1000">
            <div class="flex flex-col md:flex-row items-center justify-center gap-16 md:gap-40 mb-20 w-full">
                <div class="flex items-center gap-8 group">
                    <div class="relative">
                        <div class="absolute -inset-4 bg-white/5 rounded-xl blur opacity-0 group-hover:opacity-40 transition duration-1000"></div>
                        <img src="{prefix}ipec.jpg" class="relative h-16 rounded-xl shadow-2xl border border-white/5 grayscale group-hover:grayscale-0 transition-all duration-700" alt="IPEC">
                    </div>
                    <div class="flex flex-col">
                        <span class="text-[14px] font-black tracking-[0.4em] uppercase text-gray-400 group-hover:text-white transition-colors duration-700">International Process Excellence Council</span>
                        <span class="text-[11px] text-gray-600 uppercase tracking-widest mt-2">Strategic Standards Partner</span>
                    </div>
                </div>
                <div class="hidden md:block w-px h-24 bg-gradient-to-b from-transparent via-white/10 to-transparent"></div>
                <div class="flex items-center gap-8 group">
                    <div class="relative">
                        <div class="absolute -inset-4 bg-gold/10 rounded-full blur opacity-0 group-hover:opacity-40 transition duration-1000"></div>
                        <img src="{prefix}logo.jpeg" class="relative h-16 rounded-full shadow-2xl border border-white/5" alt="Four Alpha">
                    </div>
                    <div class="flex flex-col">
                        <span class="text-[14px] font-black tracking-[0.4em] uppercase text-gray-400 group-hover:text-gold transition-colors duration-700">Four Alpha AED Lab</span>
                        <span class="text-[11px] text-gold/40 uppercase tracking-widest mt-2">Foundational Framework Provider</span>
                    </div>
                </div>
            </div>
            
            <div class="flex flex-col items-center gap-12">
                <div class="flex flex-col md:flex-row items-center gap-10 md:gap-20 text-[12px] text-gray-500 uppercase tracking-[0.6em] font-mono">
                    <span class="hover:text-gray-200 transition-colors duration-500">&copy; 2026 Four Alpha AED Lab</span>
                    <span class="hidden md:block text-white/5">|</span>
                    <span class="text-gray-700">All Rights Reserved</span>
                    <span class="hidden md:block text-white/5">|</span>
                    <a href="{prefix}license.html" class="text-gold/30 hover:text-gold transition-all hover:tracking-[0.8em] underline underline-offset-[16px] decoration-gold/10 hover:decoration-gold transition-all duration-500">License & Usage Restriction</a>
                </div>
                <div class="bg-red-500/[0.02] border border-red-500/10 px-12 py-5 rounded-full backdrop-blur-md">
                    <p class="text-[11px] text-red-500/40 tracking-[0.5em] uppercase font-bold text-center">
                        Unauthorized reuse or reproduction of architecture is strictly prohibited.
                    </p>
                </div>
            </div>
        </div>
    </div>'''

    if '</footer>' in cleaned_content:
        # We append to the very end of </footer>
        # Remove any stray content inside <footer> that might be left
        # We find the <footer> start and keep only the first structured section (Links/Socials)
        
        # Pattern to keep until social icons end
        keep_pattern = r'(<footer[^>]*?>.*?fab fa-linkedin-in"></i></a></div></div></div>)'
        header_match = re.search(keep_pattern, cleaned_content, re.DOTALL | re.IGNORECASE)
        
        if header_match:
            header = header_match.group(1)
            # Reconstruct the file: Content before footer + header + our block + any content after footer
            parts = cleaned_content.split('</footer>')
            final_content = parts[0].split(header)[0] + header + final_block + '</footer>' + '</footer>'.join(parts[1:])
        else:
            # Fallback for simpler footers
            final_content = cleaned_content.replace('</footer>', final_block + '</footer>')
            
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(final_content)
        return True
    return False

html_files = glob.glob('**/*.html', recursive=True)
updated_count = 0
for file in html_files:
    if 'node_modules' in file or '.gemini' in file:
        continue
    if total_footer_reset(file):
        updated_count += 1

print(f"Totally reset and expanded footer in {updated_count} files.")
