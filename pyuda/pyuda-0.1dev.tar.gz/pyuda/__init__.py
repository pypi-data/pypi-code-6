__author__ = 'timmattison'

import sys       # For command-line argument processing
import os        # For checking to see if a file exists
import urllib    # For URL encoding POST parameters
import urllib2   # For creating URL openers
import cookielib # For cookie processing

# Public functions

def get_url_opener(cookie_file=None):
    if cookie_file:
        # Use a cookie JAR that can be saved to disk
        cookie_jar = cookielib.MozillaCookieJar(cookie_file)

        # Load the cookies from disk if they are available
        if os.path.isfile(cookie_file):
            cookie_jar.load()

        # Build a URL opener that uses this cookie JAR
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie_jar))
    else:
        # Build a URL opener that does not use cookies
        opener = urllib2.build_opener()
        cookie_jar = None

    return opener, cookie_jar

def get_url(opener, url):
    # GET the URL and get the response data
    response = opener.open(url)
    response_data = response.read()
    return response_data

def post_url(opener, url, fields=None):
    # Are there any fields?
    if not fields:
        # No, do this little trick to force urllib2 to do a POST
        fields = ""

    # POST the data and get the response data
    response = opener.open(url, urllib.urlencode(fields))
    response_data = response.read()
    return response_data

def check_dependencies(dependencies):
    # Is there just one dependency?
    if isinstance(dependencies, str):
        # Yes, convert it to a list
        dependencies = [dependencies]

    # Start with an empty list of dependency messages
    major_dependency_messages = []
    minor_dependency_messages = []

    # Some guidance from answer #2 here: http://stackoverflow.com/questions/60208/replacements-for-switch-statement-in-python
    for dependency in dependencies:
        # Get the dependency messages from this dependency
        temp_major_dependency_messages, temp_minor_dependency_messages = __check_dependency(dependency)

        # Add these dependencies to our existing lists
        major_dependency_messages += temp_major_dependency_messages
        minor_dependency_messages += temp_minor_dependency_messages

    # Remove all of the none values from the lists
    major_dependency_messages = __remove_none_values_from_list(major_dependency_messages)
    minor_dependency_messages = __remove_none_values_from_list(minor_dependency_messages)

    dependencies_found = False
    dependency_counter = 1

    # Are there any major dependencies?
    if major_dependency_messages:
        # Yes, print them
        for major_dependency_message in major_dependency_messages:
            dependencies_found = True
            print "Dependency #" + str(dependency_counter) + " - " + major_dependency_message
            dependency_counter += 1

    # Are there any minor dependencies?
    if minor_dependency_messages:
        # Yes, print them
        for minor_dependency_message in minor_dependency_messages:
            dependencies_found = True
            print "Dependency #" + str(dependency_counter) + " - " + minor_dependency_message
            dependency_counter += 1

    if dependencies_found:
        print "\nThis script cannot run until the dependencies have been installed."
        print "Please install them in the order specified."
        exit(1)

def get_command_line_arguments(parameters):
    # Require count+1 parameters.  The length of argv is one greater than this because it also includes the current
    #   script's name as element 0 [sys.argv[0])
    if (len(sys.argv) != (len(parameters) + 1)):
        # Didn't get enough parameters.  Print a helpful message and exit.
        print "You must specify " + str(len(parameters)) + " (and only " + str(len(parameters)) + ") options for this program.\n"

        parameter_counter = 1

        for parameter in parameters:
            print("\tParameter #" + str(parameter_counter) + " - " + parameter)
            parameter_counter += 1

        exit(1)

    # Got enough parameters, return them as a list
    output = []

    for loop in range(1, len(parameters) + 1):
        output.append(sys.argv[loop])

    return output

# Private functions

def __manual_check_if_available(program_to_check_for, shell=False):
    import os
    import subprocess

    # Open /dev/null for writing
    FNULL = open(os.devnull, 'w')

    # Call our program and redirect all output to /dev/null
    return True if (subprocess.call(["/usr/bin/env", program_to_check_for], stdout=FNULL, stderr=subprocess.STDOUT, shell=shell) == 0) else False

def __remove_none_values_from_list(input):
    # From: http://stackoverflow.com/questions/14229433/native-python-function-to-remove-nonetype-elements-from-list
    return filter(lambda x: x != None, input)

def __check_dependency(dependency):
    # Calls the necessary function to check for a named dependency.  If the dependency isn't found
    #   it returns a major dependency message indicating that it does not know about the
    #   dependency.

    return {
        'pip': lambda: __check_if_pip_available(),
        'perl': lambda: __check_if_perl_available(),
        'lxml': lambda: __check_if_lxml_available(),
        'yaml': lambda: __check_if_yaml_available()
    }.get(dependency, lambda: (['Unknown dependency ' + dependency], [None]))()

def __check_if_lxml_available():
    try:
        # Can we import lxml?
        import lxml

        # Yes, this dependency is installed and does not need any other dependencies
        return ([None], [None])
    except:
        # No, we cannot import lxml, check if pip is available (a major dependency), and return a
        #   minor dependency message of lxml itself.
        temp_major_dependencies, temp_minor_dependencies = __check_if_pip_available()
        temp_minor_dependencies += ['lxml is not available.  Install it by running "pip install lxml"']

        return [temp_major_dependencies, temp_minor_dependencies]

def __check_if_yaml_available():
    try:
        # Can we import yaml?
        import yaml

        # Yes, this dependency is installed and does not need any other dependencies
        return ([None], [None])
    except:
        # No, we cannot import yaml, check if pip is available (a major dependency), and return a
        #   minor dependency message of lxml itself.
        temp_major_dependencies, temp_minor_dependencies = __check_if_pip_available()
        temp_minor_dependencies += ['yaml is not available.  Install it by following the instructions here: http://pyyaml.org/wiki/PyYAML']

        return [temp_major_dependencies, temp_minor_dependencies]

def __check_if_pip_available():
    # Is pip available?
    if not __manual_check_if_available("pip"):
        # No, return a major dependency message
        return (["pip is not available.  Instructions to install it are here: http://www.pip-installer.org/en/latest/installing.html"], [None])
    else:
        # Yes, pip is installed and does not need any other dependencies
        return ([None], [None])

def __check_if_perl_available():
    # NOTE: This was just an early test.  Typically we don't care if Perl is installed unless we're gluing together
    #         Perl scripts with Python

    # TODO: Check if we need shell set to True for this

    # Is pip available?
    if not __manual_check_if_available("perl --version", True):
        # No, return a major dependency message
        return (["perl is not available.  Instructions to install it are here: http://www.perl.org/get.html"], [None])
    else:
        # Yes, pip is installed and does not need any other dependencies
        return ([None], [None])
