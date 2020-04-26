import os
import sys


def reset_tzpath(to=None):
    global TZPATH

    tzpaths = to
    if tzpaths is not None:
        if isinstance(tzpaths, (str, bytes)):
            raise TypeError(
                f"tzpaths must be a list or tuple, "
                + f"not {type(tzpaths)}: {tzpaths}"
            )
        base_tzpath = tzpaths
    else:
        if "PYTHONTZPATH" in os.environ:
            env_var = os.environ["PYTHONTZPATH"]
            if env_var:
                base_tzpath = env_var.split(os.pathsep)
            else:
                base_tzpath = ()
        elif sys.platform != "win32":
            base_tzpath = [
                "/usr/share/zoneinfo",
                "/usr/lib/zoneinfo",
                "/usr/share/lib/zoneinfo",
                "/etc/zoneinfo",
            ]

            base_tzpath.sort(key=lambda x: not os.path.exists(x))
        else:
            base_tzpath = ()

    TZPATH = tuple(base_tzpath)


def find_tzfile(key):
    """Retrieve the path to a TZif file from a key."""
    for search_path in TZPATH:
        filepath = os.path.join(search_path, key)
        if os.path.isfile(filepath):
            return filepath

    return None


TZPATH = ()
reset_tzpath()