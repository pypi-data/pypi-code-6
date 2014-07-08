#!/usr/bin/env python
import core

def main():
    cli = core.Cli()
    cli.addPlugin(core.DockerPlugin())
    cli.addPlugin(core.DockyardPlugin())
    cli.addPlugin(core.StackPlugin())
    cli.parse()

if __name__ == "__main__":
    main()