""" PxPilot: Proxmox Virtual Machine Launcher """

__title__ = "pxpilot"
__description__ = "A tool for managing Proxmox VMs with notifications support"
__url__ = "https://github.com/ghostkaa/pxpilot"
__version__ = "0.0.0"
__author__ = "ghostkaa"
__author_email__ = "ghostkaa@gmail.com"
__license__ = "MIT"
__copyright__ = "2024 ghostkaa"


import os
import io

version_file = os.path.join(os.path.dirname(__file__), 'VERSION')

try:
    with io.open(version_file, 'r', encoding='utf-8') as ver:
        __version__ = ver.read().strip()
except FileNotFoundError:
    raise RuntimeError(f"VERSION file not found at {version_file}")
except Exception as e:
    raise RuntimeError(f"Error reading VERSION file: {e}")
