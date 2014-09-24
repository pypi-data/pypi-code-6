from string import Template
import os
import argparse
import dragline


def generate(spider_name):
    template_dir = os.path.join(dragline.__path__[0], "templates")
    main = open(os.path.join(template_dir, "main.tem"), "r").read()
    s = Template(main)
    main = s.substitute(spider_name=spider_name)
    settings = open(os.path.join(template_dir, "settings.tem"), "r").read()

    os.makedirs(spider_name)
    mainfile = open(spider_name + "/main.py", "w")
    mainfile.write(main)
    mainfile.close()
    settfile = open(spider_name + "/settings.py", "w")
    settfile.write(settings)
    settfile.close()


def execute():
    parser = argparse.ArgumentParser()
    parser.add_argument('spider_name', help='name of spider')
    args = parser.parse_args()

    generate(args.spider_name)

if __name__ == "__main__":
    execute()
