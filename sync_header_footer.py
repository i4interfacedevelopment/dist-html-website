"""
Sync the header and footer from index.html to all other HTML pages.

Strategy:
  - HEADER: Extract everything from <body> open to </header> (inclusive) from index.html.
    In target files, replace from <body> to </header> with the extracted block.
  - FOOTER: Extract <footer ...> ... </footer> from index.html.
    In target files, replace their <footer...>...</footer> block.

Pages to SKIP (they have their own unique structure):
  - index.html  (source)
  - home-*.html (other home variants)
  - error.html, typography.html, cart.html, checkout.html, wishlist.html,
    shop.html, shop-details.html, pricing.html (template-only pages)
"""

import os
import glob
import re

ROOT = os.path.dirname(os.path.abspath(__file__))

SKIP_FILES = {
    'index.html',
    'home-university.html', 'home-university-op.html',
    'home-admission.html', 'home-admission-op.html',
    'home-courses.html', 'home-courses-op.html',
    'error.html', 'typography.html',
    'cart.html', 'checkout.html', 'wishlist.html',
    'shop.html', 'shop-details.html', 'pricing.html',
}

# ── 1. Read index.html ───────────────────────────────────────────────────────

with open(os.path.join(ROOT, 'index.html'), 'r', encoding='utf-8') as f:
    idx = f.read()

# Extract HEADER block: from <body> up to and including </header>
# We look for the opening body tag and everything up to the first </header>
body_open_match = re.search(r'<body\b[^>]*>', idx)
header_close_pos = idx.find('</header>')
assert body_open_match and header_close_pos > 0, "Could not find <body> or </header> in index.html"

# The new header block starts just after <body...> (we keep the body tag itself)
# but we replace everything from <body> to </header> in target files.
NEW_HEADER_FULL = idx[body_open_match.start() : header_close_pos + len('</header>')]

# Extract FOOTER block: from <footer to </footer>
footer_match = re.search(r'<footer\b', idx)
footer_close_pos = idx.find('</footer>')
assert footer_match and footer_close_pos > 0, "Could not find <footer> in index.html"
NEW_FOOTER = idx[footer_match.start() : footer_close_pos + len('</footer>')]

print(f"Header block extracted: {NEW_HEADER_FULL.count(chr(10))+1} lines")
print(f"Footer block extracted: {NEW_FOOTER.count(chr(10))+1} lines")

# ── 2. Process target files ──────────────────────────────────────────────────

html_files = [
    f for f in glob.glob(os.path.join(ROOT, '*.html'))
    if os.path.basename(f) not in SKIP_FILES
]

changed = []
skipped = []

for filepath in sorted(html_files):
    fname = os.path.basename(filepath)
    with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
        content = f.read()

    new_content = content

    # ── Replace HEADER ────────────────────────────────────────────────────────
    # Find <body...> and </header> in the target file
    bm = re.search(r'<body\b[^>]*>', new_content)
    hc = new_content.find('</header>')
    if not bm or hc < 0:
        print(f"  SKIP (no body/header): {fname}")
        skipped.append(fname)
        continue

    old_header = new_content[bm.start() : hc + len('</header>')]
    new_content = new_content[:bm.start()] + NEW_HEADER_FULL + new_content[hc + len('</header>'):]

    # ── Replace FOOTER ────────────────────────────────────────────────────────
    fm = re.search(r'<footer\b', new_content)
    fc_pos = new_content.find('</footer>')
    if fm and fc_pos > 0:
        old_footer = new_content[fm.start() : fc_pos + len('</footer>')]
        new_content = new_content[:fm.start()] + NEW_FOOTER + new_content[fc_pos + len('</footer>'):]
    else:
        print(f"  WARNING: no footer found in {fname}")

    if new_content != content:
        with open(filepath, 'w', encoding='utf-8', newline='') as f:
            f.write(new_content)
        changed.append(fname)
        print(f"  Updated: {fname}")
    else:
        print(f"  Unchanged: {fname}")

print(f"\nDone. {len(changed)} file(s) updated, {len(skipped)} skipped (no header/body).")
