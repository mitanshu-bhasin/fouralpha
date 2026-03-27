import os
import re
import glob

def surgical_footer_fix(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Determine prefix
    depth = file_path.replace('\\', '/').count('/')
    prefix = '../' * depth

    # 1. IDENTIFY THE END OF THE TOP FOOTER SECTION (Links/Socials)
    # The social section usually ends with the LinkedIn link and some closing divs.
    # Looking at the HTML: ...fab fa-linkedin-in"></i></a></div></div></div>
    
    footer_top_pattern = r'(<footer[^>]*?>.*?fab fa-linkedin-in"></i></a></div></div></div>)'
    
    match = re.search(footer_top_pattern, content, re.DOTALL | re.IGNORECASE)
    if not match:
        # Fallback for pages that might have a different structure but still have </footer>
        # We'll just try to find the last </footer> and work backwards.
        if '</footer>' not in content:
            return False
            
        # If we can't find the social icons, we'll just wipe everything and use a standard footer
        # but the user likes the top part.
        return False

    header_part = match.group(1)
    
    # 2. THE FINAL EXPANDED PREMIUM BLOCK
    final_block = f'''
    <div class="max-w-7xl mx-auto w-full px-4 sm:px-6 lg:px-8 py-20">
        <div class="flex flex-col items-center justify-center border-t border-white/5 pt-20 transition-all duration-1000">
            <div class="flex flex-col md:flex-row items-center justify-center gap-12 md:gap-32 mb-16 w-full">
                <div class="flex items-center gap-6 group">
                    <div class="relative">
                        <div class="absolute -inset-2 bg-white/5 rounded-lg blur opacity-0 group-hover:opacity-40 transition duration-1000"></div>
                        <img src="{prefix}ipec.jpg" class="relative h-14 rounded-lg shadow-2xl border border-white/5 grayscale group-hover:grayscale-0 transition-all duration-500" alt="IPEC">
                    </div>
                    <div class="flex flex-col">
                        <span class="text-[13px] font-black tracking-[0.3em] uppercase text-gray-400 group-hover:text-white transition-colors duration-500">International Process Excellence Council</span>
                        <span class="text-[10px] text-gray-600 uppercase tracking-widest mt-1">Strategic Standards Partner</span>
                    </div>
                </div>
                <div class="hidden md:block w-px h-20 bg-gradient-to-b from-transparent via-white/10 to-transparent"></div>
                <div class="flex items-center gap-6 group">
                    <div class="relative">
                        <div class="absolute -inset-2 bg-gold/10 rounded-full blur opacity-0 group-hover:opacity-40 transition duration-1000"></div>
                        <img src="{prefix}logo.jpeg" class="relative h-14 rounded-full shadow-2xl border border-white/5" alt="Four Alpha">
                    </div>
                    <div class="flex flex-col">
                        <span class="text-[13px] font-black tracking-[0.3em] uppercase text-gray-400 group-hover:text-gold transition-colors duration-500">Four Alpha AED Lab</span>
                        <span class="text-[10px] text-gold/40 uppercase tracking-widest mt-1">Foundational Framework Provider</span>
                    </div>
                </div>
            </div>
            
            <div class="flex flex-col items-center gap-10">
                <div class="flex flex-col md:flex-row items-center gap-8 md:gap-14 text-[11px] text-gray-500 uppercase tracking-[0.5em] font-mono">
                    <span class="hover:text-gray-300 transition-colors cursor-default">&copy; 2026 Four Alpha AED Lab</span>
                    <span class="hidden md:block text-white/5">|</span>
                    <span class="text-gray-700">All Rights Reserved</span>
                    <span class="hidden md:block text-white/5">|</span>
                    <a href="{prefix}license.html" class="text-gold/40 hover:text-gold transition-all hover:tracking-[0.6em] underline underline-offset-[12px] decoration-gold/20 hover:decoration-gold">License & Usage Restriction</a>
                </div>
                <div class="bg-red-500/[0.03] border border-red-500/10 px-10 py-4 rounded-full backdrop-blur-sm">
                    <p class="text-[10px] text-red-400/50 tracking-[0.4em] uppercase font-bold text-center">
                        Unauthorized reuse or reproduction of architecture is strictly prohibited.
                    </p>
                </div>
            </div>
        </div>
    </div>
</footer>'''

    # Swap the footer content
    # We find where parts[0] + header_part ends and </footer> ends.
    # Everything in between is duplication.
    
    # Let's use re.sub to replace from the end of header_part until the end of </footer>
    # Escape header_part for regex
    escaped_header = re.escape(header_part)
    pattern = escaped_header + r'.*?</footer>'
    
    new_content = re.sub(pattern, header_part + final_block, content, flags=re.DOTALL | re.IGNORECASE)

    if new_content != content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True
    return False

html_files = glob.glob('**/*.html', recursive=True)
updated_count = 0
for file in html_files:
    if 'node_modules' in file or '.gemini' in file:
        continue
    if surgical_footer_fix(file):
        updated_count += 1

print(f"Surgically fixed and unified footer in {updated_count} files.")
