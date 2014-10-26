#!/usr/bin/env python

"""
Usage:
    doctpl -t <template> <destination>
    doctpl -l|--list
    doctpl -p|--position

Options:
    -t <template>   init files with template.
    -l --list       list all avaliable templates.
    -p --position   print absolute path of where templates exists.
"""

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import

from docopt import docopt
from doctpl.core import TemplateInfo


def main():
    arguments = docopt(
        __doc__,
        version='0.1.2',
    )
    TemplateInfo.setup()

    if arguments['<destination>']:
        # copy template
        template_name = arguments['-t']
        rel_dst_path = arguments['<destination>']
        template_object = TemplateInfo.template_objects.get(template_name)

        if template_object is None:
            print("No such template.")
            return
        try:
            template_object.copy_to(rel_dst_path)
        except Exception as e:
            print(str(e))

    elif arguments['--list']:
        template_names = TemplateInfo.template_objects.keys()
        if template_names:
            print('\t'.join(template_names))
        else:
            print('No Template Exist.'
                  'Please place Your Templates In ~/.doctpl')

    elif arguments['--position']:
        print(TemplateInfo.CONFIG_DIR)


if __name__ == '__main__':
    main()
