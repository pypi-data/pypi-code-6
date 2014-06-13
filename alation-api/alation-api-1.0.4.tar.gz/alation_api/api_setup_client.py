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
        print "Could not open URL"
        return ""
    except ValueError:
        print "Incorrectly formatted URL"
        return ""


def execute_request(reply):
    if reply[0] == "EXISTING":
        yorn = raw_input(
            "Key already exists. Would you like to change your key? \n(yes/no): ")
        if yorn == "yes":
            execute_request(token_request("changeToken", reply[1]))
    elif reply[0] == "NOT_EXISTING":
        yorn = raw_input(
            "Key does not exist. Would you like to try again to create one? \n(yes/no): ")
        if yorn == "yes":
            execute_request(token_request("getToken")[0])
    elif reply[0] == "INVALID":
        yorn = raw_input(
            "Invalid username or password. Would you like to try again? \n(yes/no): ")
        if yorn == "yes":
            execute_request(token_request("getToken")[0])
    elif len(reply[0]) == 36:
        print "Creating config file with API key " + reply[0] + " ..."
        generate_config_file(reply[0] + "\n" + reply[1][0])
        print "Success!"
    else:
        print "Error. Please check if the API url you entered is correct."
        yorn = raw_input("Would you like to try again? \n(yes/no): ")
        if yorn == "yes":
            execute_request(token_request("getToken")[0])


def generate_config_file(token):
    home = os.path.expanduser('~')
    doc = open(home+"/.alation_api_config", "w")
    doc.write(token)
    doc.close()


def run_setup():
    print "This quick script will set up your API key in a config file"
    sleep(1.0)
    execute_request(token_request("getToken"))
