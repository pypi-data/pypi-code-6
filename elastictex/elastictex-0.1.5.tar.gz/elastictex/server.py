#!/usr/bin/env python
from elastictex import api
from flask import Flask, request, render_template

app = Flask(__name__, )


def main():
    try:
        with open("./.elastictex", "r") as f:
            host = f.read().strip()
    except:
        host = "localhost:9200"

    print(host)
    api.init(host)
    app.run(debug=True, post=9999)


@app.route('/')
def get():
    results = None
    q = request.args.get('q')
    if q:
        results = api.search(q)
    return render_template("index.html",
                           results=results)


@app.route('/upload', methods=['POST'])
def post():
    url = request.args.get('url')
    if url is None:
        return "Invalid URL"
    else:
        api.index(url, request.data)
        return "Indexed %s\n" % url


if __name__ == "__main__":
    main()
