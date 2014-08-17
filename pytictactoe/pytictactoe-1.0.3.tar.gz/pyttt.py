from Tkinter import *
import webbrowser
from random import randint, shuffle
import tkMessageBox
print "Welcome to Tic Tac Toe By Gurpreet Singh Toora"
global b0 , b1 , b2 , b3 , b4 , b5 , b6 , b7 , b8 , startg , sys , sym , lis, root, dd, color
color="darkgrey"
lis=[ "" , "" , "" , "" , "" , "" , "" , "" , "" ]
def start():
	global startg
	startg=Tk()
	startg.resizable(height=FALSE, width=FALSE)
	startgfr=Frame(startg)
	startgfr2=Frame(startg)
	startg.title("PyTicTacToe")
	startg.minsize(200,200)
        ws=startg.winfo_screenwidth()
        hs=startg.winfo_screenheight()
        x=(ws/2)-105
        y=(hs/2)-66
        startg.geometry('%dx%d+%d+%d' %(210,132,x,y))
	Label(startgfr, text="Choose Your Symbol: ").grid(row=0, column=1, columnspan=2)
	Button(startgfr, text="X", command=lambda:choosesym("x")).grid(row=1, column=1)
	Button(startgfr, text="O", command=lambda:choosesym("o")).grid(row=1, column=2)
	Label(startgfr2, text="").grid(row=0, column=1, columnspan=2)
	Label(startgfr2, text="Developed by Gurpreet Singh\n (PythonPalace)\nwww.pythonpalace.blogspot.com").grid(row=1, column=1, columnspan=2)
	Label(startgfr2, text="").grid(row=2, column=1, columnspan=2)
	Label(startgfr2, text="Visit Python Palace").grid(row=3, column=1)
	Button(startgfr2, text="Visit", command=lambda:visit("http://www.pythonpalace.blogspot.com")).grid(row=3, column=2)
	Button(startgfr2, text="About PyTicTacToe", command=func).grid(row=4, column=1, columnspan=2)
	startgfr.pack(anchor=CENTER)
	startgfr2.pack(anchor=CENTER)
	startg.mainloop()
def choosesym(y):
	global startg, sys, sym
	startg.withdraw()
	if y=="x":
		sys="O"
		sym="X"
	elif y=="o":
		sys="X"
		sym="O"
	r=randint(0,1)
	first(r, sys, sym)
def first(r, sys, sym):
	global lis, b0, b2, b6, b8
	if r==0:
		tkMessageBox.showinfo("Info","System gets to go first.\nYour Symbol     : %s\nSystem's Symbol : %s" %(sym,sys))
		game(0)
		comp()
	elif r==1:
		tkMessageBox.showinfo("Info","You get to go first!\nYour Symbol     : %s\nSystem's Symbol : %s" %( sym, sys ))
		game(1)
def game(cp):
	global b0 , b1 , b2 , b3 , b4 ,b5 , b6, b7 , b8 , sys , sym , root
	root=Tk()
	root.minsize(120,100)
	root.title("PyTicTacToe")
	root.resizable(height=False, width=False)
	rootf=Frame(root)
        ws=root.winfo_screenwidth()
        hs=root.winfo_screenheight()
        x=(ws/2)-105
        y=(hs/2)-66
        root.geometry('%dx%d+%d+%d' %(210,132,x,y))
	b0=Button(rootf, text="", height=2, width=5, command=lambda:tictac(0, sym, b0))
	b1=Button(rootf, text="", height=2, width=5, command=lambda:tictac(1, sym, b1))
	b2=Button(rootf, text="", height=2, width=5, command=lambda:tictac(2, sym, b2))
	b3=Button(rootf, text="", height=2, width=5, command=lambda:tictac(3, sym, b3))
	b4=Button(rootf, text="", height=2, width=5, command=lambda:tictac(4, sym, b4))
	b5=Button(rootf, text="", height=2, width=5, command=lambda:tictac(5, sym, b5))
	b6=Button(rootf, text="", height=2, width=5, command=lambda:tictac(6, sym, b6))
	b7=Button(rootf, text="", height=2, width=5, command=lambda:tictac(7, sym, b7))
	b8=Button(rootf, text="", height=2, width=5, command=lambda:tictac(8, sym, b8))
	b0.grid(row=0,column=0)
	b1.grid(row=0,column=1)
	b2.grid(row=0,column=2)
	b3.grid(row=1,column=0)
	b4.grid(row=1,column=1)
	b5.grid(row=1,column=2)
	b6.grid(row=2,column=0)
	b7.grid(row=2,column=1)
	b8.grid(row=2,column=2)
	rootf.pack(anchor=CENTER)
	if cp==0:
		comp()
	elif cp==1:
		None
	root.mainloop()
