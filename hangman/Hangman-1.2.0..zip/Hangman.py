import random

words=[
"War","Brother","Winter"
,"Sneeze"


]
a=0
while a==0:
    Rightword=random.choice(words)
    correctword=Rightword.lower()
    correctletters=set(list(correctword))
    guessed=[]
    print("Welcome to Suhail's Hangman!")
    print("#You will get *number of letters in word* + 5 chances to guess.")
    print("#Incase you notice the missing Hangman, I oppose Capital Punishment ;)")
    print("1. Start")
    print("2. Quit")
    b=input("Your choice: ")
    if b=="2":
       print("K bye.")
    if b=="1":
        print("Guess this word: ")
        dashes=("_ "*len(correctword))
        print(dashes)
        c=1
        while c< (len(correctword)+6):
            letter=input("Your Guess: ")
            if letter==("cheatercock"):
                print("YOU WIN")
                print("The word is", correctword)
                break
            if letter in correctword and letter not in guessed and len(letter)==1:
                guessed.append(letter)
                print("Yus.You got that right")
            else:
                print("Nope, wrong letter.Try again.")
            for letter in correctword:
                if letter in guessed:
                    print(letter,end=" ")
                else:
                    print("_ ",end=" ")
            print()
            print("You have ", len(correctword)+5-c, "tries remaining.")
            c+=1
            if len(guessed)==len(correctletters):
                print("Congratulations!!!")
                print("You have guessed wisely! ")
                print(correctword,"is the word you have correctly guessed.")
                print()
                c+=30
                break
            if c==(len(correctword)+6):
                print("The correct word is", correctword)
                print("You got " ,guessed,"correct.")
                print("AAP HAARE HUE INSAAN HO.")
                print("Try again now.")
                print()
