import re


def get_front_matter(lines):
    front_matter = {}
    first_line_after_front_matter = 0
    for idx, line in enumerate(lines):
        match = re.match(r"(.*?)::[\s]*(.*)", line)
        if match is not None:
            front_matter[match[1]] = match[2]
            first_line_after_front_matter = idx + 1
        else:
            break
    return front_matter, first_line_after_front_matter


def create_front_matter(first_line, newlines):
    pattern = r'^#(\S+\s)*#?$'
    if bool(re.match(pattern, first_line)):
        tags = first_line.split()
        newlines.append("---\n")
        newlines.append("tags:\n")
        for tag in tags:
            clean_tag = tag.replace("#", "")
            newlines.append('  - ' + clean_tag + "\n")
        newlines.append("---\n")
        return True
    return False


def front_matter_conversion(newlines, front_matter):
    newlines.append("---\n")
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
            newlines.append("aliases:\n")
            aliases = front_matter[key].split(",")
            for alias in aliases:
                newlines.append('  - ' + alias.strip() + "\n")
        elif key.lower().find("description") >= 0:
            new_taglinks.extend(re.findall(r'\[\[(.*?)\]\]', front_matter[key]))
            clean_line = front_matter[key].replace("#", "").replace("[[", "").replace("]]", "")
            newlines.append(key + ": " + clean_line + "\n")
        elif key.lower() == "author" or key.lower() == "origin":
            newlines.append(f"{key.lower()}:\n")
            options = front_matter[key].split(",")
            for option in options:
                newlines.append('  - "' + option + '"' + "\n")
        else:
            newlines.append(key + ": " + front_matter[key] + "\n")
    if len(new_taglinks) > 0:
        newlines.append("taglinks:\n")
        for taglink in new_taglinks:
            newlines.append('  - "[[' + taglink + ']]"' + "\n")
    newlines.append("---\n")
