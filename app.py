from flask import Flask
from flask import render_template
from flask import request
from flask import jsonify
from flask import send_file
from flask import abort
import jinja2
from markupsafe import Markup

# Monkeypatch to make flask_jsglue work
jinja2.Markup = Markup

from flask_jsglue import JSGlue
from mdx.renderer import render_text_with_view
import os
from os import getcwd

app = Flask(__name__)
jsglue = JSGlue(app)
initial_directory = getcwd()

RESOLUTION = "1280x720"


@app.after_request
def add_header(r):
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers["Cache-Control"] = "public, max-age=0"
    return r


def resolve_in_base(base, relative):
    """Resolve a client-supplied relative path against base, refusing to
    escape the base directory."""
    base_abs = os.path.normcase(os.path.abspath(base))
    joined = os.path.normcase(os.path.abspath(os.path.join(base_abs, relative)))
    if joined != base_abs and not joined.startswith(base_abs + os.sep):
        abort(403)
    return joined


def resolve_workdir(work_dir):
    """Map a deck's work-dir meta to an absolute directory."""
    if not work_dir or work_dir == ".":
        return initial_directory
    return resolve_in_base(initial_directory, work_dir)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/save", methods=["POST"])
def save():
    json = request.get_json()
    text = json["text"]
    filename = json["filename"]
    if not filename:
        abort(400)
    base = resolve_workdir(json.get("work_dir"))
    path = resolve_in_base(base, filename)
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(text)
    return jsonify({"status": "ok"})


@app.route("/p5js", methods=["POST"])
def p5js():
    json = request.get_json()
    script = json["script"]
    return render_template("p5js.html", script=script)


@app.route("/preview", methods=["GET", "POST"])
@app.route("/preview/<view>", methods=["GET", "POST"])
def preview(view=None, auto_print=False, auto_full=False):
    text = request.form.get("text")
    rendered = render_text_with_view(text, view)
    return render_template(
        "preview.html",
        **rendered,
        auto_print=auto_print,
        auto_full=auto_full,
        resolution=RESOLUTION
    )


@app.route("/print", methods=["GET", "POST"])
@app.route("/print/<view>", methods=["GET", "POST"])
def print_preview(view=None):
    return preview(view, auto_print=True)


@app.route("/present", methods=["GET", "POST"])
@app.route("/present/<view>", methods=["GET", "POST"])
def present_preview(view=None):
    return preview(view, auto_full=True)


@app.route("/file/<path:location>")
def file(location):
    path = resolve_in_base(initial_directory, location)
    if not os.path.isfile(path):
        abort(404)
    return send_file(path)


@app.route("/render", methods=["POST"])
def render():
    json = request.get_json()
    text = json.get("text")
    view = json.get("view")
    rendered = render_text_with_view(text, view)
    return jsonify(rendered)


if __name__ == "__main__":
    app.run(debug=True, port=5010)
