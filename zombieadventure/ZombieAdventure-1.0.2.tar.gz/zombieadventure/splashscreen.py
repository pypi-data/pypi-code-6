# -*- coding: utf-8 -*-

import ast
import operator
import custom_error

def intro():
	print """
                      :::!~!!!!!:.
                  .xUHWH!! !!?M88WHX:.
                .X*#M@$!!  !X!M$$$$$$WWx:.
               :!!!!!!?H! :!$!$$$$$$$$$$8X:
              !!~  ~:~!! :~!$!#$$$$$$$$$$8X:
             :!~::!H!<   ~.U$X!?R$$$$$$$$MM!
             ~!~!!!!~~ .:XW$$$U!!?$$$$$$RMM!
               !:~~~ .:!M"T#$$$$WX??#MRRMMM!
               ~?WuxiW*`   `"#$$$$8!!!!??!!!
             :X- M$$$$       `"T#$T~!8$WUXU~
            :%`  ~#$$$m:        ~!~ ?$$$$$$
          :!`.-   ~T$$$$8xx.  .xWW- ~""##*"
.....   -~~:<` !    ~?T#$$@@W@*?$$      /`
W$@@M!!! .!~~ !!     .:XUW$W!~ `"~:    :
#"~~`.:x%`!!  !H:   !WM$$$$Ti.: .!WUn+!`
:::~:!!`:X~ .: ?H.!u "$$$B$$$!W:U!T$$M~
.~~   :X@!.-~   ?@WTWo("*$$$W$TH$! `
Wi.~!X$?!-~    : ?$$$B$Wu("**$RM!
$R@i.~~ !     :   ~$$$$$B$$en:``
?MXT@Wx.~    :     ~"##*$$$$M~
"""

def outro():
	print"""
            ^^                   @@@@@@@@@
       ^^       ^^            @@@@@@@@@@@@@@@
                            @@@@@@@@@@@@@@@@@@              ^^
                           @@@@@@@@@@@@@@@@@@@@
 ~~~~ ~~ ~~~~~ ~~~~~~~~ ~~ &&&&&&&&&&&&&&&&&&&& ~~~~~~~ ~~~~~~~~~~~ ~~~
 ~         ~~   ~  ~       ~~~~~~~~~~~~~~~~~~~~ ~       ~~     ~~ ~
   ~      ~~      ~~ ~~ ~~  ~~~~~~~~~~~~~ ~~~~  ~     ~~~    ~ ~~~  ~ ~~
   ~  ~~     ~         ~      ~~~~~~  ~~ ~~~       ~~ ~ ~~  ~~ ~
 ~  ~       ~ ~      ~           ~~ ~~~~~~  ~      ~~  ~             ~~
       ~             ~        ~      ~      ~~   ~             ~ 
	"""

def new_game():
	print "Winter has been long in the little town of"
	print "Welton in Kentucky."
	print "Weird stuff has been happening since the summer"
	print "but the full outbreak hasn't happened until October."
	print "Government's been awfully quiet about the whole affair"
	print "and then it was too late to do anything."
	print "Everything happened quickly. Your family is gone now"
	print "and you have been surviving on snow water and ramen"
	print "for past three weeks."
	print "Now it's time to go out..."


def killed_enemies(the_player):

	print "\n--- Killed enemies ---"

	for enemy,number in the_player.killed.items():
		print enemy, ':', number

def score_board(the_player):
	
	ordinary_guy = {'Ordinary Guy': 100}

	score_file = open('scoreboard.txt', 'r')

	if len(score_file.read()) == 0:
		score_file.close()
		score_file = open('scoreboard.txt', 'w')
		score_file.write(str(ordinary_guy))
		score_file.close()
	else:
		score_file.close()
		pass

	score_file = open('scoreboard.txt', 'r')

	scores = ast.literal_eval(score_file.readline())
	score_file.close()
	sorted_scores = sorted(scores.iteritems(), key = operator.itemgetter(1), reverse = True)
	previous_hi_score_tuple = sorted_scores[0]
	previous_hi_score = previous_hi_score_tuple[1]
	get_highest_score(the_player.score, previous_hi_score)

	score_file = open('scoreboard.txt', 'r')

	if len(score_file.read()) == 0:
		score_file.close()
		scores = {}
		scores[the_player.name] = the_player.score
		score_file = open('scoreboard.txt', 'w')
		score_file.write(str(scores))
		score_file.close()
		
	else:
		score_file = open('scoreboard.txt', 'r')
		scores = ast.literal_eval(score_file.readline())
		score_file.close()

	scores[the_player.name] = the_player.score
	score_file = open('scoreboard.txt', 'w')
	score_file.write(str(scores))
	score_file.close()

	sorted_scores = sorted(scores.iteritems(), key = operator.itemgetter(1), reverse = True)



	print "\n"
	print "*" * 80
	print "***** Scoreboard *****"
	print "*" * 80
	
	num = 1

	for name, score in sorted_scores:
		print str(num) + '.', name, " ....... ", score,"points"
		num = num + 1

	custom_error.errortype(4)
	killed_enemies(the_player)

def get_highest_score(score, previous_hi_score):

	if score > previous_hi_score:
		print chr(27) + "[2J"
		intro()
		print "!!! NEW HIGH SCORE !!!"
		print "!!!%d points!!!" % score
		print "Congratulations."
		custom_error.errortype(4)

	elif score >= previous_hi_score:
		print chr(27) + "[2J"
		print "!!! TIE HIGH SCORE !!!"
		print "You have %d, same as previous winner!" % score
		print "Congrats."
		custom_error.errortype(4)
		
		
	else:
		pass







	
