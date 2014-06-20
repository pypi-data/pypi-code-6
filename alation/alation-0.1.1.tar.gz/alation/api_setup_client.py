import getpass
import urllib
import urllib2
import os
from time import sleep


def user_input():
    base_url = "".join(
        raw_input('Enter the url where you access alation, including http:// (e.g. http://alation.mycorp.com/)\n URL: ').split())
    base_url = base_url.strip("/")
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
        message + "\n(y/[n]): ")
    if yorn == "y":
        execute_request(token_request("getToken", values))


def execute_request(reply):
    (status, values) = reply
    if status == "EXISTING":
        yorn = raw_input(
            "Key already exists on server. " +
            "Would you like to change your key and configure the api on this machine? \n(y/[n]): ")
        if yorn == "y":
            execute_request(token_request("changeToken", values))
    elif status == "NOT_EXISTING":
        retry("Key does not exist. Would you like to try to create one?", values)
    elif status == "INVALID":
        retry("Invalid username or password. Would you like to try again?", values)
    elif status == "NOT_OPEN":
        retry("Could not open URL. Make sure it starts with http:// Would you like to try again?", values)
    elif status == "BAD_FORMAT":
        retry("Incorrectly formatted URL. Make sure it starts with http:// Would you like to try again?", values)
    elif len(status) == 36:
        print "Creating config file with API key " + status + " ..."
        generate_config_file(status + "\n" + values[0])
        print "Success!"
    else:
        print "Error. Please check if the API url you entered is correct and starts with http://"
        retry("Would you like to try again?", values)


def generate_config_file(token):
    home = os.path.expanduser('~')
    doc = open(home + "/.alation_api_config", "w")
    doc.write(token)
    doc.close()


def run_setup():
    print "This quick script will set up your API key in a config file"
    sleep(1.0)
    execute_request(token_request("getToken"))
