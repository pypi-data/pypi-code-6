#-*-coding:utf-8-*-
"""
le module "lextractor.py" fournit la fonction print_item_list().
print_item_list affiche les éléments d'une liste contenant ou pas 
des listes.
"""

def print_item_list(ma_liste):
	"""
	print_item_list() prend en argument "ma_liste",
	ma_liste  est une liste python. Chaque element de "ma_liste" 
	est affichée à l'écran de manière récursive (1 element par ligne)
	"""
	for element in ma_liste:
		if isinstance(element, list):
			print_item_list(element)
		else:
			print(element)
