"""A library to support the mojo command line client"""
import os
import sys
import yaml

from mojo import Mojo


def dict_merge(src, dest):
    """Helper function for merging config dictionaries"""
    # For each item in the source
    for key, value in src.items():
        # If the item is a dictionary, merge it
        if isinstance(value, dict):
            dict_merge(value, dest.setdefault(key, {}))
        # Otherwise, the destination takes the source value
        else:
            dest[key] = value
    return dest


def cli(args):
    """Run the command line client"""

    # Defaults
    config_files = ["/etc/mojo.yml", os.path.expanduser("~") + "/.mojo.yml"]
    config = {"environments": {}, "default_environment": None}
    opts = {}
    default_opts = {
        "endpoint": "localhost",
        "port": 3000,
        "use_ssl": False,
        "verify": True,
        "user": None,
        "password": None
    }

    # User supplied additional config file?
    if args.config is not None:
        config_files.append(os.path.expanduser(args.config))

    # Merge the config dictionaries
    for config_file in config_files:
        try:
            config = dict_merge(yaml.load(open(config_file, 'r')), config)
        except IOError:
            pass

    # Some logic to determine if we have enough information to run
    # and also to load any preconfigured connection options

    # User supplied an environment name...
    if args.env is not None:
        # ...but it doesn't exist: error/exit.
        if args.env not in config["environments"]:
            print("The specified environment is not defined.")
            sys.exit(1)
        # ...and it is defined: "load" those settings.
        else:
            opts = config["environments"][args.env]
    # User did not supply an environment name...
    else:
        # ...but they have a default_environment...
        if config["default_environment"] is not None:
            # ...and that environment is defined: "load" those settings.
            if config["default_environment"] in config["environments"]:
                opts = config["environments"][config["default_environment"]]
            # ...but that env doesn't exist: error/exit.
            else:
                print("The default environment is not defined.")
                sys.exit(1)

    # Allow user to override settings from the CLI
    if args.endpoint is not None:
        opts["endpoint"] = args.endpoint
    if args.port is not None:
        opts["port"] = args.port
    if args.use_ssl is not None:
        opts["use_ssl"] = args.use_ssl
    if args.verify is not None:
        opts["verify"] = args.verify
    if args.user is not None:
        opts["user"] = args.user
    if args.password is not None:
        opts["password"] = args.password

    # Bring in any missing values at their defaults
    opts = dict_merge(opts, default_opts)

    # Route that action!
    if args.action == "list":
        opts["boolean"] = args.boolean
        opts["tags"] = args.tags
        list_scripts(opts)
    elif args.action == "show":
        show(opts, args)
    elif args.action == "run":
        run(opts, args)
    elif args.action == "reload":
        reload_jojo(opts)

    sys.exit(0)


def print_script(script):
    print("Name: {}".format(script["name"]))
    print("Description: {}".format(script["description"]))
    print("Filename: {}".format(script["filename"]))
    if "http_method" in script:
        print("HTTP Method: {}".format(script["http_method"]))
    if "output" in script:
        print("Output Type: {}".format(script["output"]))
    if "params" in script and len(script["params"]) > 0:
        print("Parameters:")
        for param in sorted(script["params"]):
            print("  {}: {}".format(param["name"], param["description"]))
    if "filtered_params" in script and len(script["filtered_params"]) > 0:
        print("Filtered parameters:")
        for param in script["filtered_params"]:
            print("  {}".format(param))
    if "tags" in script and len(script["tags"]) > 0:
        print("Tags:")
        for tag in sorted(script["tags"]):
            print("  {}".format(tag))
    print("Lock: {}".format(script["lock"]))



def list_scripts(opts):
    """List available scripts"""
    mojo = Mojo(**opts)
    if mojo.unauthorized:
        print("Authentication failed")
    else:
        if opts["boolean"] is not None and opts["tags"] is not None:
            if opts["boolean"] == "and":
                param = "tags"
            elif opts["boolean"] == "or":
                param = "any_tags"
            elif opts["boolean"] == "not":
                param = "not_tags"
            scripts = mojo.get_scripts(param, opts["tags"])
            for script in sorted(scripts):
                print_script(mojo.get_script(script))
                print("")
        else:
            for script in sorted(mojo.scripts):
                print(script)


def show(opts, args):
    """Show script details"""
    mojo = Mojo(**opts)
    script = mojo.get_script(args.script)

    if mojo.unauthorized:
        print("Authentication failed")
    else:
        print_script(script)

def run(opts, args):
    """Run a script"""
    mojo = Mojo(**opts)

    # Parse CLI-given parameters
    params = {}
    for param in args.params:
        broken = param.split("=")
        params[broken[0]] = broken[1]

    resp = mojo.run(args.script, params)

    if mojo.auth and mojo.unauthorized:
        print("Authentication failed")
    else:
        print("Status Code: {}".format(resp.status_code))
        print("Headers:")
        for header in resp.headers:
            print("  {}: {}".format(header, resp.headers[header]))
        j = resp.json()
        print("Script return code: {}".format(resp.status_code))
        if "stderr" in j:
            print("Stderr:")
            if type(j["stderr"]) is unicode:
                print(j["stderr"])
            else:
                for line in j["stderr"]:
                    print("  {}".format(line))
        if "stdout" in j:
            print("Stdout:")
            if type(j["stdout"]) is unicode:
                print(j["stdout"])
            else:
                for line in j["stdout"]:
                    print("  {}".format(line))
        if "return_values" in j and len(j["return_values"]) > 0:
            print("Return Values:")
            for key in sorted(j["return_values"]):
                print("  {}: {}".format(key, j["return_values"][key]))

def reload_jojo(opts):
    """Reload the Jojo"""
    mojo = Mojo(**opts)
    result = mojo.reload()

    if result is True:
        print("Reload successful!")
    elif result is False:
        print("Authentication failed")
    elif type(result) == int:
        print(
            "The Jojo responded with an unexpected status code: {}".
            format(result)
        )