def tictac(x , symb , but):
	global b0 , b1 , b2 , b3 , b4 ,b5 , b6, b7 , b8 , sys , sym , lis
	if lis[x]=="":
		lis[x]=symb
		but.config(text=symb)
		if check():
			again()
		if symb==sym:
			comp()
	else:
		if symb==sym:
			tkMessageBox.showinfo("Info", "Sorry, That Box is Already Filled.\nPlease Try another one.")
def comp():
	global sys, sym, lis
	if (lis[0]==sym and lis[1]=="" and lis[2]=="" and lis[3]=="" and lis[4]=="" and lis[5]=="" and lis[6]=="" and lis[7]=="" and lis[8]=="") or (lis[2]==sym and lis[1]=="" and lis[0]=="" and lis[3]=="" and lis[4]=="" and lis[5]=="" and lis[6]=="" and lis[7]=="" and lis[8]=="") or (lis[6]==sym and lis[1]=="" and lis[2]=="" and lis[3]=="" and lis[4]=="" and lis[5]=="" and lis[0]=="" and lis[7]=="" and lis[8]=="") or (lis[8]==sym and lis[1]=="" and lis[2]=="" and lis[3]=="" and lis[4]=="" and lis[5]=="" and lis[6]=="" and lis[7]=="" and lis[0]==""):
	    x=4
	elif lis[4]==sys and ((lis[0]==sym and lis[8]==sym) or (lis[2]==sym and lis[6]==sym)) and ((lis[1]=="" and lis[2]=="" and lis[3]=="" and lis[5]=="" and lis[6]=="" and lis[7]=="") or (lis[1]=="" and lis[0]=="" and lis[3]=="" and lis[5]=="" and lis[8]=="" and lis[7]=="")):
	    z=[1,3,5,7]
	    shuffle(z)
	    x=z[0] 
        elif lis[0]==sys and lis[2]==sys and lis[1]=="":
            x=1
        elif lis[3]==sys and lis[5]==sys and lis[4]=="":
            x=4
        elif lis[6]==sys and lis[8]==sys and lis[7]=="":
            x=7
        elif lis[0]==sys and lis[6]==sys and lis[3]=="":
            x=3
        elif lis[1]==sys and lis[7]==sys and lis[4]=="":
            x=4
        elif lis[2]==sys and lis[8]==sys and lis[5]=="":
            x=5
        elif lis[0]==sys and lis[8]==sys and lis[4]=="":
            x=4
        elif lis[2]==sys and lis[6]==sys and lis[4]=="":
            x=4
        elif lis[1]==sys and lis[7]==sys and lis[4]=="":
            x=4
        elif lis[3]==sys and lis[5]==sys and lis[4]=="":
            x=4
        elif lis[0]==sys and lis[1]==sys and lis[2]=="":
            x=2
        elif lis[3]==sys and lis[4]==sys and lis[5]=="":
            x=5
        elif lis[6]==sys and lis[7]==sys and lis[8]=="":
            x=8
        elif lis[1]==sys and lis[2]==sys and lis[0]=="":
            x=0
        elif lis[4]==sys and lis[5]==sys and lis[3]=="":
            x=3
        elif lis[7]==sys and lis[8]==sys and lis[6]=="":
            x=6
        elif lis[0]==sys and lis[3]==sys and lis[6]=="":
            x=6
        elif lis[3]==sys and lis[6]==sys and lis[0]=="":
            x=0
        elif lis[1]==sys and lis[4]==sys and lis[7]=="":
            x=7
        elif lis[4]==sys and lis[7]==sys and lis[1]=="":
            x=1
        elif lis[2]==sys and lis[5]==sys and lis[8]=="":
            x=8
        elif lis[8]==sys and lis[5]==sys and lis[2]=="":
            x=2
        elif lis[0]==sys and lis[4]==sys and lis[8]=="":
            x=8
        elif lis[4]==sys and lis[8]==sys and lis[0]=="":
            x=0
        elif lis[6]==sys and lis[4]==sys and lis[2]=="":
            x=2
        elif lis[2]==sys and lis[4]==sys and lis[6]=="":
            x=6
        elif lis[0]==sym and lis[2]==sym and lis[1]=="":
            x=1
        elif lis[3]==sym and lis[5]==sym and lis[4]=="":
            x=4
        elif lis[6]==sym and lis[8]==sym and lis[7]=="":
            x=7
        elif lis[0]==sym and lis[6]==sym and lis[3]=="":
            x=3
        elif lis[1]==sym and lis[7]==sym and lis[4]=="":
            x=4
        elif lis[2]==sym and lis[8]==sym and lis[5]=="":
            x=5
        elif lis[0]==sym and lis[8]==sym and lis[4]=="":
            x=4
        elif lis[2]==sym and lis[6]==sym and lis[4]=="":
            x=4
        elif lis[1]==sym and lis[7]==sym and lis[4]=="":
            x=4
        elif lis[3]==sym and lis[5]==sym and lis[4]=="":
            x=4
        elif lis[0]==sym and lis[1]==sym and lis[2]=="":
            x=2
        elif lis[3]==sym and lis[4]==sym and lis[5]=="":
            x=5
        elif lis[6]==sym and lis[7]==sym and lis[8]=="":
            x=8
        elif lis[1]==sym and lis[2]==sym and lis[0]=="":
            x=0
        elif lis[4]==sym and lis[5]==sym and lis[3]=="":
            x=3
        elif lis[7]==sym and lis[8]==sym and lis[6]=="":
            x=6
        elif lis[0]==sym and lis[3]==sym and lis[6]=="":
            x=6
        elif lis[3]==sym and lis[6]==sym and lis[0]=="":
            x=0
        elif lis[1]==sym and lis[4]==sym and lis[7]=="":
            x=7
        elif lis[4]==sym and lis[7]==sym and lis[1]=="":
            x=1
        elif lis[2]==sym and lis[5]==sym and lis[8]=="":
            x=8
        elif lis[8]==sym and lis[5]==sym and lis[2]=="":
            x=2
        elif lis[0]==sym and lis[4]==sym and lis[8]=="":
            x=8
        elif lis[4]==sym and lis[8]==sym and lis[0]=="":
            x=0
        elif lis[6]==sym and lis[4]==sym and lis[2]=="":
            x=2
        elif lis[2]==sym and lis[4]==sym and lis[6]=="":
            x=6         
        else:
            y=[0,2,6,8]
	    shuffle(y)
	    x=y[0]
            if lis[x]!="":
		if check():
			again()
		else:
			f=0
			for i in lis:
				if i=="":
					f+=1
			if f==2:
				x=lis.index("")
			else:
				comp()

	if x==0:
		tictac(x, sys, b0)
	elif x==1:
		tictac(x, sys, b1)
	elif x==2:
		tictac(x, sys, b2)
	elif x==3:
		tictac(x, sys, b3)
	elif x==4:
		tictac(x, sys, b4)
	elif x==5:
		tictac(x, sys, b5)
	elif x==6:
		tictac(x, sys, b6)
	elif x==7:
		tictac(x, sys, b7)
	elif x==8:
		tictac(x, sys, b8)
