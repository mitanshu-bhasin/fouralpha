import os

def fix_file(path):
    print(f"Checking {path}...")
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if 'id="mobile-menu"' not in content:
        print("  - mobile-menu not found")
        return False
    
    n_end = content.find('</nav>')
    if n_end == -1:
        print("  - </nav> not found")
        return False
        
    m_id_idx = content.find('id="mobile-menu"')
    m_start = content.rfind('<div', 0, m_id_idx)
    
    print(f"  - m_start: {m_start}, n_end: {n_end}")
    
    if m_start > n_end:
        print("  - Menu already outside nav")
        return False
        
    # Logic to find m_end...
    depth = 0
    m_end = -1
    for i in range(m_start, len(content)):
        if content[i:i+4] == '<div':
            depth += 1
        elif content[i:i+6] == '</div':
            depth -= 1
            if depth == 0:
                m_end = i + 6
                break
    
    if m_end != -1:
        print(f"  - m_end: {m_end}")
        # Move it
        return True
    return False

fix_file(r'd:\security-tools\Four Alpha\alpha-family.html')
