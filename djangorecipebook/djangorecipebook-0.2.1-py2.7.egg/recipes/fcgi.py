"""
Recipe generating a fcgi script
"""

from prod import ProdRecipe


class Recipe(ProdRecipe):

    def install(self):
        return super(Recipe, self). \
            install(__name__.replace('recipes', 'scripts'))
