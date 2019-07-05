"""
pyApp - Messaging

"""
from .factory import *


class Extension:
    """
    pyApp Messaging
    """

    default_settings = ".default_settings"
    checks = ".checks"

    @staticmethod
    def register_commands(root: CommandGroup):
        pass

    @staticmethod
    def ready():
        pass
