import os
import inspect
from httplib2 import Http
from urllib import urlencode
import base64
from runner import load_modules
import argparse
import zipfile


def zipdir(source, destination):
    folder = os.path.abspath(source)
    with zipfile.ZipFile(destination, 'w') as zipf:
        for root, dirs, files in os.walk(folder):
            path = os.path.relpath(root, folder)
            for filename in files:
                relname = os.path.join(path, filename)
                absname = os.path.join(root, filename)
                if filename.endswith(".py"):
                    zipf.write(absname, relname, zipfile.ZIP_DEFLATED)


def deploy(url, username, password, foldername, spider_website=None):
    # check whether the folder is a spider
    if not "main.py" in os.listdir(foldername):
        return "Not a valid spider"

    # check if the main.py contain a spider class
    module, settings = load_modules(foldername)
    # check if main.py contain a spider class
    try:
        spider = getattr(module, "Spider")
    except Exception as e:
        return "Spider class not found"

    if not inspect.isclass(spider):
        return "Spider class not found"

    # create a spider object and check whether it contain required attributes
    spider_object = spider(None)

    try:
        if spider_object._name and spider_object._start and spider_object._allowed_urls_regex:
            spider_name = spider_object._name
        else:
            return "required attributes not found in spider"

    except Exception as e:
        print e
        return "Spider deploying failed"

    # zip the folder
    zipdir(foldername, "/tmp/%s.zip" % spider_name)
    zipf = base64.encodestring(open("/tmp/%s.zip" % spider_name, "rb").read())
    post_data = {'username': username, 'password': password, 'name':
                 spider_name, 'zipfile': zipf}
    if spider_website:
        post_data['website'] = spider_website
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    h = Http()
    resp, content = h.request(
        url, "POST", body=urlencode(post_data), headers=headers)
    # read zip file
    return content


def deploy_spider():
    parser = argparse.ArgumentParser()
    parser.add_argument('url')
    parser.add_argument('username')
    parser.add_argument('password')
    parser.add_argument('spider_dir')

    args = parser.parse_args()
    result = deploy(args.url, args.username, args.password, args.spider_dir)
    print result


if __name__ == "__main__":
    deploy_spider()
