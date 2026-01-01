import os
import re
from pathlib import Path

def generate_folder_structure(tree_text, base_path="."):
    """
    Parses a text-based tree structure and creates folders/files.
    """
    lines = [line for line in tree_text.strip().split('\n') if line.strip()]
    
    # Stack to keep track of the current path context: [(indent_level, path_object)]
    # We start with indent -1 so the root item (indent 0) is always treated as a child of base_path
    stack = [(-1, Path(base_path))]

    print(f"🚀 Starting generation in: {os.path.abspath(base_path)}\n")

    for line in lines:
        # 1. Calculate indentation level based on visual characters
        # We look for the start of the actual name. 
        # The regex looks for the last occurrence of tree characters or whitespace at the start.
        match = re.match(r"^([│\s├──└──]*)", line)
        prefix = match.group(1) if match else ""
        indent_level = len(prefix)

        # 2. Extract the actual name
        raw_name = line[len(prefix):].strip()
        
        # Skip empty lines if any slipped through
        if not raw_name:
            continue

        # 3. Determine if it is a folder or file
        # Convention: If it ends with '/', it's a folder. 
        # (We also remove the trailing slash for the path creation)
        is_folder = raw_name.endswith('/')
        clean_name = raw_name.rstrip('/')

        # 4. Adjust the stack to find the correct parent
        # Pop items from stack while the current item is not deeper than the top of stack
        while stack and stack[-1][0] >= indent_level:
            stack.pop()

        # The current parent is now at the top of the stack
        parent_path = stack[-1][1]
        current_path = parent_path / clean_name

        # 5. Create the Item
        if is_folder:
            try:
                os.makedirs(current_path, exist_ok=True)
                print(f"📁 Created Dir:  {current_path}")
                # Push this new folder onto the stack as a potential parent
                stack.append((indent_level, current_path))
            except OSError as e:
                print(f"❌ Error creating dir {current_path}: {e}")
        else:
            try:
                # Create parent dir if it doesn't exist (just in case)
                os.makedirs(current_path.parent, exist_ok=True)
                # Create an empty file
                with open(current_path, 'w', encoding='utf-8') as f:
                    pass
                print(f"📄 Created File: {current_path}")
            except OSError as e:
                print(f"❌ Error creating file {current_path}: {e}")

    print("\n✨ Structure generation complete.")

# ==========================================
# PASTE YOUR TREE STRUCTURE BETWEEN QUOTES
# ==========================================
tree_structure = r"""
vidflow/
├── vidflow/
│   ├── __init__.py
│   ├── video.py
│   ├── ffmpeg.py
│   ├── transcript.py
│   ├── captions.py
│   ├── presets/
│   │   ├── __init__.py
│   │   ├── registry.py
│   │   ├── loader.py
│   │   ├── schemas.py
│   │   └── styles.yaml
│   ├── config/
│   │   └── loader.py
│   └── cli.py
│
├── presets/
│   ├── shorts.yaml
│   ├── podcast_video.yaml
│   ├── course.yaml
│   ├── captioned.yaml
│   ├── viral_clips.yaml
│   ├── before_after.yaml
│   └── faceless.yaml
│
├── examples/
│   └── README.md
│
├── docs/
│   └── presets/
│       ├── shorts.md
│       ├── podcast_video.md
│       ├── course.md
│       ├── captioned.md
│       ├── viral_clips.md
│       ├── before_after.md
│       └── faceless.md
│
├── pyproject.toml
└── README.md
"""

if __name__ == "__main__":
    # You can change "." to a specific path like "C:/Projects/"
    generate_folder_structure(tree_structure, base_path=".")
