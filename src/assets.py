import os
import re
import shutil


def update_assets(line: str, old_path: str, new_path: str):
    """Updates embedded asset links and copies the asset
    Assets are copied to the 'attachments' subfolder under the same directory as new_path is in
    Images (.PNG, .JPG) are embedded. Everything else is linked to
    """

    def fix_asset_embed(match: re.Match) -> str:
        out = []
        name = match[1]
        old_relpath = match[2]
        if old_relpath[:8] == "file:///":
            old_relpath = old_relpath[7:]

        old_relpath = old_relpath.replace("%20", " ")

        old_asset_path = os.path.normpath(
            os.path.join(os.path.dirname(old_path), old_relpath)
        )
        new_asset_path = os.path.join(
            os.path.dirname(new_path), "attachments", os.path.basename(old_asset_path)
        )
        new_asset_dir = os.path.dirname(new_asset_path)
        os.makedirs(new_asset_dir, exist_ok=True)
        print("Old note path: " + old_path)
        print("Old asset path: " + old_asset_path)
        print("New asset path: " + new_asset_path)
        try:
            shutil.copyfile(old_asset_path, new_asset_path)
            new_relpath = os.path.relpath(new_asset_path, os.path.dirname(new_path))
        except FileNotFoundError:
            print(
                "Warning: copying the asset from "
                + old_asset_path
                + " to "
                + new_asset_path
                + " failed, skipping it"
            )
            new_relpath = old_relpath
            # import ipdb; ipdb.set_trace()

        if os.path.splitext(old_asset_path)[1].lower() in [".png", ".jpg", ".jpeg", ".gif"]:
            out.append("!")
        out.append("[" + name + "]")
        out.append("(" + new_relpath + ")")

        return "".join(out)

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
