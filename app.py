#!/usr/bin/python3

import flask
import jinja2
import argparse
import os

TEMPLATE_DIR = "templates"

app = flask.Flask(__name__)

class Loader(jinja2.BaseLoader):
    '''
    Simple loader that just retrieves the template file from the given path.
    '''

    def __init__(self, path):
        '''
        * path: path (full or relative) to templates directory.
        '''
        self.path = path

    def get_source(self, environment, template):
        path = os.path.join(self.path, template)
        if not os.path.exists(path):
            raise jinja2.TemplateNotFound(template)
        mtime = os.path.getmtime(path)
        with open(path, 'r') as f:
            src = f.read()
        return src, path, lambda: mtime == os.path.getmtime(path)

env = jinja2.Environment(loader=Loader(TEMPLATE_DIR), autoescape=jinja2.select_autoescape(['html']))

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--address", default="127.0.0.1")
    parser.add_argument("-p", "--port", default=8080, type=int)
    return parser.parse_args()

@app.route("/", methods=["GET"])
def hello():
    return "Aloha, brother."

@app.route("/madlibs", methods=["GET"])
def madlibs():
    template = env.get_template("madlibs.html")
    try:
        with open("static/text/lorem_ipsum.txt") as f:
            lorem_ipsum = f.read()
    except FileNotFoundError:
        return flask.make_response("Could not find text", 404)
    css_url = flask.url_for("static", filename="css/style.css")
    js_url = flask.url_for("static", filename="js/app.js")
    words = lorem_ipsum.split(' ')
    descriptors = []
    for w in words:
        word = w.lower()
        if word and word[0] == '[' and word[-1] == ']':
            descriptors.append(word[1].upper() + word[2:-1])
    return template.render(words=lorem_ipsum.split(' '), descriptors=descriptors, css_url=css_url, js_url=js_url)


if __name__ == "__main__":
    args = parse_args()
    app.run(host=args.address, port=args.port)