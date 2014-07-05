import sys
import custom_error
import splashscreen

def type(death_id, the_player):

		death_dict = {
			1: "\nYou're so old you barely survived the first wave of zombie attack. Just as you get out of the bed you feel pain chest. Seconds later you fall to the ground and die",
			2: "\n'Baba.. da-ba'. You're just a baby unable to do anything really. You starve to death and die.",
			3: "\nYou reached zero/negative hitpoints. You die.",
			4: "\nYou're an old fart. You get heart attack from push ups and die seconds later.",
			5: "\nYou exhaust yourself and later a zombie approaches you. Your lack of strength is unable to deal with it. You're dead now... and sort of alive but the game is over now.",
			6: "\nYou reached zero/negative hitpoints and got killed by your enemy.",
			7: "\nYou get bitten by zombie and eventually turn dead. You die.",
			8: "\nLast thing you see is a barrel of shotgun and sparks in slow motion. 'Fucker' you hear old man mumbling.",
			9: "\nYou feel a pinch on your finger as you turn cylinders on the lock again. Seconds later you stop breathing and you die.",
			10: "\n'What a stupid answer.' You think to yourself as you feel the bullet coming through you.",
			11: "\nAs you keep going the cracking sound gets louder. Eventually the bridge collapses and you lose conscience when you fall into river, drowning to death.",
			12: "\nYou lose balance for a little while and you slip. A lone glass shrapnel hanging from the window impales you."
			}

		get_death_type = death_dict.get(death_id)
		print get_death_type
		print "Your score is %d." % the_player.score

		custom_error.errortype(4)
		splashscreen.score_board(the_player)
		custom_error.errortype(4)
		exit(1)