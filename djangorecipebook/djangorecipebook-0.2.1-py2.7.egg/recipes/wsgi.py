"""
Recipe generating a wsgi script
"""

from prod import ProdRecipe


wsgi_template = """
%(relative_paths_setup)s
import sys
sys.path[0:0] = [
  %(path)s,
  ]
%(initialization)s
import %(module_name)s

application = %(module_name)s.%(attrs)s(%(arguments)s)
"""


class Recipe(ProdRecipe):

    script_template = wsgi_template

    def install(self):
        return super(Recipe, self). \
            install(__name__.replace('recipes', 'scripts'))
