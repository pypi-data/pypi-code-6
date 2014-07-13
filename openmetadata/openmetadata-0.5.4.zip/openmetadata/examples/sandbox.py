
import os
import shutil
import tempfile
import openmetadata as om
# import openmetadata.api as om

# om.setup_log()

# Starting-point

try:
    root = tempfile.mkdtemp()
    project_path = r'C:\Users\marcus\Dropbox\AF\development\marcus\pipi\repos\openmetadata\openmetadata\tests\fixtures\basic\projects\content\jobs\spiderman'
    shot_path = os.path.join(project_path, '1000')
    shot_location = om.Location(shot_path)
    # om.pull(shot_location)
    # print shot_location['apps'].path
    # apps = om.Entry('apps', parent=shot_location)
    # om.pull(apps)
    entry = om.entry(location=shot_location, metapath='apps')
    # om.pull(entry)
    om.inherit(entry)
    print repr(entry)
    print [c for c in entry.children]
    # print entry.path
    # print entry.value
    # om.pull(shot_location)
    # print apps.path
    # print shot_location['apps'].path
    # print [c for c in shot_location.children]
    # print om.read(project_path)
    # print om.read(r'c:\users\marcus\appdata\local\temp', 'lower')
    # assert upper_value.value == 15

finally:
    shutil.rmtree(root)
