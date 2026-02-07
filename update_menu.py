import os
import re

files = [
    "index.html", "about.html", "milestones.html", "admission.html", 
    "location.html", "library.html", "contact.html", "dept_cs.html", 
    "dept_management.html", "dept_commerce.html", "dept_social_work.html", 
    "dept_media.html", "dept_english.html", "dept_psychology.html", 
    "dept_hospitality.html", "placement.html", "iqac.html", 
    "alumni.html", "sports.html"
]

menu_items = """
    <ul>
        <li><a href="index.html">Home</a></li>
        <li class="menu-item-has-children">
            <a href="#">About Us</a>
            <ul class="sub-menu">
                <li><a href="about.html">About DiST</a></li>
                <li><a href="milestones.html">Milestones</a></li>
                <li><a href="iqac.html">IQAC</a></li>
                <li><a href="alumni.html">Alumni</a></li>
            </ul>
        </li>
        <li class="menu-item-has-children">
            <a href="#">Academics</a>
            <ul class="sub-menu">
                <li><a href="dept_cs.html">School of Computer Science</a></li>
                <li><a href="dept_management.html">School of Management</a></li>
                <li><a href="dept_commerce.html">School of Commerce</a></li>
                <li><a href="dept_social_work.html">School of Social Work</a></li>
                <li><a href="dept_media.html">School of Media & Communication</a></li>
                <li><a href="dept_english.html">School of English</a></li>
                <li><a href="dept_psychology.html">School of Behavioral Sciences</a></li>
                <li><a href="dept_hospitality.html">School of Hospitality</a></li>
                <li><a href="library.html">Library</a></li>
            </ul>
        </li>
        <li class="menu-item-has-children">
            <a href="#">Admission</a>
            <ul class="sub-menu">
                <li><a href="admission.html">Admission Home</a></li>
                <li><a href="location.html">Location & Ambiance</a></li>
            </ul>
        </li>
        <li><a href="placement.html">Placement</a></li>
        <li><a href="sports.html">Sports</a></li>
        <li><a href="contact.html">Contact Us</a></li>
    </ul>
"""

# Clean up indentation for replacement
menu_items = menu_items.strip()

for f in files:
    path = os.path.abspath(f)
    if not os.path.exists(path):
        print(f"Skipping {path} (not found)")
        continue
    
    with open(path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # 1. Update Main Menu
    # Regex to capture content inside <nav class="main-menu">... <ul>...</ul> ... </nav>
    # We target the <ul ...> ... </ul> block inside nav
    # The template has <nav class="main-menu"><ul>...</ul></nav> usually.
    
    # Regex: Look for <nav class="main-menu">, then any whitespace, then <ul...>, then content, then </ul>, then anything, then </nav>
    # Actually, simpler: replace everything between <nav class="main-menu"> and </nav> with the new <ul> wrapped content?
    # No, sometimes there might be other things? Usually not in this template.
    # index.html has: <nav class="main-menu"> <ul> ... </ul> </nav>
    
    # Regex: Look for <nav class="...main-menu..."> (allow extra classes)
    # matching <nav ... class="...main-menu..." ...> is tricky with simple regex if we don't know attribute order.
    # But usually it's class="main-menu ...".
    # We'll use a broad pattern: <nav [^>]*main-menu[^>]*> ... </nav>
    
    new_main_nav_content = f'<nav class="main-menu d-none d-xl-block">\n                                {menu_items}\n                            </nav>'
    
    # We want to preserve the original class if possible, but for now let's just force the class that index.html uses + standard ones.
    # Or better: capture the opening tag, and replace content.
    
    content = re.sub(
        r'(<nav[^>]*main-menu[^>]*>).*?(</nav>)', 
        r'\1' + menu_items + r'\2', 
        content, 
        flags=re.DOTALL
    )
    
    # 2. Update Mobile Menu
    # <div class="th-mobile-menu"> ... </div>
    
    content = re.sub(
        r'(<div class="th-mobile-menu">).*?(</div>)', 
        r'\1' + menu_items + r'\2', 
        content, 
        flags=re.DOTALL
    )

    with open(path, 'w', encoding='utf-8') as file:
        file.write(content)
    print(f"Updated {f}")
