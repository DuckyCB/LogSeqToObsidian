import re


def is_collapsed_line(line: str) -> bool:
    """Checks if the line is a logseq artefact representing a collapsed block"""
    match = re.match(r"\s*collapsed:: true\s*", line)
    return match is not None


def add_space_after_hyphen_that_ends_line(line: str) -> str:
    """Add a space after a hyphen that ends a line"""
    line = re.sub(r"-$", "- ", line)
    return line


def prepend_code_block(line: str) -> list[str]:
    """Replaces a line starting a code block after a bullet point with two lines,
    so that the code block is displayed correctly in Obsidian

    If this line does not start a code block after a bullet point, then returns an empty list
    """
    out = []

    match = re.match(r"(\t*)-[ *]```(\w+)", line)
    if match is not None:
        tabs = match[1]
        language_name = match[2]
        out.append(tabs + "- " + language_name + " code block below:\n")
        out.append(tabs + "```" + language_name + "\n")
        INSIDE_CODE_BLOCK = True
        # import ipdb; ipdb.set_trace()

    return out


def convert_todos(line: str, inside_code_block: bool) -> str:
    # Not if we're inside a code block
    if inside_code_block:
        return line

    line = re.sub(r"^- DONE", "- [X]", line)
    line = re.sub(r"^- TODO", "- [ ]", line)

    return line
