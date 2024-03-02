import logging
import os
import shutil

from file_type import is_markdown_file, is_empty, is_asset_file
from text_utils import fix_escapes, unencode_filenames_for_links, spaces_to_underscore, underscore_to_dash


def get_namespace_hierarchy(file: str, args) -> list[str]:
    """Given a markdown filename (not full path) representing a logseq page, returns a list representing the namespace
    hierarchy for that file
    Eg a file in the namespace "A/B/C" would return ['A', 'B', 'C.md']
    Namespaces are detected as follows ways:
        Splitting by "%2F" in the file name
        Splitting by "___" in the file name if the above is not present
        Splitting by "." in the file name if the above is not present and the --ignore_dot_for_namespaces flag is not present
    """
    split_by_pct = file.split("%2F")
    if len(split_by_pct) > 1:
        return split_by_pct

    split_by_underscores = file.split("___")
    if len(split_by_underscores) > 1:
        return split_by_underscores

    if not args.ignore_dot_for_namespaces:
        split_by_dot = file.split(".")
        split_by_dot[-2] += "." + split_by_dot[-1]
        split_by_dot.pop()
        if len(split_by_dot) > 1:
            return split_by_dot

    return [file]


def copy_attachment(file_path, new_path):
    new_file_dir = os.path.join(new_path, 'attachments')
    file = os.path.basename(file_path)
    new_file = spaces_to_underscore(file)
    new_file_path = os.path.join(new_file_dir, new_file)
    shutil.copyfile(file_path, new_file_path)


def copy_files(old_path: str, new_path: str, args, journals: bool = False):
    new_paths = set()
    new_to_old_paths = {}
    pages_that_were_empty = set()
    old_pagenames_to_new_paths = {}
    for root, dirs, files in os.walk(old_path):
        for file in files:
            file_path = os.path.join(root, file)
            folder = os.path.relpath(root, old_path)
            if os.path.isfile(file_path):
                if is_markdown_file(file_path):
                    if not is_empty(file_path):
                        new_file_dir = new_path
                        if not journals:
                            new_file_dir = os.path.join(new_path, 'pages')
                        hierarchy = get_namespace_hierarchy(file, args)
                        hierarchical_pagename = "/".join(hierarchy)  # ?

                        if folder == '.':
                            new_file_path = os.path.join(new_file_dir, *hierarchy)
                        else:
                            new_file_path = os.path.join(new_file_dir, *([folder] + hierarchy))

                        new_file_path = fix_escapes(new_file_path)
                        new_dirname = os.path.split(new_file_path)[0]
                        os.makedirs(new_dirname, exist_ok=True)
                        if journals:
                            new_file_path = underscore_to_dash(new_file_path)
                        shutil.copyfile(file_path, new_file_path)
                        new_to_old_paths[new_file_path] = file_path
                        new_paths.add(new_file_path)

                        old_pagename = os.path.splitext(hierarchical_pagename)[0]
                        old_pagenames_to_new_paths[old_pagename] = new_file_path

                        if journals:
                            if args.journal_dashes:
                                old_pagenames_to_new_paths[old_pagename.replace("_", "-")] = new_file_path
                        else:
                            old_pagenames_to_new_paths[unencode_filenames_for_links(old_pagename)] = new_file_path
                    else:
                        pages_that_were_empty.add(file)
                elif is_asset_file(file_path):
                    copy_attachment(file_path, new_path)

    return new_paths, new_to_old_paths, pages_that_were_empty, old_pagenames_to_new_paths
