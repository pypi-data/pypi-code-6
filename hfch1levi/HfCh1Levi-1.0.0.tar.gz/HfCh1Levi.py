def print_nested_list(targetList, indent = False, tapNum = 0):
    for each_item in targetList:
        if isinstance(each_item, list):
            print_nested_list(each_item, indent, tapNum + 1)
        else:
            if indent:
                for tapNums in range(tapNum):
                    print("\t", end = ' ')
            print(each_item)


grandSlam = ["Aus Open", "French Open"]
grandSlam.insert(1,["Li Na", 2014])
grandSlam.append(["Sharapova", 2014])

print_nested_list(grandSlam, False, 1)
