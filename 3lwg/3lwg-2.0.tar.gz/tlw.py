#! /usr/bin/env python
import argparse
import random

def choose_word(length=3):
    """
        Select a word for the player to guess.
    """
    if length != 3:
        raise ValueError('Length must be 3')

    with open('words') as words_handle:
        words = words_handle.readlines()
        words = [word.strip() for word in words
                 if len(word.strip()) == length]

    return random.choice(words).lower()

def count_points(word,guess):
    #for position in range(0, len(word)):
    count = 0
    for pos,letter in enumerate(word):
        if guess[pos] == letter:
            count +=1
    return count

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '--length', '-l',
        default=3,
        type=int,
        help='Length of word you have to guess.'
    )
    parser.add_argument(
        '--guesses', '-g',
        default=10,
        type=int,
        help='Amount of guesses you get.'
    )

    options = parser.parse_args()

    length = options.length
    guesses = options.guesses
    word = choose_word(length).lower()
    print('Guess the {} letter word'.format(length))
    for i in range(guesses):
        guess = ''
        while len(guess) != length:
            if len(guess) > 0:
                print('No, you must have a guess of length %s' % length)
            guess = raw_input().lower().strip()
            if len(guess) == random.randint(1,2 * length):
                print("That's NUMBERWANG!")
        points = count_points(word,guess)
        print('You got {} letters correct!'.format(points))
        print('You have %s guesses left' % (guesses - 1 - i))
        if points == length:
            print('You win!')
            break
    print("Better luck next time, the word was %s." % word)


if __name__ == '__main__':
    main()
