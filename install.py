import shutil
import sys
from os import path

from util import MOD_DIRECTORY, MOD_FILE

MACOS_FOLDER_PATH = path.expanduser(
    "~/Library/Containers/com.vpltd.Victoria2HeartOfDarkness/Data/Library/Application Support/com.vpltd.Victoria2HeartOfDarkness-MAS/mod")
WINDOWS_FOLDER_PATH = "C:\Program Files (x86)\Steam\SteamApps\common\Victoria 2\mod"


def install_mod(folder: str) -> None:
    """Install the mod into the game folder."""

    mod_directory_path = path.join(folder, MOD_DIRECTORY)
    mod_file_path = path.join(folder, MOD_FILE)

    print(f"Deleting {mod_directory_path}.")
    shutil.rmtree(mod_directory_path, ignore_errors=True)

    print(f"Deleting {mod_file_path}.")
    shutil.rmtree(mod_file_path, ignore_errors=True)

    print(f"Copying {MOD_DIRECTORY} into {mod_directory_path}.")
    shutil.copytree(MOD_DIRECTORY, mod_directory_path)

    print(f"Copying {MOD_FILE} into {mod_file_path}.")
    shutil.copy2(MOD_FILE, mod_file_path)


if __name__ == "__main__":
    os_type = sys.platform
    if os_type in ["win32", "cygwin"]:
        install_mod(WINDOWS_FOLDER_PATH)
    elif os_type == "darwin":
        install_mod(MACOS_FOLDER_PATH)
    elif os_type == "linux":
        sys.exit("Victoria 2 cannot run on linux systems.")
    else:
        sys.exit(f"Unrecognized OS {os_type}.")
