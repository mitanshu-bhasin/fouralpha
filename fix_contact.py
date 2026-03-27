import os

filepath = r'c:\Users\mitan\Videos\Four Alpha\contact.html'
with open(filepath, 'r', encoding='utf-8') as f:
    html = f.read()

start_idx = html.find('<div\n                class="glass-box')
if start_idx == -1:
    start_idx = html.find('<div class="glass-box')
    
end_idx = html.find('</section>')

if start_idx != -1 and end_idx != -1:
    new_html = html[:start_idx] + '''<div class="glass-box p-8 sm:p-12 rounded-2xl max-w-5xl text-left shadow-[0_0_30px_rgba(255,184,0,0.1)] relative z-10 w-full border border-white/10">
                <div class="flex items-center justify-between mb-8 pb-4 border-b border-white/10">
                    <div class="flex items-center gap-4">
                        <div class="w-12 h-12 rounded-full border border-gold flex items-center justify-center text-gold shadow-[0_0_10px_rgba(255,184,0,0.2)] bg-cosmic-dark">
                            <i class="fas fa-envelope-open-text text-xl"></i></div>
                        <div>
                            <h1 class="text-2xl font-black tracking-widest text-white uppercase">Get In Touch</h1>
                            <p class="text-xs text-gold font-bold tracking-[0.2em] uppercase opacity-70">Transmission Node</p>
                        </div>
                    </div>
                    <div class="hidden sm:inline-block px-3 py-1 rounded-full bg-green-500/10 border border-green-500/30 text-green-400 text-[10px] font-bold tracking-widest uppercase">Node Active</div>
                </div>

                <div class="grid lg:grid-cols-2 gap-8 items-start">
                    <div class="max-h-[60vh] overflow-y-auto pr-2 custom-scrollbar">
                        <p class="font-serif text-gray-300 text-sm leading-relaxed mb-8">For architectural queries, partnership
                            protocols, or system support, connect via the primary transmission channel.</p>
                        <div class="mb-10">
                            <p class="text-xs text-gold font-bold tracking-[0.3em] uppercase mb-2 opacity-70">Support Email</p>
                            <a href="mailto:info@fouralpha.org"
                                class="text-xl sm:text-2xl font-black text-white hover:text-gold transition-colors break-all">info@fouralpha.org</a>
                        </div>

                        <!-- Contact Form -->
                        <form id="contact-form" class="space-y-4 text-left border-t border-white/10 pt-6 mt-6">
                            <div>
                                <label for="contact-name" class="block text-xs font-bold text-gray-400 uppercase tracking-widest mb-1">Name</label>
                                <input type="text" id="contact-name" required
                                    class="w-full bg-white/5 border border-white/20 rounded px-4 py-3 text-white focus:outline-none focus:border-gold focus:ring-1 focus:ring-gold transition-all" aria-label="Name">
                            </div>
                            <div>
                                <label for="contact-email" class="block text-xs font-bold text-gray-400 uppercase tracking-widest mb-1">Email</label>
                                <input type="email" id="contact-email" required
                                    class="w-full bg-white/5 border border-white/20 rounded px-4 py-3 text-white focus:outline-none focus:border-gold focus:ring-1 focus:ring-gold transition-all" aria-label="Email">
                            </div>
                            <div>
                                <label for="contact-message" class="block text-xs font-bold text-gray-400 uppercase tracking-widest mb-1">Message</label>
                                <textarea id="contact-message" required rows="4"
                                    class="w-full bg-white/5 border border-white/20 rounded px-4 py-3 text-white focus:outline-none focus:border-gold focus:ring-1 focus:ring-gold transition-all" aria-label="Message"></textarea>
                            </div>
                            <div id="contact-toast" class="hidden text-sm font-bold p-3 rounded" role="alert"></div>
                            <button type="submit" id="contact-submit"
                                class="w-full bg-gold text-cosmic-dark py-4 rounded-sm font-black text-sm hover:bg-white hover:text-black transition-all shadow-[0_0_20px_rgba(255,184,0,0.5)] focus:ring-2 focus:ring-offset-2 focus:ring-offset-cosmic-dark focus:ring-gold uppercase tracking-widest flex justify-center items-center gap-2">Initiate Transmission <i class="fas fa-paper-plane"></i></button>
                        </form>
                    </div>

                    <div class="hidden lg:flex justify-center items-center h-full">
                        <img src="contact_hero.png" alt="Communication Protocol" class="w-full max-w-sm rounded-[2rem] object-cover opacity-90 shadow-[0_0_40px_rgba(255,184,0,0.15)] border border-white/5 grayscale-[20%] hover:grayscale-0 transition-all duration-700 hover:shadow-[0_0_50px_rgba(255,184,0,0.3)]">
                    </div>
                </div>

                <div class="mt-8 pt-6 border-t border-white/10 flex flex-col sm:flex-row gap-4">
                    <a href="index.html" class="flex-1 border border-white/20 text-white py-3 rounded-sm font-bold text-center text-xs hover:bg-white/5 transition-colors tracking-widest uppercase">Return to Baseline</a>
                </div>
            </div>
        ''' + html[end_idx:]

    btn_code = '''
    <!-- Back to Top Button -->
    <button id="back-to-top" onclick="window.scrollTo({top:0,behavior:'smooth'})" aria-label="Back to top"
        style="display:none; position:fixed; bottom:90px; right:20px; z-index:90; width:44px; height:44px; border-radius:50%; background:rgba(10,15,36,0.8); border:2px solid #FFB800; color:#FFB800; cursor:pointer; font-size:18px; backdrop-filter:blur(8px); transition:all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275); box-shadow:0 0 15px rgba(255,184,0,0.3); align-items:center; justify-content:center;"
        onmouseover="this.style.background='#FFB800';this.style.color='#0d1117';this.style.boxShadow='0 0 25px rgba(255,184,0,0.6)';this.style.transform='translateY(-3px)'"
        onmouseout="this.style.background='rgba(10,15,36,0.8)';this.style.color='#FFB800';this.style.boxShadow='0 0 15px rgba(255,184,0,0.3)';this.style.transform='translateY(0)'">
        <i class="fas fa-chevron-up"></i>
    </button>
    <script>
        window.addEventListener('scroll', function() {
            var btn = document.getElementById('back-to-top');
            if (window.scrollY > 400) { btn.style.display = 'flex'; } else { btn.style.display = 'none'; }
        });
    </script>
</body>'''
    if 'id="back-to-top"' not in new_html:
        new_html = new_html.replace('</body>', btn_code)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_html)
    print("Success")
else:
    print(f"Could not find delimiters. Start: {start_idx}, End: {end_idx}")
