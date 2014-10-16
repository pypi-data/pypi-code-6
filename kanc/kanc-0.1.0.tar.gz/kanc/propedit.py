"""
 Property editor
"""
import os, sys, tempfile, subprocess
import re

class PropertyEditor(object):
    def __init__(self, properties):
        self.properties = properties

    def __contains__(self, key):
        for p in self.properties:
            if p['name'] == key:
                return True
        return False

    def __setitem__(self, key, value):
        for p in self.properties:
            if p['name'] == key:
                p['value'] = value
                return
        sys.stderr.write('Error: wrong key {}'.format(key))
    
    def __getitem__(self, key):
        for p in self.properties:
            if p['name'] == key:
                return p['value']
        return None

    def __prop_to_text(self):
        propfile = \
"""\
#
# Please type the following fields
# Please do not modify/delete the line followed by #
#

"""
        for p in self.properties:
            propfile += '##################\n'
            propfile += '# {}\n\n'.format(p['name'])
        return propfile

    def __text_to_prop(self, text):
        props = re.findall('#{5,}\n# (.*)\n([^#]*)', text)
        for p in props:
            if p is not None:
                k, v = p
                if k in self:
                    self[k] = v
                else:
                    sys.stderr.write('Error: Unknown field {}'.format(k))

    def edit(self):
        editor = os.environ.get('EDITOR')
        if editor is None or editor == '':
            sys.stdout.write('Error: No editor is specified EDITOR')
        
        data = self.__prop_to_text()

        tmp_file = tempfile.mkstemp()
        f = file(tmp_file[1], 'w')
        f.write(data)
        f.close()
        subprocess.call([editor, tmp_file[1]])
        f = file(tmp_file[1])
        modified = f.read()
        f.close()
        os.remove(tmp_file[1])

        if data == modified:
            sys.stderr.write('Abort: The data is not updated')
            return None
        print self.__text_to_prop(modified)
        return modified 


if __name__ == "__main__":
    # Test code
    p = PropertyEditor([{'name':'p1', 'value':None}, {'name':'p2', 'value':None}])
    p.edit()
