import os
import re
import glob

def absolute_footer_unification(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Determine depth and prefix
    depth = file_path.replace('\\', '/').count('/')
    prefix = '../' * depth

    # 1. CAPTURE THE TICKER IF IT EXISTS
    ticker_pattern = r'<div class="ticker-wrap[^>]*?>.*?</div>\s*</div>'
    ticker_match = re.search(ticker_pattern, content, re.DOTALL | re.IGNORECASE)
    ticker_html = ticker_match.group(0) if ticker_match else ""

    # 2. DEFINE THE CLEAN TOP SECTION (Brand, Links, Socials)
    # Note: Using prefix for links if needed, but usually links are relative to root or we adjust
    # For now, let's keep them as they were or standardize.
    
    # We'll use absolute-ish paths for images (relative to root)
    
    brand_html = f'''
        <div class="max-w-7xl mx-auto w-full px-4 sm:px-6 lg:px-8 py-12">
            <div class="flex flex-col md:flex-row justify-between items-center gap-10">
                <div class="flex items-center gap-4">
                    <div class="w-12 h-12 rounded-full bg-gold/10 flex items-center justify-center text-gold border border-gold/20 shadow-[0_0_20px_rgba(255,184,0,0.1)]">
                        <i class="fas fa-dna text-xl"></i>
                    </div>
                    <div>
                        <h4 class="font-black tracking-[0.2em] text-xl text-white uppercase">Four Alpha <span class="text-gold">AED Lab</span></h4>
                        <p class="text-[10px] text-gray-500 uppercase tracking-[0.3em] mt-1">Foundational Framework for Human Excellence</p>
                    </div>
                </div>
                
                <div class="flex flex-wrap justify-center gap-x-8 gap-y-4 text-[11px] font-bold text-gray-400 uppercase tracking-widest">
                    <a href="{prefix}index.html" class="hover:text-gold transition-colors">Home</a>
                    <a href="{prefix}about-deepak.html" class="hover:text-gold transition-colors">About</a>
                    <a href="{prefix}policy-governance.html" class="hover:text-gold transition-colors">Policy</a>
                    <a href="{prefix}contact.html" class="hover:text-gold transition-colors">Contact</a>
                    <a href="{prefix}privacy.html" class="hover:text-gold transition-colors">Privacy</a>
                    <a href="{prefix}terms.html" class="hover:text-gold transition-colors">Terms</a>
                </div>
                
                <div class="flex gap-5">
                    <a href="https://facebook.com/4a.aed.lab/" class="w-10 h-10 rounded-full bg-white/5 border border-white/10 flex items-center justify-center hover:bg-gold hover:text-cosmic-dark transition-all duration-300 shadow-lg"><i class="fab fa-facebook-f"></i></a>
                    <a href="https://x.com/4A_AED_Lab" class="w-10 h-10 rounded-full bg-white/5 border border-white/10 flex items-center justify-center hover:bg-gold hover:text-cosmic-dark transition-all duration-300 shadow-lg"><i class="fab fa-x-twitter"></i></a>
                    <a href="https://instagram.com/4a_aed_lab/" class="w-10 h-10 rounded-full bg-white/5 border border-white/10 flex items-center justify-center hover:bg-gold hover:text-cosmic-dark transition-all duration-300 shadow-lg"><i class="fab fa-instagram"></i></a>
                    <a href="https://linkedin.com/company/4-%CE%B1-aed-lab/" class="w-10 h-10 rounded-full bg-white/5 border border-white/10 flex items-center justify-center hover:bg-gold hover:text-cosmic-dark transition-all duration-300 shadow-lg"><i class="fab fa-linkedin-in"></i></a>
                </div>
            </div>
        </div>'''

    # 3. THE EXPANDED PARTNERSHIP BLOCK (Bottom)
    partnership_block = f'''
        <div class="max-w-7xl mx-auto w-full px-4 sm:px-6 lg:px-8 py-24">
            <div class="flex flex-col items-center justify-center border-t border-white/5 pt-20">
                <div class="flex flex-col md:flex-row items-center justify-center gap-16 md:gap-40 mb-20 w-full">
                    <div class="flex items-center gap-8 group">
                        <img src="{prefix}ipec.jpg" class="h-16 rounded-xl shadow-2xl border border-white/10 grayscale group-hover:grayscale-0 transition-all duration-700" alt="IPEC">
                        <div class="flex flex-col">
                            <span class="text-[14px] font-black tracking-[0.4em] uppercase text-gray-300 group-hover:text-white transition-colors">International Process Excellence Council</span>
                            <span class="text-[11px] text-gray-600 uppercase tracking-widest mt-2">Strategic Standards Partner</span>
                        </div>
                    </div>
                    <div class="hidden md:block w-px h-24 bg-white/5"></div>
                    <div class="flex items-center gap-8 group">
                        <img src="{prefix}logo.jpeg" class="h-16 rounded-full shadow-2xl border border-white/10" alt="Four Alpha">
                        <div class="flex flex-col">
                            <span class="text-[14px] font-black tracking-[0.4em] uppercase text-gray-300 group-hover:text-gold transition-colors">Four Alpha AED Lab</span>
                            <span class="text-[11px] text-gold/40 uppercase tracking-widest mt-2">Foundational Framework Provider</span>
                        </div>
                    </div>
                </div>
                
                <div class="flex flex-col items-center gap-12">
                    <div class="flex flex-col md:flex-row items-center gap-10 md:gap-20 text-[12px] text-gray-500 uppercase tracking-[0.6em] font-mono">
                        <span>&copy; 2026 Four Alpha AED Lab</span>
                        <span class="hidden md:block text-white/5">|</span>
                        <span>All Rights Reserved</span>
                        <span class="hidden md:block text-white/5">|</span>
                        <a href="{prefix}license.html" class="text-gold/40 hover:text-gold transition-all hover:tracking-[0.8em] underline underline-offset-[16px] decoration-gold/20 hover:decoration-gold">License & Usage Restriction</a>
                    </div>
                    <div class="bg-red-500/[0.02] border border-red-500/10 px-12 py-5 rounded-full backdrop-blur-sm">
                        <p class="text-[11px] text-red-500/40 tracking-[0.5em] uppercase font-bold text-center">
                            Notice: Unauthorized reuse or reproduction of architecture is strictly prohibited.
                        </p>
                    </div>
                </div>
            </div>
        </div>'''

    # 4. RECONSTRUCT THE FOOTER
    new_footer = f'<footer class="bg-cosmic-dark text-white border-t border-white/10 relative z-10 flex flex-col">{ticker_html}{brand_html}{partnership_block}</footer>'
    
    # 5. REPLACE THE ENTIRE FOOTER TAG
    # Broad pattern for <footer>...</footer>
    footer_tag_pattern = r'<footer[^>]*?>.*?</footer>'
    
    if re.search(footer_tag_pattern, content, re.DOTALL | re.IGNORECASE):
        updated_content = re.sub(footer_tag_pattern, new_footer, content, flags=re.DOTALL | re.IGNORECASE)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(updated_content)
        return True
    return False

html_files = glob.glob('**/*.html', recursive=True)
updated_count = 0
for file in html_files:
    if 'node_modules' in file or '.gemini' in file:
        continue
    if absolute_footer_unification(file):
        updated_count += 1

print(f"Absolutely unified footer in {updated_count} files.")
