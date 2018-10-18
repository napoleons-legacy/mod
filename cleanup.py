import os
from typing import List

MOD_DIRECTORY = "Napoleon's Legacy"

def clean_line(line: str) -> str:
    """Clean a line by removing useless information and following one standard.
    :param line: A line of text
    :type line: str
    :returns: str -- The cleaner line
    """

    return line.replace("\t", "    ").replace("\r\n", "\n").rstrip("\t ")

def clean_file(filepath: str) -> None:
    """Clean the entire file by replacing tabs with spaces,
    replacing Windows line endings with Unix line endings,
    and removing trailing whitespace. We also adjust the file
    such that it follows style rules.

    :param filepath: The path of the file
    :type filepath: str
    """

    with open(filepath, "r+", encoding="ISO-8859-1") as file:
        lines = file.readlines()
        for index, line in enumerate(lines):
            cleaned = clean_line(line)
            if cleaned.isspace():
                cleaned = "\n"

            lines[index] = cleaned

        # check for more style things
        clean_style(lines)

        # wipe the file and rewrite
        file.seek(0)
        file.truncate()
        file.writelines(lines)

def clean_style(lines: List[str]) -> None:
    """Adjust the file information to be stylistically cleaner
    :param lines: The file contents
    :type lines: List[str]
    """

    # remove any extra newlines at the start of the file
    while lines and lines[0].isspace():
        del lines[0]

    # remove any extra newlines at the end of the file.
    while lines and lines[-1].isspace():
        del lines[-1]

    # add a newline to the end of the file if not exists.
    if lines and not lines[-1].endswith("\n"):
        lines[-1] = lines[-1] + "\n"

def good_ext(filename: str) -> bool:
    """Verify that the filename has a valid file extension
    :param filename: The name of the file
    :type filename: str
    """

    exts = ("." + s for s in ["txt", "lua", "map", "csv"])
    return any([good for good in exts if filename.endswith(good)])

if __name__ == '__main__':
    for dirpath, dirnames, filenames in os.walk(MOD_DIRECTORY):
        for name in filter(good_ext, filenames):
            filepath = os.path.join(dirpath, name)
            print(f"Cleaning {filepath}")
            clean_file(filepath)
