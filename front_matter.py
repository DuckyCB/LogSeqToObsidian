import re


def get_front_matter(lines):
    front_matter = {}
    first_line_after_front_matter = 0
    loose_tags_match = re.findall(r'#\w+', lines[0])
    if len(loose_tags_match) > 0:
        front_matter["tags::"] = lines[0]
        first_line_after_front_matter += 1
    for idx, line in enumerate(lines):
        match = re.match(r"(.*?)::[\s]*(.*)", line)
        if match is not None:
            front_matter[match[1]] = match[2]
            first_line_after_front_matter = idx + 1
        else:
            break
    return front_matter, first_line_after_front_matter


def front_matter_list(newlines, title, list, taglink=False):
    newlines.append(f"{title}:\n")
    for item in list:
        if taglink:
            newlines.append(f'  - "[[{item.strip()}]]"\n')
        else:
            newlines.append(f'  - "{item.strip()}"\n')


def add_timestamps(newlines, created, edited):
    newlines.append(f"created: {created}\n")
    newlines.append(f"edited: {edited}\n")


def front_matter_conversion(newlines, front_matter, created, edited, is_daily):
    newlines.append("---\n")
    if not is_daily:
        if bool(front_matter):
            new_taglinks = []
            for key in front_matter:
                if key.lower().find("tags") >= 0:
                    # convert tags:: value1 #[[value 2]] #value3 [[value4]]
                    # to
                    # tags:
                    #   - value1
                    #   - value3
                    # taglinks:
                    #   - "[[value 2]]"
                    #   - "[[value4]]"
                    # tags = front_matter[key].split(",")
                    tags = re.findall(r'\[\[.*?]]|#(?:\[\[.*?]]|\S+)(?:,)?|\S+', front_matter[key])
                    tags = [tag.replace("#", "") for tag in tags]

                    new_tags = []
                    for tag in tags:
                        if "[[" not in tag:
                            tag = tag.strip()
                            clean_tag = tag.replace("#", "")
                            new_tags.append('  - ' + clean_tag + "\n")
                        else:
                            tag = tag.strip()
                            clean_tag = tag.replace("#", "")
                            clean_tag = clean_tag.replace("[[", "")
                            clean_tag = clean_tag.replace("]]", "")
                            new_taglinks.append(clean_tag)

                    if len(new_tags) > 0:
                        newlines.append("tags:\n")
                        for tag in new_tags:
                            newlines.append(tag)

                elif key.lower().find("alias") >= 0:
                    front_matter_list(newlines, "aliases", front_matter[key].split(","))
                elif key.lower().find("description") >= 0:
                    new_taglinks.extend(re.findall(r'\[\[(.*?)\]\]', front_matter[key]))
                    clean_line = front_matter[key].replace("#", "").replace("[[", "").replace("]]", "")
                    newlines.append(key + ": " + clean_line + "\n")
                elif key.lower() == "author" or key.lower() == "origin":
                    front_matter_list(newlines, key.lower(), front_matter[key].split(","), taglink=True)
                else:
                    newlines.append(key + ": " + front_matter[key] + "\n")
            if len(new_taglinks) > 0:
                front_matter_list(newlines, "taglinks", new_taglinks, taglink=True)
    else:
        front_matter_list(newlines, "tags", ["daily"])
    add_timestamps(newlines, created, edited)
    newlines.append("---\n")


def get_markdown_file_properties(file_path: str) -> tuple[dict, int]:
    """Given a path to a markdown file, returns a dictionary of its properties and the index of the first line after the properties

    Properties can either be in page property format: "title:: test"
    Or in front matter format:
        ---
        title: test
        ---
    """

    raise NotImplementedError()
