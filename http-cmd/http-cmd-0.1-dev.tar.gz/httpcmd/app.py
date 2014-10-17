from flask import Flask


app = Flask(__name__)


def run_cmd():
    app.run()


if __name__ == '__main__':
    run_cmd()
