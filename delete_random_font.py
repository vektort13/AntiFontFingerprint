import sys
import logging
import log_helper
import random
import registry_helper
from registry_helper import Wow64RegistryEntry

logger = log_helper.setup_logger(name="font_fp", level=logging.INFO, log_to_file=False)


__doc__ = "The script deletes N random fonts from the system"


def delete_random_font(fonts_delete):
    """
    Delete several random fonts from the system
    :param fonts_delete: Fonts to delete
    """
    hive = "HKEY_LOCAL_MACHINE"
    fonts64 = registry_helper.enumerate_key(hive, "SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Fonts")

    for _ in range(0, fonts_delete):
        delete_font = random.choice(fonts64)
        logger.info("Delete font {0}".format(delete_font))
        registry_helper.delete_value(hive, "SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Fonts", delete_font)


def main():
    """
    :return: Exec return code
    """
    if len(sys.argv) != 2:
        print("Usage: delete_random_font.py <N>")
        return 0

    delete_random_font(int(sys.argv[1]))
    return 0


###########################################################################
if __name__ == '__main__':
    sys.exit(main())
