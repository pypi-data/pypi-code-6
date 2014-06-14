#!/usr/bin/python3
"""
cloneall.py
Clones all of a user's repositories.

Usage:
    python cloneall.py [-a|--all] [-u username] [--no-curses]

(+) If the -a or --all flag is not set, the script will ask about each repository in turn.
(+) If the --no-curses option is given, the program will use the standard input method.
(+) If --no-curses is not given, the program defaults to using Curses if installed, falling
    back to the standard method if necessary.
(+) If the username is not given, the program will ask for it to be entered.

"""
try:
    # Import libraries
    import json
    import urllib.request
    import sys
    import os
    import subprocess
    from pprint import pprint


    def get_json(url):
        """Takes url as argument, returns json data from GitHub."""
        try:
            data = urllib.request.urlopen(url).read().decode("utf-8")
        except urllib.error.HTTPError:
            print("Username not found.")
            quit()
        else:
            return json.loads(data)


    def api_url(username):
        """Returns github api url for a given username."""
        return "https://api.github.com/users/{}/repos?per_page=100".format(username)
        # Pass PHP argument per_page with value 100; get 100 results per page.


    def parse_args():
        """
        Sifts through the command-line arguments given.
        Returns a dictionary in the format:
        {username:<string>,
         dl_all:<boolean>,  # Should download all user's repos
         ud_all:<boolean>,  # Should update all existing repos
         no_dl:<boolean>}   # Only update existing repos
        """
        args = sys.argv[1:]  # Don't include filename.

        # By default the user has to pick whether to download/update all.
        return_dict = {'username': "",
                       'dl_all': False,
                       'ud_all': False,
                       'no_dl': False}

        if not args:
            return return_dict  # No input, get it from program.

        else:
            try:
                if "--download-all" in args or "-a" in args:
                    # Set boolean, then remove all instances of "--all" or "-a"
                    return_dict['dl_all'] = True
                    args = [arg for arg in args 
                        if arg not in ["-a", "--download-all"]]

                # "Download all" takes precedence over "No download".
                elif "--no-download" in args:
                    return_dict['no_dl'] = True
                    args = [arg for arg in args if arg != "--no-download"]

                if "--update-all" in args or "-p" in args:
                    # Same as above, for update rather than download.
                    return_dict['ud_all'] = True
                    args = [arg for arg in args
                        if arg not in ["-p", "--update-all"]]


                # The element after "-u" or "--username" should be the username.
                if "--username" in args:
                    return_dict['username'] = args[args.index("--username") + 1]
                elif "-u" in args:
                    return_dict['username'] = args[args.index("-u") + 1]

            except IndexError:
                # User typed an option after -u, instead of a username.
                print(__doc__)
                quit()
        return return_dict

    def print_repo_info(repo):
        """Pretty-prints information about repository."""
        print("\n -- {} -- \n".format(repo['name']))
        print("Description:\n{}\n".format(repo['description']))


    def should_download_all():
        """Provides a prompt to query whether all items should be downloaded."""
        while True:
            get_all = input("Download all? [Y/N] ")
            if get_all in ['Y', 'y']:
                return True
            elif get_all in ['N', 'n']:
                return False


    def should_dl_all_menu():
        """Curses menu for should_download_all."""
        newmenu = Menu("Yes", "No", title="Download all repositories?")
        choice = newmenu.show()
        if choice:
            return choice == "Yes"
        # Choice is None, user pressed Q.
        print("Exiting.")
        quit()


    def should_update_all():
        """Provides a prompt to query whether all items should be updated."""
        while True:
            get_all = input("Update all? [Y/N] ")
            if get_all in ['Y', 'y']:
                return True
            elif get_all in ['N', 'n']:
                return False


    def should_ud_all_menu():
        """Curses menu for should_update_all."""
        newmenu = Menu("Yes", "No", title="Update all existing repositories?")
        choice = newmenu.show()
        if choice:
            return choice == "Yes"
        # Choice is None, user pressed Q.
        print("Exiting.")
        quit()


    def get_username():
        """Provides a prompt to query the username to download from."""
        while True:
            username = input("Username: ")
            if username:
                return username


    def clone_repo(repository, arguments):
        """Clones the repository passed to it using the git program."""
        devnull = open(os.devnull, "w")  # Allow writing to null
        try:
            # Try cloning; write all errors to null and catch them here.
            subprocess.check_call(["git", "clone", repository['git_url']],
                                    stderr=devnull)
        except subprocess.CalledProcessError:
            # Error thrown when repo exists locally.
            if arguments['ud_all']:
                update_repository(repository['name'])
            elif should_update_repository(repository['name']):
                update_repository(repository['name'])
        else:
            print("Cloned {} successfully.".format(repository['name']))


    def should_update_repository(repo_name):
        """Provides a prompt to ask the user to update an existing repository."""
        while True:
            choice = input("Repository {} already exists here, update? [Y/N] "
                            .format(repo_name))
            if choice.lower() in ["y", "n"]:
                break
        return choice.lower() == 'y'


    def should_ud_repo_menu(repo_name):
        """Curses version of should_update_repository."""
        menu_title = "Repository {} already exists. Update?".format(repo_name)
        menu = Menu("Yes", "No", title=menu_title)
        choice = menu.show()
        if choice:
            return choice == "Yes"
        # Choice is None, user pressed Q.
        print("Exiting.")
        quit()


    def should_download_repository(repo):
        """Provides a prompt to ask the user to download a repository."""
        print_repo_info(repo)  # Display name and description.
        while True:
            yesno = input("Clone repository? [Y/A/N/Q] ")
            if yesno.lower() in ["y", "n", "a"]:
                return yesno.lower()
            elif yesno.lower() == "q":
                quit()


    def should_dl_repo_menu(repo):
        """Curses version of should_download_repo."""
        menu = Menu("Download",
                    "Skip",
                    "Download All",
                    title=repo['name'],
                    subtitle=repo['description'])
        choice = menu.show()
        # Required for interchangeability with non-curses input.
        choice_dict = {"Download": "y",
                       "Skip": "n",
                       "Download All": "a"}
        if choice:
            return choice_dict[choice]
        # Choice is None, user pressed Q.
        quit()


    def update_repository(repo_name):
        """Updates a given repository."""
        print("\nUpdating {}.".format(repo_name))
        try:
            # Change into repo directory.
            os.chdir(repo_name)
        except:  # Catch-all
            print("Something's gone wrong, will ignore repository.")
        else:
            try:
                output = subprocess.check_output(["git", "pull"])
                # Output is a byte string, need to decode.
                print(output.decode(sys.stdout.encoding))
            except subprocess.CalledProcessError:
                # Shouldn't happen with working Git.
                print("Something went badly wrong.")
            os.chdir("..")


    def download_repos(repos, arguments):
        """Downloads repositories according to given arguments."""
        if repos:  # If list of repositories is not blank.
            for repo in repos:
                try:
                    if arguments['dl_all']:
                        # Skip printing repo info for each one.
                        clone_repo(repo, arguments)
                    elif arguments['ud_all'] and os.path.exists(repo['name']):
                        update_repository(repo['name'])
                    elif not arguments['no_dl']:
                        choice = should_download_repository(repo)
                        if choice == "y":
                            clone_repo(repo, arguments)
                        elif choice == "a":
                            clone_repo(repo, arguments)
                            arguments['dl_all'] = True

                except subprocess.CalledProcessError:
                    # Mostly a safety net, this shouldn't happen.
                    pass  # Error message printed anyway.
        else:
            print("User has no publicly available repositories.")


    def format_url(url):
        """Ensures URL is using HTTPS protocol."""
        return "https://" + url[6:]


    def main():
        """The main function for this program. Requests any input necessary, then
        carries out the instructions."""
        # Collect command-line switches.
        arguments = parse_args()

        # Get info if it hasn't been specified in parameters.
        if not arguments['username']:
            arguments['username'] = get_username()

        # Get info from fetched JSON data.
        my_api_url = api_url(arguments['username'])
        json_data = get_json(my_api_url)

        if not (arguments['dl_all'] or arguments['no_dl']):
            arguments['dl_all'] = should_download_all()

        if not arguments['ud_all']:
            arguments['ud_all'] = should_update_all()

        # Make a shorter, more manageable list of dictionaries:
        repos = [
                {'name': repo['name'],
                'git_url': format_url(repo['git_url']),
                'description': repo['description']}
                for repo in json_data
                ]

        download_repos(repos, arguments)


    if __name__ == "__main__":
        # Check if Git is installed (vital).
        try:
            devnull = open(os.devnull, "w")
            subprocess.check_call(["git", "--version"], stdout=devnull)
        except subprocess.CalledProcessError:
            print("Git version control system required.")
            quit()

        # Check if Curses is installed (nonvital).
        if "--no-curses" not in sys.argv:
            try:
                import curses
            except ImportError:
                pass
            else:
                try:
                    from SimpleMenu import Menu
                    # _menu suffix denotes a Curses menu alternative.
                    should_update_repository = should_ud_repo_menu
                    should_download_repository = should_dl_repo_menu
                    should_update_all = should_ud_all_menu
                    should_download_all = should_dl_all_menu
                except ImportError:
                    # SimpleMenu not present
                    print("Menu support requires SimpleMenu.py, will fall"
                          " back to standard input.")
        main()

except (KeyboardInterrupt, EOFError):
    # User presses C-c or C-d (respectively: kill process or EOF)
    print("\nWill exit now.")