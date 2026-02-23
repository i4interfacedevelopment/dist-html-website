"""
Update department/school names across all HTML files in the dist-html-website project.

Changes:
 - "School of Computer Science" → "School of Computer"
 - "School of English"         → "School of Languages"
 - "School of Hospitality"     → "School of Hospitality and Tourism Management"
 - "School of Media & Communication" → "School of Media and Communication"
   (only the display name; href="dept_media.html" stays the same)
"""

import os
import glob

replacements = [
    # (old_text, new_text)
    # Order matters: longest / most specific first
    ("School of Hospitality and Tourism Management", "School of Hospitality and Tourism Management"),  # already correct – no-op guard
    ("School of Computer Science", "School of Computer"),
    ("School of English", "School of Languages"),
    # Hospitality short form → full name (must come AFTER the long form guard above)
    ("School of Hospitality &amp; Tourism Management", "School of Hospitality and Tourism Management"),
    ("School of Hospitality", "School of Hospitality and Tourism Management"),
    # Media & Communication: HTML-encoded ampersand variant
    ("School of Media &amp; Communication", "School of Media and Communication"),
    ("School of Media & Communication", "School of Media and Communication"),
]

root = os.path.dirname(os.path.abspath(__file__))
html_files = glob.glob(os.path.join(root, "*.html"))

changed_files = []

for filepath in html_files:
    with open(filepath, "r", encoding="utf-8", errors="replace") as f:
        content = f.read()

    new_content = content
    for old, new in replacements:
        new_content = new_content.replace(old, new)

    if new_content != content:
        with open(filepath, "w", encoding="utf-8", newline="") as f:
            f.write(new_content)
        changed_files.append(os.path.basename(filepath))
        print(f"  Updated: {os.path.basename(filepath)}")

print(f"\nDone. {len(changed_files)} file(s) updated.")
