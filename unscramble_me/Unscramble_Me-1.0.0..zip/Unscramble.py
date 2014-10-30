import random
import sys
import time
words=[
"War","Brother","Winter"
,"Sneeze","Word"
,"Agreement"
,"Theory"
,"Slope"
,"Need"
,"Event"
,"Help"
,"Play"
,"Price"
,"Birth"
,"Respect"
,"Month"
,"Move"
,"Use"
,"Produce"
,"Substance"
,"Scale"
,"Letter"
,"Oil"
,"Meeting"
,"Size"
,"Death"
,"Servant"
,"Driving"
,"Hope"
,"Room"
,"Invention"
,"Shake"
,"Nation"
,"Relation"
,"Love"
,"Tin"
,"River"
,"Summer"
,"Weight"
,"Increase"
,"Crack"
,"Flower"
,"Base"
,"Offer"
,"Mountain"
,"Committee"
,"Ray"
,"Blood"
,"Rain"
,"Name"
,"Amount"
,"Woman"
,"Paper"
,"Trade"
,"Money"
,"Wind"
,"Friend"
,"Teaching"
,"Group"
,"Story"
,"Judge"
,"Science"
,"Comparison"
,"Religion"
,"Paint"
,"Harbor"
,"Man"
,"Request"
,"Answer"
,"Meal"
,"Vessel"
,"Swim"
,"Reading"
,"Knowledge"
,"Machine"
,"Amusement"
,"Digestion"
,"List"
,"Snow"
,"Current"
,"Stitch"
,"Sand"
,"Smell"
,"Company"
,"Family"
,"Reaction"
,"Shock"
,"Owner"
,"Lift"
,"Cotton"
,"Fear"
,"Steam"
,"Observation"
,"Animal"
,"Attempt"
,"Butter"
,"Music"
,"Rest"
,"Unit"
,"Desire"
,"Representative"
,"Sugar",
"Market",
"Wood",
"Front",
"Top",
"Idea",
"Art",
"Thunder",
"Value","Grass"]
a=0
while a==0:
    print("Welcome to my 'Unscramble The Word'!!!\nPlease choose your option:\n1.Play\n2.Quit\nYour time limit is 12 seconds.\nYou can guess as many number of times as you want, within the time limit.")
    b=input("Your choice:")
    if b=="2":
        print("Okay bye.")
        sys.exit()
    elif b=="1":
        correctword=random.choice(words)
        Correctword=correctword.lower()
        correctlist=list(Correctword)
        random.shuffle(correctlist)
        t="".join(correctlist)
        T1=time.clock()
        while True:
            print("Your scrambled word is:")
            print(t.upper())
            c=input("Your guess: ")
            T2=time.clock()
            T=T2-T1
            k=format(T,'.2f')
            if T<12 and c!=Correctword:
                print("Nope, Try Again.")
                print(k, "seconds are done, speed up.")
                print("")
            if T>= 12:
                print("TIME UP\nYou Lose,Start Over.")
                print("")
                break
            if c==Correctword:
                T3=time.clock()
                print("YOU WON!\nYour word is",correctword)
                T4=T3-T1
                k2=format(T4,".2f")
                print("You used",k2,"seconds!")
                print("") 
                break
          
            
            
        
    
            
        
        
        
    
