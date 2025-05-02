import os
import sys


def get_building_path(relative: str) -> str:
    """
    Get the absolute path to a resource, compatible with both development and PyInstaller environments.

    When the application is bundled using PyInstaller, it extracts all necessary files into a temporary
    directory, accessible via `sys._MEIPASS`. This function checks for the presence of `sys._MEIPASS` to
    determine if the application is running in a bundled context and constructs the path accordingly.

    Args:
        relative (str): The relative path to the resource file.

    Returns:
        str: The absolute path to the resource file.
    """
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative)
    else:
        return os.path.join(os.path.abspath("."), relative)
