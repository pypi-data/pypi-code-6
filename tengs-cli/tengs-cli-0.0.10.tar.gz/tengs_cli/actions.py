import requests, os, zipfile, subprocess
from tengs_cli import *

def dump_object(obj):
    for attr in dir(obj):
        print("obj.%s = %s" % (attr, getattr(obj, attr)))


def login(args, logger):
    path = "users/{0}/check_auth.json".format(args.github_name)
    query_url = generate_url(path, api_key=args.tengs_api_key)
    logger("debug", query_url)
    res = requests.get(query_url)
    logger("debug", res)
    if res.status_code == 200:
        data = {
            "github_name": args.github_name,
            "api_key": args.tengs_api_key
        }
        write_config(data)
        print("Login has been successful!")
        print("{0} has been written".format(settings.file_path))
        return True
    else:
        print("Invalid credentials.")
        return False

def fetch(args, logger):
    path = "exercises/unchecked.json"
    query_url = generate_url(path)
    logger("debug", query_url)
    res = requests.get(query_url)
    if res.status_code == 404:
        print("Try to login (use 'git login' command).")
    elif res.status_code == 500:
        print("Something was wrong. Try later.")
    elif res.status_code == 200:
        data = res.json()
        exercises = data["exercises"]
        if len(exercises) == 0:
            print("You have no new exercises.")
        else:
            for exercise in data["exercises"]:
                exercise_path = "{0}/{1}/{2}".format(settings.tengs_path, exercise["teng_slug"], exercise["slug"])
                tarball_path = "{0}/exercise.zip".format(exercise_path)
                if not os.path.isdir(exercise_path):
                    os.makedirs(exercise_path)
                r = requests.get(exercise["tarball"] + "?api_key=" + value_for("api_key"))
                with open(tarball_path, "wb") as code:
                    code.write(r.content)
                zfile = zipfile.ZipFile(tarball_path)
                zfile.extractall(exercise_path)
                print("Exercise has been written to {0}".format(exercise_path))

def submit(args, logger):
    try:
        (teng_name, exercise_slug) = os.getcwd().replace(os.path.join(settings.tengs_path, ""), "").split(os.sep)
        logger("debug", "teng name: '{0}', exercise slug: '{1}'".format(teng_name, exercise_slug))
    except ValueError:
        exit("Wrong directory.")

    cmd = "make -C {0} test".format(os.getcwd())
    logger("debug", "{0}".format(cmd))
    p = subprocess.Popen([cmd],
        stderr=subprocess.PIPE,
        stdout=subprocess.PIPE,
        shell=True
    )
    result = p.wait()
    logger("debug", "result: {0}".format(result))
    if result != 0:
        print("run `make test` and fix them")
    else:
        #FIXME upload zip with solution to server
        path = "exercises/{0}/results".format(exercise_slug)
        payload = {"result[passed]": 1}
        query_url = generate_url(path)
        logger("debug", query_url)
        logger("debug", payload)
        res = requests.post(query_url, data=payload)
        if res.status_code == 201:
            print("Exercise has been submitted. Check this one on the site.")
            # print res.json()
        elif res.status_code == 404:
            print("Try to login (use 'git login' command).")
        else:
            print("Something was wrong. Try later.")

