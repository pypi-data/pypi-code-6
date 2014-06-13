import getpass
import urllib
import urllib2
import os
from time import sleep


def user_input():
    base_url = "".join(
        raw_input('Enter the base url of the API (including http://):  ').split())
    username = "".join(raw_input('Enter your email:  ').split())
    password = getpass.getpass('Enter your password:  ')
    return (base_url, username, password)


def token_request(request_type, values=()):
    if request_type == "getToken":
        (base_url, username, password) = user_input()
        values = (base_url, username, password)
    else:
        (base_url, username, password) = values
    request = urllib2.Request(
        base_url + "/api/" + request_type + "/")
    try:
        data = urllib.urlencode({"Username": username, "Password": password})
        response = urllib2.urlopen(request, data=data)
        reply = response.read()
        if len(reply) > 36:
            # execute_request will catch unknown error
            print response.status, response.reason
        return (reply, values)
    except urllib2.URLError:
        return ("NOT_OPEN", ())
    except ValueError:
        return ("BAD_FORMAT", ())


def retry(message, values):
    yorn = raw_input(
        message + "\n(yes/[no]): ")
    if yorn == "yes":
        execute_request(token_request("getToken", values))


def execute_request(reply):
    status = reply[0]
    if status == "EXISTING":
        yorn = raw_input(
            "Key already exists. Would you like to change your key? \n(yes/no): ")
        if yorn == "yes":
            execute_request(token_request("changeToken", reply[1]))
    elif status == "NOT_EXISTING":
        retry("Key does not exist. Would you like to try to create one?", reply)
    elif status == "INVALID":
        retry("Invalid username or password. Would you like to try again?", reply)
    elif status == "NOT_OPEN":
        retry("Could not open URL. Make sure it starts with http:// Would you like to try again?", reply)
    elif status == "BAD_FORMAT":
        retry("Incorrectly formatted URL. Make sure it starts with http:// Would you like to try again?", reply)
    elif len(status) == 36:
        print "Creating config file with API key " + reply[0] + " ..."
        generate_config_file(status + "\n" + reply[1][0])
        print "Success!"
    else:
        print "Error. Please check if the API url you entered is correct and starts with http://"
        retry("Would you like to try again?", reply)


def generate_config_file(token):
    home = os.path.expanduser('~')
    doc = open(home + "/.alation_api_config", "w")
    doc.write(token)
    doc.close()


def run_setup():
    print "This quick script will set up your API key in a config file"
    sleep(1.0)
    execute_request(token_request("getToken"))
