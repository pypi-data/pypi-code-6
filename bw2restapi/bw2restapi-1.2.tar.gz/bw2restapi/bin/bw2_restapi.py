#!/usr/bin/env python
# encoding: utf-8
"""Brightway2 REST API.

Usage:
  bw2-webapi [--port=<port>] [--insecure]
  bw2-webapi -h | --help
  bw2-webapi --version

Options:
  -h --help     Show this screen.
  --version     Show version.
  --insecure    Allow outside connections (insecure!).

"""
from bw2restapi import api_app
from docopt import docopt


def main():
    args = docopt(__doc__, version='Brightway2 Web UI 0.1')
    port = int(args.get("--port", False) or 5000)  # + random.randint(0, 999))
    host = "0.0.0.0" if args.get("--insecure", False) else "localhost"

    api_app.run(host=host, port=port)

if __name__ == "__main__":
    main()
