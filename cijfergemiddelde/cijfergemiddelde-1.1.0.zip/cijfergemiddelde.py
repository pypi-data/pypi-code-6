'''Dit is een cijfergemiddelde programma zoals berekend wordt
op het Calandlyceum in Amsterdam.'''

def bereken_gemiddelde(cijfers, gewichten):
    '''Deze functie heeft twee lijsten als argument.
    Een lijst met behaalde cijfers en een lijst met
    bijbehorende gewichten.'''

    som = 0 # Hierin opgeslagen alle cijfers vermenigvuldigt met bijbehorende gewichten
    totaal = 0 # Hierin opgeslagen de opgetelde gewichten
    for c, g in zip(cijfers, gewichten):
      som = som + float(c) * int(g)
      totaal = totaal + int(g)
    gemiddelde = format(som / totaal, '.1f') #uitrekenen gemiddelde, afgerond op 1 decimaal
    return gemiddelde



