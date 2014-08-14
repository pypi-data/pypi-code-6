import os

here = os.path.abspath(os.path.dirname(__file__))
config_src = os.path.join(here, 'config.yaml')
metadata_src = os.path.join(here, 'metadata.jinja2')
userdata_src = os.path.join(here, 'userdata.jinja2')