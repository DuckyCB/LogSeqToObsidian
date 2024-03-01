import os
import re
import shutil

from text_utils import spaces_to_underscore


def update_assets(line: str):
    """Updates embedded asset links
    Assets are copied to the 'attachments' subfolder under the same directory as new_path is in
    Images (.PNG, .JPG) are embedded. Everything else is linked to
    """

    def fix_asset_embed(match: re.Match) -> str:
        name = match[1]
        file_name = match[2]
        if file_name[:8] == "file:///":
            file_name = file_name[7:]
        file_name = os.path.basename(file_name)
        file_name = spaces_to_underscore(file_name)

        return "![" + name + "](attachments/" + file_name + ")"

    line = re.sub(r"!\[(.*?)]\((.*?)\)", fix_asset_embed, line)

    return line


def update_image_dimensions(line: str) -> str:
    """Updates the dimensions of embedded images with custom height/width specified
    Eg from ![image.png](image.png){:height 319, :width 568}
        to ![image.png|568](image.png)
    """

    def fix_image_dim(match):
        return "![" + match[1] + "|" + match[3] + "](" + match[2] + ")"

    line = re.sub(r"!\[(.*?)]\((.*?)\){:height \d*, :width (\d*)}", fix_image_dim, line)

    return line


def add_bullet_before_indented_image(line: str) -> str:
    """If an image has been embedded on a new line created after shift+enter, it won't be indented in Obsidian"""

    def add_bullet(match):
        return match[1] + "- " + match[2]

    line = re.sub(r"^(\t+)(!\[.*$)", add_bullet, line)
    return line
