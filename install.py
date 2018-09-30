import shutil, sys, os
from os.path import expanduser

MACOS_MOD_FOLDER_PATH = expanduser("~/Library/Containers/com.vpltd.Victoria2HeartOfDarkness/Data/Library/Application Support/com.vpltd.Victoria2HeartOfDarkness-MAS/mod")
WINDOWS_MOD_FOLDER_PATH = "C:\Program Files (x86)\Steam\steamapps\common\Victoria 2\mod"

MOD_FOLDER_PATH = "Napoleon's Legacy"
MOD_FILE_PATH = "Napoleon.mod"

def install_mod(path: str) -> None:
    """Install the mod into the game folder.
    :param path: The install path.
    :type path: str
    """

    mod_folder_path = os.path.join(path, MOD_FOLDER_PATH)
    mod_file_path = os.path.join(path, MOD_FILE_PATH)

    print(f"Deleting {mod_folder_path}.")
    shutil.rmtree(mod_folder_path, ignore_errors=True)

    print(f"Deleting {mod_file_path}.")
    shutil.rmtree(mod_file_path, ignore_errors=True)

    print(f"Copying {MOD_FOLDER_PATH} into {mod_folder_path}.")
    shutil.copytree(MOD_FOLDER_PATH, mod_folder_path)

    print(f"Copying {MOD_FILE_PATH} into {mod_file_path}.")
    shutil.copy2(MOD_FILE_PATH, mod_file_path)

if __name__ == "__main__":
    os_type = sys.platform
    if os_type in ["win32", "cygwin"]:
        install_mod(WINDOWS_MOD_FOLDER_PATH)
    elif os_type == "darwin":
        install_mod(MACOS_MOD_FOLDER_PATH)
    elif os_type == "linux":
        sys.exit("Victoria 2 cannot run on linux systems.")
