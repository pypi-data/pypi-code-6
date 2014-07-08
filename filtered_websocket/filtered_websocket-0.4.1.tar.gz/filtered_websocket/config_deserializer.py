import json


def config_deserializer(filename):
    """
    Transforms a JSON config file into a list or arguments which may be passed
    to arg_parser.parse_args.

    For instance:

        {
            port: 22
        }

    Would would be transformed to:

        ['--port', '22']
    """
    with open(filename, "r") as config_file:
        config_lines = "".join([l for l in config_file if l[0] != "#"])
        config_data = json.loads(config_lines)
        processed_config_data = []
        for key, value in config_data.items():
            if key == "flags":
                for flag in value:
                    processed_config_data.append("--%s" % flag)
            else:
                processed_config_data.append("--%s" % key)
                if isinstance(value, (list, set)):
                    processed_config_data += value
                else:
                    processed_config_data.append(value)
    return processed_config_data
