import re


def convert_spaces_to_tabs(line: str) -> str:
    """Converts 2-4 spaces to a tab"""
    line = re.sub(r" {2,4}", "\t", line)
    return line


def convert_empty_line(line: str) -> str:
    """An empty line in logseq still starts with a hyphen"""
    line = re.sub(r"^- *$", "", line)
    return line


def escape_lt_gt(line: str, inside_code_block: bool) -> str:
    """Escapes < and > characters"""
    # Not if we're inside a code block
    if inside_code_block:
        return line

    # Replace < and > with \< and \> respectively, but only if they're not at the start of the line
    line = re.sub(r"(?<!^)<", r"\<", line)
    line = re.sub(r"(?<!^)>", r"\>", line)

    return line


def unindent_once(line: str) -> str:
    """Returns the line after removing one level of indentation"""
    # If it starts with a tab, we can just remove it
    if line.startswith("\t"):
        return line[1:]

    # If it starts with a "- ", we can remove that
    if line.startswith("- "):
        return line[2:]

    return line


def fix_escapes(old_str: str) -> str:
    """Given a filename, replace url escaped characters with an acceptable character for Obsidian filenames

    :arg old_str old string
    """
    if old_str.find("%") < 0:
        return old_str

    replace_map = {
        "%3A": ".",
    }

    new_str = old_str

    for escape_str in replace_map:
        if new_str.find(escape_str) >= 0:
            new_str = new_str.replace(escape_str, replace_map[escape_str])

    return new_str


def unencode_filenames_for_links(old_str: str) -> str:
    """Given a filename, replace url escaped characters with the normal character as it would appear in a link

    :arg old_str old value
    """
    if old_str.find("%") < 0:
        return old_str

    replace_map = {
        "%3A": ":",
    }

    new_str = old_str

    for escape_str in replace_map:
        if new_str.find(escape_str) >= 0:
            new_str = new_str.replace(escape_str, replace_map[escape_str])

    return new_str
