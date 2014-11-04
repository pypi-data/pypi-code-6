def print_lol(liist):
        for each_item in liist:
                if isinstance(each_item, list):
                        print_lol(each_item)
                else:
                        print(each_item)
