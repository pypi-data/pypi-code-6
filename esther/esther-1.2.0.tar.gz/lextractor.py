#-*-coding:utf-8-*-
"""
le module "lextractor.py" fournit la fonction print_item_list().
print_item_list affiche les éléments d'une liste contenant ou pas 
des listes.
"""

def print_item_list(ma_liste, niveau=0):
	"""
	print_item_list() prend en argument "ma_liste",
	ma_liste  est une liste python. Chaque element de "ma_liste" 
	est affichée à l'écran de manière récursive (1 element par ligne)
	l'argument "niveau" est utilisé pour insérer une tabulation pour afficher les item suivant qu'ils soient dans une liste incluse.
	"""
	for element in ma_liste:
		if isinstance(element, list):
			print_item_list(element, niveau + 1)
		else:
			for tab in range(niveau):
				print("\t", end='')
			print(element)

