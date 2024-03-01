import logging
import os
import shutil

from src.assets import update_assets, update_image_dimensions, add_bullet_before_indented_image
from src.copy_files import copy_files
from src.front_matter import front_matter_conversion, get_front_matter, create_front_matter
from src.links import update_links_and_tags, remove_block_links_embeds
from src.parser import get_parser
from src.text_utils import convert_spaces_to_tabs, convert_empty_line, escape_lt_gt, unindent_once
from src.utils import is_collapsed_line, add_space_after_hyphen_that_ends_line, prepend_code_block, convert_todos

logging.basicConfig(level=logging.INFO, format="%(levelname)s:%(message)s")

# Global state isn't always bad mmkay
ORIGINAL_LINE = ""
INSIDE_CODE_BLOCK = False

parser = get_parser()
args = parser.parse_args()

old_base = args.logseq
new_base = args.output

# First loop: copy files to their new location, populate the maps and list of paths

if not os.path.exists(old_base) or not os.path.isdir(old_base):
    raise ValueError(f"The directory '{old_base}' does not exist or is not a valid directory.")

if args.overwrite_output and os.path.exists(new_base):
    shutil.rmtree(new_base)

os.makedirs(new_base, exist_ok=False)

# Copy journals pages to their own subfolder
old_journals = os.path.join(old_base, "journals")
assert os.path.isdir(old_journals)

new_journals = os.path.join(new_base, "journals")
os.mkdir(new_journals)

logging.info("Now beginning to copy the journal pages")
new_paths, new_to_old_paths, pages_that_were_empty, old_pagenames_to_new_paths = copy_files(old_journals, new_journals,
                                                                                            args, journals=True)

# Copy other markdown files to the new base folder, creating subfolders for namespaces
old_pages = os.path.join(old_base, "pages")
assert os.path.isdir(old_pages)

logging.info("Now beginning to copy the pages")
new_paths_p, new_to_old_paths_p, pages_that_were_empty_p, old_pagenames_to_new_paths_p = copy_files(old_pages,
                                                                                                    new_base, args)
new_paths.update(new_paths_p)
new_to_old_paths.update(new_to_old_paths_p)
pages_that_were_empty.update(pages_that_were_empty_p)
old_pagenames_to_new_paths.update(old_pagenames_to_new_paths_p)

# Second loop: for each new file, reformat its content appropriately
for file_path in new_paths:
    newlines = []
    with open(file_path, "r", encoding="utf-8", errors="replace") as f:
        lines = f.readlines()

        # First replace the 'title:: my note' style of front matter with the Obsidian style (triple dashed)
        front_matter, first_line_after_front_matter = get_front_matter(lines)
        if bool(front_matter):
            # import ipdb; ipdb.set_trace()
            front_matter_conversion(newlines, front_matter)
        else:
            has_front_matter = create_front_matter(lines[0], newlines)
            if has_front_matter:
                first_line_after_front_matter += 1

        for line in lines[first_line_after_front_matter:]:
            ORIGINAL_LINE = line

            # Update global state if this is the end of a code block
            if INSIDE_CODE_BLOCK and line == "```\n":
                INSIDE_CODE_BLOCK = False

            # Ignore if the line if it's a collapsed:: true line
            if is_collapsed_line(line):
                continue

            # Convert empty lines in logseq to empty lines in Obsidian
            line = convert_empty_line(line)

            # Convert 2-4 spaces to a tab
            line = convert_spaces_to_tabs(line)

            # Unindent once if the user requested it
            if args.unindent_once:
                line = unindent_once(line)

            # Add a line above the start of a code block in a list
            lines = prepend_code_block(line)
            if len(lines) > 0:
                newlines.append(lines[0])
                line = lines[1]

            # Update links and tags
            line = update_links_and_tags(line, old_pagenames_to_new_paths, file_path)

            # Update assets
            line = update_assets(line, new_to_old_paths[file_path], file_path)

            # Update image dimensions
            line = update_image_dimensions(line)

            # Remove block links and embeds
            line = remove_block_links_embeds(line)

            # Self-explanatory
            line = add_space_after_hyphen_that_ends_line(line)

            # Self-explanatory
            line = convert_todos(line, INSIDE_CODE_BLOCK)

            # < and > need to be escaped to show up as normal characters in Obsidian
            line = escape_lt_gt(line, INSIDE_CODE_BLOCK)

            # Make sure images are indented correctly
            line = add_bullet_before_indented_image(line)

            newlines.append(line)

    with open(file_path, "w", encoding="utf-8") as f:
        f.writelines(newlines)
