import os
import re

def replace_logos(directory):
    # Regex pattern to match various logo src attributes
    # We want to match src="assets/img/logo..." but NOT "assets/img/logohead.jpg" if it's already there
    # The user wants to replace:
    # assets/img/logo-smol.png
    # assets/img/logo.svg
    # assets/img/light-white-logo.svg
    # assets/img/logo-icon.svg
    # assets/img/logo2.svg
    
    # We can match any src ending in these filenames.
    
    files_updated = 0
    
    # Walk through directory
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".html"):
                filepath = os.path.join(root, file)
                
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # List of specific logos to replace
                logos_to_replace = [
                    'assets/img/logo-smol.png',
                    'assets/img/logo.svg',
                    'assets/img/light-white-logo.svg',
                    'assets/img/logo-icon.svg',
                    'assets/img/logo2.svg'
                ]
                
                new_content = content
                replaced = False
                
                for logo in logos_to_replace:
                    if logo in new_content:
                        new_content = new_content.replace(logo, 'assets/img/logohead.jpg')
                        replaced = True
                
                # Also generic regex for safety if exact matches fail but structure is similar? 
                # No, stick to explicit replacements to avoid breaking things.
                
                if replaced:
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    print(f"Updated logos in: {file}")
                    files_updated += 1
                    
    print(f"Total files updated: {files_updated}")

if __name__ == "__main__":
    current_dir = os.getcwd()
    print(f"Scanning {current_dir} for logo updates...")
    replace_logos(current_dir)
