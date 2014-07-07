import click


def fetch_exercise(args, logger):
    path = "exercises/unchecked.json"
    query_url = hexlet.generate_url(path)
    logger("debug", query_url)
    res = requests.get(query_url)
    if res.status_code == 404:
        print "try to login"
    elif res.status_code == 500:
        print "Something was wrong. Try later."
    elif res.status_code == 200:
        data = res.json()
        exercises = data["exercises"]
        if len(exercises) == 0:
            print "You have no new exercises."
        else:
            for exercise in data["exercises"]:
                exercise_path = "{0}/{1}/{2}".format(tengs_path,
                                                     exercise["teng_slug"],
                                                     exercise["slug"])
                tarball_path = "{0}/exercise.zip".format(exercise_path)
                if not os.path.isdir(exercise_path):
                    os.makedirs(exercise_path)
                r = requests.get(
                    exercise["tarball"] +
                    "?hexlet_api_key=" +
                    utils.value_for("hexlet_api_key"))
                with open(tarball_path, "wb") as code:
                    code.write(r.content)
                zfile = zipfile.ZipFile(tarball_path)
                zfile.extractall(exercise_path)
                print "Exercise has been written to {}".format(exercise_path)


def submit_exercise(args, logger):
    try:
        (teng_name, exercise_slug) = os.getcwd().replace(
            tengs_path + "/", "").split("/")
        logger(
            "debug",
            "teng name: '{}', exercise slug: '{}'".format(
                teng_name,
                exercise_slug))
    except ValueError:
        exit("Wrong directory.")

    cmd = "make -C {} test".format(os.getcwd())
    logger("debug", "{}".format(cmd))
    p = subprocess.Popen([cmd],
                         stderr=subprocess.PIPE,
                         stdout=subprocess.PIPE,
                         shell=True
                         )
    result = p.wait()
    logger("debug", "result: {}".format(result))
    if result != 0:
        print "run `make test` and fix them"
    else:
        # FIXME upload zip with solution to server
        path = "exercises/{}/results".format(exercise_slug)
        payload = {"result[passed]": 1}
        query_url = hexlet.generate_url(path)
        logger("debug", query_url)
        logger("debug", payload)
        res = requests.post(query_url, data=payload)
        if res.status_code == 201:
            print "Exercise has been submitted. Check this one on the site."
            # print res.json()
        else:
            print "something was wrong"
