import os


def is_markdown_file(file_path: str) -> bool:
    return file_path.lower().endswith(".md")


def is_asset_file(file_path: str) -> bool:
    return file_path.lower().endswith((".png", ".jpg", ".jpeg", ".gif", ".pdf"))


def is_empty(file_path: str) -> bool:
    """Given a path to a file, checks if it's empty
    A file is empty if it only contains whitespace
    A file containing only front matter / page properties is not empty
    """
    if not is_markdown_file(file_path):
        return False

    with open(file_path, "r", encoding="utf-8", errors="replace") as f:
        lines = f.readlines()
        for line in lines:
            if not line.isspace():
                return False

    return True


def get_markdown_file_properties(file_path: str) -> tuple[dict, int]:
    """Given a path to a markdown file, returns a dictionary of its properties and the index of the first line after the properties

    Properties can either be in page property format: "title:: test"
    Or in front matter format:
        ---
        title: test
        ---
    """

    raise NotImplementedError()
