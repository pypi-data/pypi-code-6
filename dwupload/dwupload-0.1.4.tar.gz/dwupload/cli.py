import argparse


def process_arguments():
    parser = argparse.ArgumentParser(prog="dwupload", description="Demandware Upload File System Watcher")
    parser.add_argument("watch_path", nargs="?")
    parser.add_argument("-c", "--config", dest="config_path", help="Path to the config file")
    parser.add_argument("-s", "--section", dest="section_name", default="dwsettings",
                        help="Alternate config section to use if multiple sandbox configurations exist"
                                    "in the config file.")

    args = parser.parse_args()
    return args