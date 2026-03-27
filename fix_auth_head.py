file_paths = [r'c:\Users\mitan\Videos\Four Alpha\login.html', r'c:\Users\mitan\Videos\Four Alpha\signup.html', r'c:\Users\mitan\Videos\Four Alpha\admin.html']

for f in file_paths:
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
        
    if 'localStorage.getItem("fourAlphaUser")' not in content:
        if f.endswith('admin.html'):
            insert_str = '''<script>
    if (localStorage.getItem("fourAlphaUser")) {
        try {
            const userObj = JSON.parse(localStorage.getItem("fourAlphaUser"));
            if (userObj && userObj.email !== "info@fouralpha.org") {
                // If not admin, they are kept waiting and auth.js re-redirects or denies access.
            } else if (userObj && userObj.email === "info@fouralpha.org") {
                // Pre-unhide to avoid delay flash
                document.addEventListener('DOMContentLoaded', () => {
                    const c = document.getElementById("access-denied");
                    const p = document.getElementById("admin-panel");
                    const u = document.getElementById("auth-status");
                    if(c && p && u) {
                        c.classList.add("hidden");
                        p.classList.remove("hidden");
                        u.innerHTML = `<span class="text-green-500"><i class="fas fa-signal"></i> CACHED CONNECTION</span> | ${userObj.email}`;
                    }
                });
            }
        } catch(e) {}
    }
</script>
'''
        else:
            insert_str = '''<script>
    if (localStorage.getItem("fourAlphaUser")) {
        try {
            const userObj = JSON.parse(localStorage.getItem("fourAlphaUser"));
            if (userObj && userObj.email) {
                window.location.replace("dashboard.html");
            }
        } catch(e) {}
    }
</script>
'''
        # Insert right after <meta charset="UTF-8"> or inside <head>
        if '<meta charset="UTF-8">' in content:
            content = content.replace('<meta charset="UTF-8">', f'<meta charset="UTF-8">\n{insert_str}')
        else:
            content = content.replace('<head>', f'<head>\n{insert_str}')

        with open(f, 'w', encoding='utf-8') as file:
            file.write(content)
        print(f"Updated {f}")
    else:
        print(f"Skipped {f} (already has logic)")
