#!/usr/bin/python
"""This program is the first step in creating a module which
provides the functions that can be used in applications for
monitoring servers &amp; services.This code snippet will check
whether specified port on the given server is in listening
state. (Basically it does a port scanning)"""

"""The first line is actually part of the code, not comment.
The characters #! combined is called shebang.The rest of the
line points to the interpreter.If the shebang line is present
the specified interpreter program is run and the path to the
script is provided as the first argument."""

"""Python contains a ton of modules which containes BIFs(Built
in Functions) packaged. To verify the status of the ports we
need to make use of the functions provided  by the "socket"
module.To use the module simply import it into your program."""

import socket

"""The function is defined which takes to arguements host and
port."""

"""Then, Create a new Socket in the AF_INET address family.This is
used for IPv4 Internet Addressing.For IPv6 address here we need
to add a different name SOCK_STREAM means connection oriented TCP
protocol.In short for creating a socket for connection through TCP
invloving IPv4 addresses this will be the code more or less."""

def checkport(host, port):

#Then, Create a new Socket in the AF_INET address family.This is
#used for IPv4 Internet Addressing.For IPv6 address here we need
#to add a different name SOCK_STREAM means connection oriented TCP
#protocol.In short for creating a socket for connection through TCP
#invloving IPv4 addresses this will be the code more or less.

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#The following code handles exceptions.Exceptions are errors
#happens during execution of a program.When the error occurs Python
#generates an exception that can be handled.Python uses "try" and "except"
#blocks to handle the exception. The code below is trying to connect
# to the port in host  which are specified as the arguments to the function.
#If the connection fails an exception will be thrown and "except" block will
#be activated.Under the except block it returns a value "1". Hence if the
#connection to the port fails the function will return the value 1.
#If the connection is successful the value "None" will be returned by the
#function by default.

        try:
          s.connect((host, port))
          s.close()
        except:
          return 1
