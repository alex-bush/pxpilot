__version__ = ""
__title__ = ""


def set_metadata(title, version):
    global __title__, __version__
    __title__ = title
    __version__ = version


def get_metadata():
    return __title__, __version__
