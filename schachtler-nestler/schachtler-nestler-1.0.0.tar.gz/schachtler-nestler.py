def print_lvl(liste):
    for element in liste:
        if isinstance(element, list):
            print_lvl(element)
        else:
            print(element)

#filme = ["Die Ritter der Kokusnuss", 1975, "Terry Jones & Terry Gilliam",
#        ["Graham Cheapman", ["Michael Palin", "John Cleese",
#        "Terry Gilliam", "Eric Idle", "Terry Jones"]]]

#print_lvl(filme)
