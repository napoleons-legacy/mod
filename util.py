import os
from typing import Callable, List

MOD_DIRECTORY = "Napoleon's Legacy"


def is_good_ext(extensions: List[str]) -> Callable[[str], bool]:
    """Verify that the file_name has a valid file extension
    :param file_name: The name of the file
    :type file_name: str
    """

    endings = ["." + s for s in extensions]

    def func(file_name: str) -> bool:
        return any([good for good in endings if file_name.endswith(good)])

    return func


def process_directory(directory: str, extensions: List[str], handler: Callable[[str], None]) -> None:
    for dirpath, dirnames, file_names in os.walk(directory):
        for name in filter(is_good_ext(extensions), file_names):
            file_path = os.path.join(dirpath, name)
            handler(file_path)
