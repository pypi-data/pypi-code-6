import argparse
import random
import webbrowser

from __init__ import __version__, app

def run():
    description = "Simple markdown viewer."
    parser = argparse.ArgumentParser(description=description)

    parser.add_argument("filename")
    parser.add_argument("-x", "--extensions", help=("markdown extensions"
                        " separated by commas"))
    parser.add_argument('--version', action="version",
                        version="%(prog)s " + __version__)
    args = parser.parse_args()
    app.config['filename'] = args.filename
    app.config['extensions'] = None
    if args.extensions:
        app.config['extensions'] = args.extensions.split(',')


    port = random.randrange(1024,2**16)
    port = 5000
    app.config['DEBUG'] = True
    #webbrowser.open('http://localhost:%d/' % port)
    app.run(debug=True, use_reloader=False, port=port)

if __name__ == '__main__':
    run()
