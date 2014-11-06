"""Dies ist das Modul "listElement_in_list.py". Es stellt eine Funktion namens print_ lvl(), die eine Liste mit beliebig vielen eingebetten Listen ausgibt."""

def print_lvl(liste):
    """Diese Funktion erwartet ein positionelles Argument namens “liste", das eine beliebige Python-Liste (mit eventuellen eingebetten Listen) ist. Jedes Element der Liste wird (rekursiv) auf dem Bildschirm auf einer eigenen Zeile ausgegeben."""
    for element in liste: 
        if isinstance(element, list):
            print_lvl(element)
        else:
            print(element)