def check():
    global lis, sym, sys, startg, root, dd
    if (lis[0]==sym and lis[1]==sym and lis[2]==sym) or (lis[3]==sym and lis[4]==sym and lis[5]==sym) or (lis[6]==sym and lis[7]==sym and lis[8]==sym) or (lis[0]==sym and lis[3]==sym and lis[6]==sym) or (lis[1]==sym and lis[4]==sym and lis[7]==sym) or (lis[2]==sym and lis[5]==sym and lis[8]==sym) or (lis[0]==sym and lis[4]==sym and lis[8]==sym) or (lis[2]==sym and lis[4]==sym and lis[6]==sym):
        dd="You Win"
	return True
    elif (lis[0]==sys and lis[1]==sys and lis[2]==sys) or (lis[3]==sys and lis[4]==sys and lis[5]==sys) or (lis[6]==sys and lis[7]==sys and lis[8]==sys) or (lis[0]==sys and lis[3]==sys and lis[6]==sys) or (lis[1]==sys and lis[4]==sys and lis[7]==sys) or (lis[2]==sys and lis[5]==sys and lis[8]==sys) or (lis[0]==sys and lis[4]==sys and lis[8]==sys) or (lis[2]==sys and lis[4]==sys and lis[6]==sys):
        dd="You Lose"
	return True
    else:
        v=0
        for i in lis:
            if i!="":
                v+=1
        if v==9:
            dd="It's a Draw!"
	    return True
