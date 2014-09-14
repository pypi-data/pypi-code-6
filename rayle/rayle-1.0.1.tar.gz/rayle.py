def test(movie, level):
    for i in movie:
        if isinstance(i, list):
            level += 1
            test(i, level)
        else:

            print '\t' * level,
            print i

movie = ['i', 'love', ['you', 'are', 'a', 'dream',['love', 'is', 'blind']]]
test(movie, 0)

print 'dream is a dream'
