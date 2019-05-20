import os
from typing import List

MOD_DIRECTORY = "Napoleon's Legacy"
EXTENSIONS = ["txt", "lua", "map", "csv"]


def clean_line(line: str) -> str:
    """Clean a line by removing useless information and following one standard.
    :param line: A line of text
    :type line: str
    :returns: str -- The cleaner line
    """

    return line.replace(b"\t", b"    ").rstrip() + b"\n"


def clean_file(filepath: str) -> bool:
    """Clean the entire file by replacing tabs with spaces,
    replacing Windows line endings with Unix line endings,
    and removing trailing whitespace. We also adjust the file
    such that it follows style rules.

    :param filepath: The path of the file
    :type filepath: str
    :returns: bool -- Whether the file was changed or not
    """

    file_changed = False
    with open(filepath, "r+b") as file:
        lines = file.readlines()
        for index, line in enumerate(lines):
            cleaned = clean_line(line)
            if cleaned.isspace():
                cleaned = b"\n"

            if cleaned != line:
                file_changed = True

            lines[index] = cleaned

        # check for more style things
        style_changed = clean_style(lines)

        if style_changed:
            file_changed = True

        # wipe the file and rewrite
        file.seek(0)
        file.truncate()
        file.writelines(lines)

        return file_changed


def clean_style(lines: List[str]) -> bool:
    """Adjust the file information to be stylistically cleaner
    :param lines: The file contents
    :type lines: List[str]
    :returns: bool -- Whether the styling rules were used or not
    """

    style_changed = False

    # remove any extra newlines at the start of the file
    while lines and lines[0].isspace():
        del lines[0]
        style_changed = True

    # remove any extra newlines at the end of the file.
    while lines and lines[-1].isspace():
        del lines[-1]
        style_changed = True

    # add a newline to the end of the file if not exists.
    if lines and not lines[-1].endswith(b"\n"):
        lines[-1] += "\n"
        style_changed = True

    return style_changed


def good_ext(filename: str) -> bool:
    """Verify that the filename has a valid file extension
    :param filename: The name of the file
    :type filename: str
    """

    exts = ["." + s for s in EXTENSIONS]
    return any([good for good in exts if filename.endswith(good)])


if __name__ == '__main__':
    none_changed = True
    change_count = 0

    for dirpath, dirnames, filenames in os.walk(MOD_DIRECTORY):
        for name in filter(good_ext, filenames):
            filepath = os.path.join(dirpath, name)
            cleaned = clean_file(filepath)
            if cleaned:
                print(f"Cleaned {filepath}")
                none_changed = False
                change_count += 1

    if none_changed:
        print("No files were changed.")
    else:
        print(f"{change_count} files were changed.")