def again():
	global lis, startg, root, dd, b0, b1, b2, b3, b4, b5, b6, b7, b8, color, sys, sym
	if (lis[0]==sys and lis[1]==sys and lis[2]==sys):
		b0.config(bg=color)
		b1.config(bg=color)
		b2.config(bg=color)
	elif (lis[3]==sys and lis[4]==sys and lis[5]==sys):
		b3.config(bg=color)
		b4.config(bg=color)
		b5.config(bg=color)
	elif (lis[6]==sys and lis[7]==sys and lis[8]==sys):
		b6.config(bg=color)
		b7.config(bg=color)
		b8.config(bg=color)
	elif (lis[0]==sys and lis[3]==sys and lis[6]==sys):
		b0.config(bg=color)
		b3.config(bg=color)
		b6.config(bg=color)
	elif (lis[1]==sys and lis[4]==sys and lis[7]==sys):
		b1.config(bg=color)
		b4.config(bg=color)
		b7.config(bg=color)
	elif (lis[2]==sys and lis[5]==sys and lis[8]==sys):
		b2.config(bg=color)
		b5.config(bg=color)
		b8.config(bg=color)
	elif (lis[0]==sys and lis[4]==sys and lis[8]==sys):
		b0.config(bg=color)
		b4.config(bg=color)
		b8.config(bg=color)
	elif (lis[2]==sys and lis[4]==sys and lis[6]==sys):
		b2.config(bg=color)
		b4.config(bg=color)
		b6.config(bg=color)
	elif (lis[0]==sym and lis[1]==sym and lis[2]==sym):
		b0.config(bg=color)
		b1.config(bg=color)
		b2.config(bg=color)
	elif (lis[3]==sym and lis[4]==sym and lis[5]==sym):
		b3.config(bg=color)
		b4.config(bg=color)
		b5.config(bg=color)
	elif (lis[6]==sym and lis[7]==sym and lis[8]==sym):
		b6.config(bg=color)
		b7.config(bg=color)
		b8.config(bg=color)
	elif (lis[0]==sym and lis[3]==sym and lis[6]==sym):
		b0.config(bg=color)
		b3.config(bg=color)
		b6.config(bg=color)
	elif (lis[1]==sym and lis[4]==sym and lis[7]==sym):
		b1.config(bg=color)
		b4.config(bg=color)
		b7.config(bg=color)
	elif (lis[2]==sym and lis[5]==sym and lis[8]==sym):
		b2.config(bg=color)
		b5.config(bg=color)
		b8.config(bg=color)
	elif (lis[0]==sym and lis[4]==sym and lis[8]==sym):
		b0.config(bg=color)
		b4.config(bg=color)
		b8.config(bg=color)
	elif (lis[2]==sym and lis[4]==sym and lis[6]==sym):
		b2.config(bg=color)
		b4.config(bg=color)
		b6.config(bg=color)
	if tkMessageBox.askyesno("Completed","%s\nDo You Want to Play again?" %(dd)):
		for i in range(len(lis)):
			lis[i]=""
		root.withdraw()
		if tkMessageBox.askyesno("Start again","Do You want to start over?"):
			start()
		else:
			r=randint(0,1)
			if r==0:
				tkMessageBox.showinfo("Info","System gets to go first.\nYour Symbol     : %s\nSystem's Symbol : %s" %(sym,sys))
				game(0)
				comp()
			else:
				tkMessageBox.showinfo("Info","You get to go first!\nYour Symbol     : %s\nSystem's Symbol : %s" %( sym, sys ))
				game(1)
	else:
		quit()
def visit(website):
	webbrowser.open(website)
def func():
	tkMessageBox.showinfo("About","Application Name : PyTicTacToe\nVersion : 1.0.1\nDeveloped By : Gurpreet Singh (http://www.pythonpalace.blogspot.com)\nVisit and Join for some interesting stuff.\nThanks for using PyTicTacToe")
start()	
