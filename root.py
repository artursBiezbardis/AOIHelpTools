import os
import sys


def _root_dir():
    if getattr(sys, "frozen", False):
        beside_app = os.path.dirname(os.path.abspath(sys.executable))
        if os.path.isfile(os.path.join(beside_app, "settings.db")):
            return beside_app
        bundled = getattr(sys, "_MEIPASS", "")
        if bundled and os.path.isfile(os.path.join(bundled, "settings.db")):
            return bundled
        return beside_app
    return os.path.dirname(os.path.abspath(__file__))


class RootLocation:

    root_dir = _root_dir()
