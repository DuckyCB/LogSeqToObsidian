import os
import re


def is_markdown_file(file_path: str) -> bool:
    return file_path.lower().endswith(".md")


def is_asset_file(file_path: str) -> bool:
    return file_path.lower().endswith((".png", ".jpg", ".jpeg", ".gif", ".pdf", ".heic"))


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


def is_daily_file(path):
    """Check if the given path corresponds to a daily entry.
    """
    if "daily" not in path.split(os.sep):
        return False

    filename = os.path.basename(path)
    pattern = r"\d{4}-\d{2}-\d{2}\.md"

    return bool(re.match(pattern, filename))
