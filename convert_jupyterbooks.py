import os
import shutil

source_dir = "mybookname/_build/html"
target_dir = "mybookname_html_autoconvert"
base_url = "https://flst01.github.io/"

# 1. Copy the built book to a clean target folder
if os.path.exists(target_dir):
    shutil.rmtree(target_dir)
shutil.copytree(source_dir, target_dir)

# 2. Find and rename all folders whose names start with '_'
underscore_folders = {}  # map old_name -> new_name
for root, dirs, _ in os.walk(target_dir):
    for d in list(dirs):
        if d.startswith("_"):
            old_name = d
            new_name = d[1:]  # drop the leading underscore
            old_path = os.path.join(root, old_name)
            new_path = os.path.join(root, new_name)
            shutil.move(old_path, new_path)
            underscore_folders[old_name] = new_name

# 3. Rewrite HTML files to fix references
#    We replace occurrences like '/_static/' → '/static/' and '"_static/' → '"static/'
for root, _, files in os.walk(target_dir):
    for fn in files:
        if not fn.lower().endswith(".html"):
            continue
        full_path = os.path.join(root, fn)
        with open(full_path, "r", encoding="utf-8") as f:
            text = f.read()

        for old, new in underscore_folders.items():
            # replace URL paths
            text = text.replace(f'/{old}/', f'/{new}/')
            # replace references in quotes/apostrophes
            text = text.replace(f'"{old}/', f'"{new}/')
            text = text.replace(f"'{old}/", f"'{new}/")
        text = text.replace('<a class="navbar-brand logo" href="#">',
                            f'<a class="navbar-brand logo" href="{base_url}">')
        text = text.replace('<a class="navbar-brand logo" href="intro.html">',
                            f'<a class="reference internal" href="{base_url}">')

        # write back only if changed
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(text)
