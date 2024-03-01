import re


def update_links_and_tags(line: str, name_to_path: dict, curr_path: str) -> str:
    """Given a line of a logseq page, updates any links and tags in it

    :arg curr_path Absolute path of the current file, needed so that links can be replaced with relative paths
    """
    # First replace [[Aug 24th, 2022] with [[2022-08-24]]
    # This will stop the comma breaking tags
    month_map = {
        "Jan": "01",
        "Feb": "02",
        "Mar": "03",
        "Apr": "04",
        "May": "05",
        "Jun": "06",
        "Jul": "07",
        "Aug": "08",
        "Sep": "09",
        "Oct": "10",
        "Nov": "11",
        "Dec": "12",
    }

    def reformat_dates_in_links(match: re.Match):
        month = match[1]
        date = match[2]
        year = match[4]

        if len(date) == 1:
            date = "0" + date

        return "[[" + year + "-" + month_map[month] + "-" + date + "]]"

    line = re.sub(
        r"\[\[(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\b (\d{1,2})(st|nd|rd|th), (\d{4})]]",
        reformat_dates_in_links,
        line,
    )

    # Replace #[[this type of tag]] with #this_type_of_tag or [[this type of tag]] depending on args.convert_tags_to_links
    def fix_long_tag(match: re.Match):
        s = match[0]
        s = s.replace("#", "")
        # if args.convert_tags_to_links:
        #     s = s.replace("#","")
        # else:
        #     s = s.replace(" ", "_")
        #     s = s.replace("[", "")
        #     s = s.replace("]", "")
        return s

    line = re.sub(r"#\[\[.*?]]", fix_long_tag, line)

    # Convert a 'short' #tag to a [[tag]] link, if args.convert_tags_to_links is true
    # def convert_tag_to_link(match: re.Match):
    #     s = match[0]
    #     if args.convert_tags_to_links:
    #         s = s.replace("#","")
    #         s = "[[{}]]".format(s)
    #     return s

    # line = re.sub(r"#\w+", convert_tag_to_link, line)

    # Replace [[This/Type/OfLink]] with [OfLink](../Type/OfLink) - for example
    # def fix_link(match: re.Match):
    #     s = match[0]
    #     s = s.replace("[", "")
    #     s = s.replace("]", "")

    #     # Or make it a tag if the page doesn't exist
    #     if s not in name_to_path:
    #         if args.convert_tags_to_links:
    #             s = s.replace(":", ".")
    #             return "[[" + s + "]]"
    #         else:
    #             s = "#" + s
    #             s = s.replace(" ", "_")
    #             s = s.replace(",", "_")
    #             return s
    #     else:
    #         new_file_path = name_to_path[s]
    #         relpath = os.path.relpath(new_file_path, os.path.dirname(curr_path))
    #         relpath.replace(" ", "%20")  # Obsidian does this
    #         relpath = fix_escapes(relpath)
    #         name = s.split("/")[-1]
    #         s = "[" + name + "](" + relpath + ")"  # TOFIX We return the []() format of link here rather than [[]] format which we do elsewhere
    #         return s

    # line = re.sub(r"\[\[.*?]]", fix_link, line)

    return line


def remove_block_links_embeds(line: str) -> str:
    """Returns the line stripped of any block links or embeddings"""
    line = re.sub(r"{{embed .*?}}", "", line)
    line = re.sub(r"\(\(.*?\)\)", "", line)
    return line
