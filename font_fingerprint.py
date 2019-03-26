import sys
import logging
import log_helper
import random
import argparse
import registry_helper

logger = log_helper.setup_logger(name="font_fp", level=logging.DEBUG, log_to_file=False)

__doc__ = """The script moves N random fonts to the hidden registry key
Every next run puts it back, but moves there N other fonts, generating new fingerprint"""


class FontFingerprintGenerator:
    """
    The class changes system font fingerprint by moving several fonts to Hidden subkey of Fonts key
    If some fonts were in Hidden key, they are being put back, so all fonts stay in the system
    """

    HIVE = "HKEY_LOCAL_MACHINE"
    FONTS_KEY = "SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Fonts"
    HIDDEN_FONTS_KEY = "SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Fonts\\Hidden"

    @staticmethod
    def create_hidden_key():
        logger.info("Create key {0}".format(FontFingerprintGenerator.HIDDEN_FONTS_KEY))
        registry_helper.create_key(key_hive=FontFingerprintGenerator.HIVE,
                                   key_path=FontFingerprintGenerator.HIDDEN_FONTS_KEY)

    @staticmethod
    def recover_fonts():
        """
        Recover hidden fonts before redistributing to generate new fonts fingerprint
        """
        hidden_fonts = registry_helper.enumerate_key_values(key_hive=FontFingerprintGenerator.HIVE,
                                                            key_path=FontFingerprintGenerator.HIDDEN_FONTS_KEY)
        # font is tuple (ValueName, ValueData, ValueType)
        for font in hidden_fonts:
            rc = registry_helper.create_value(key_hive=FontFingerprintGenerator.HIVE,
                                              key_path=FontFingerprintGenerator.FONTS_KEY,
                                              value_name=font[0],
                                              key_value=font[1],
                                              value_type=font[2])
            logger.info("{0} recovered successfully".format(font) if rc else "Error recovering {0}".format(font))
            if not rc:
                continue
            logger.debug("registry_helper.delete_value({0})".format(font))
            registry_helper.delete_value(key_hive=FontFingerprintGenerator.HIVE,
                                         key_path=FontFingerprintGenerator.HIDDEN_FONTS_KEY,
                                         value_name=font[0])

    @staticmethod
    def generate_font_fingerprint(fonts_delete):
        """
        The script moves N random fonts to the hidden registry key
        :param fonts_delete: Fonts to delete
        """
        logger.info("Generating fonts fingerprint")

        if not registry_helper.is_key_exist(key_hive=FontFingerprintGenerator.HIVE,
                                            key_path=FontFingerprintGenerator.HIDDEN_FONTS_KEY):
            FontFingerprintGenerator.create_hidden_key()
        else:
            FontFingerprintGenerator.recover_fonts()

        system_fonts = registry_helper.enumerate_key_values(key_hive=FontFingerprintGenerator.HIVE,
                                                            key_path=FontFingerprintGenerator.FONTS_KEY)

        logger.info("Moving fonts to hidden key")
        for _ in range(0, fonts_delete):
            # delete_font is tuple (ValueName, ValueData, ValueType)
            delete_font = random.choice(system_fonts)
            logger.info("Move font {0}".format(delete_font))
            rc = registry_helper.create_value(key_hive=FontFingerprintGenerator.HIVE,
                                              key_path=FontFingerprintGenerator.HIDDEN_FONTS_KEY,
                                              value_name=delete_font[0],
                                              key_value=delete_font[1],
                                              value_type=delete_font[2])
            logger.info("{0} moved successfully".format(delete_font) if rc else "Error moving {0}".format(delete_font))
            if not rc:
                continue
            logger.debug("registry_helper.delete_value({0})".format(delete_font))
            registry_helper.delete_value(key_hive=FontFingerprintGenerator.HIVE,
                                         key_path=FontFingerprintGenerator.FONTS_KEY,
                                         value_name=delete_font[0])


def main():
    """
    :return: Exec return code
    """
    parser = argparse.ArgumentParser(description='Command-line parameters')
    parser.add_argument('--recover-only',
                        help='Generate network-related fingerprint',
                        action='store_true',
                        required=False,
                        default=False)
    parser.add_argument(dest='fonts_redistribute', metavar='N', type=int, nargs='?',
                        help='Number of fonts to hide for changing fingerprint', default=-1)

    args = parser.parse_args()

    if args.recover_only and args.fonts_redistribute != -1:
        logger.info("Use either number of fonts or other options")
        parser.print_usage()
        return 0

    if args.recover_only:
        logger.info("Recovering hidden fonts to initial system state")
        FontFingerprintGenerator.recover_fonts()
        return

    fonts_to_redistribute = args.fonts_redistribute
    if args.fonts_redistribute == -1:
        fonts_to_redistribute = random.randint(1, 3)
        logger.info("Number of fonts does not set, choose random")

    logger.info("{0} fonts set to redistribute".format(args.fonts_redistribute))
    FontFingerprintGenerator.generate_font_fingerprint(fonts_to_redistribute)
    return 0


###########################################################################
if __name__ == '__main__':
    sys.exit(main())
