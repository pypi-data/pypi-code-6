FOO="barr"

A = { 
 "user" : "a",
 "hostname" : "a",
 "password": "a",
 "key": "a"
}

B = { 
 "user" : "b",
 "password": "b",
 "key": "b"
}

C = { 
 "user" : "c",
 "password": "c",
 "key": "c"
}

ROLES = {
	"one":		[A],
	"two":  	[A,B],
	"three": 	[A,B,C],
}