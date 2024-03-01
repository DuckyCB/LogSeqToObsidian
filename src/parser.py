import argparse


def get_parser():
    parser = argparse.ArgumentParser()

    parser.add_argument("--logseq", help="base directory of logseq graph", required=True)
    parser.add_argument(
        "--output", help="base directory where output should go", required=True
    )
    parser.add_argument(
        "--overwrite_output",
        dest="overwrite_output",
        default=False,
        action="store_true",
        help="overwrites output directory if included",
    )
    parser.add_argument(
        "--unindent_once",
        default=False,
        action="store_true",
        help="unindents all lines once - lines at the highest level will have their bullet point removed",
    )
    parser.add_argument(
        "--journal_dashes",
        default=False,
        action="store_true",
        help="use dashes in daily journal - e.g. 2023-12-03.md",
    )
    parser.add_argument(
        "--tag_prop_to_taglist",
        default=False,
        action="store_true",
        help="convert tags in tags:: property to a list of tags in front matter",
    )
    parser.add_argument(
        "--ignore_dot_for_namespaces",
        default=False,
        action="store_true",
        help="ignore the use of '.' as a namespace character",
    )
    parser.add_argument(
        "--convert_tags_to_links",
        default=False,
        action="store_true",
        help="Convert #[[long tags]] to [[long tags]]",
    )
    return parser
