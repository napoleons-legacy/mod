import shutil
import sys
from os import path

MACOS_FOLDER_PATH = path.expanduser(
    "~/Library/Containers/com.vpltd.Victoria2HeartOfDarkness/Data/Library/Application Support/com.vpltd.Victoria2HeartOfDarkness-MAS/mod")
WINDOWS_FOLDER_PATH = "C:\Program Files (x86)\Steam\SteamApps\common\Victoria 2\mod"

MOD_FOLDER = "Napoleon's Legacy"
MOD_FILE = "Napoleon.mod"


def install_mod(folder: str) -> None:
    """Install the mod into the game folder.
    :param folder: The installation folder.
    :type path: str
    """

    mod_folder_path = path.join(folder, MOD_FOLDER)
    mod_file_path = path.join(folder, MOD_FILE)

    print(f"Deleting {mod_folder_path}.")
    shutil.rmtree(mod_folder_path, ignore_errors=True)

    print(f"Deleting {mod_file_path}.")
    shutil.rmtree(mod_file_path, ignore_errors=True)

<<<<<<< HEAD
    print(f"Copying {MOD_FOLDER_PATH} into {mod_folder_path}.")
    shutil.copytree(MOD_FOLDER_PATH, mod_folder_path)

    print(f"Copying {MOD_FILE_PATH} into {mod_file_path}.")
    shutil.copy2(MOD_FILE_PATH, mod_file_path)
=======
    print(f"Copying {MOD_FOLDER} into {mod_folder_path}")
    shutil.copytree(MOD_FOLDER, mod_folder_path)

    print(f"Copying {MOD_FILE} into {mod_file_path}")
    shutil.copy2(MOD_FILE, mod_file_path)
>>>>>>> Remove two anti-slavery events in the United States, they should be a slavocracy


if __name__ == "__main__":
    os_type = sys.platform
    if os_type in ["win32", "cygwin"]:
        install_mod(WINDOWS_FOLDER_PATH)
    elif os_type == "darwin":
        install_mod(MACOS_FOLDER_PATH)
    elif os_type == "linux":
        sys.exit("Victoria 2 cannot run on linux systems.")
    else:
        sys.exit(f"Unrecognized OS {os_type}")
