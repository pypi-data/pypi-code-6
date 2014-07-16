FOO="barr"

A = { 
 "user" : "thierry",
 "hostname" : "localhost",
 "password": "cordonchat",
}

B = { 
 "user" : "jeanglode",
 "hostname" : "valkyrie2.quelquechose.fr",
 "key": "/home/thierry/.ssh/id_rsa.pub"

}

C = { 
 "user" : "qqch",
 "hostname" : "yggdrasil.quelquechose.fr",
 "port": "2206",
 "password" : "heckeljeckel",
}

FABRIC_ROLES = {
	"db":		[A],
	"web":  	[B,C],
}