def test(movie, indent=False, level=0):
    for i in movie:
        if isinstance(i, list):
            level += 1
            test(i, indent, level)
        else:
            if indent:
                print '\t' * level,
            print i

movie = ['i', 'love', ['you', 'are', 'a', 'dream',['love', 'is', 'blind']]]
test(movie, True, 2)

print 'dream is a dream'
