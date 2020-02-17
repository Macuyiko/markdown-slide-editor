from flask import Flask
from flask import render_template
from flask import request
from flask import jsonify
from flask import url_for
from flask import send_file
from flask_jsglue import JSGlue
from mdx.renderer import render_text_with_view
from os import getcwd, chdir

app = Flask(__name__)
jsglue = JSGlue(app)
initial_directory = getcwd()

@app.after_request
def add_header(r):
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r

def handle_workdir(rendered):
    work_dir = rendered.get('work_dir', None)
    try:
        if work_dir:
            print("Changing working directory to:", work_dir)
            chdir(initial_directory + '/' + work_dir)
        else:
            print("Changing working directory to:", initial_directory)
            chdir(initial_directory)
    except FileNotFoundError:
        print("Could not change working directory")

@app.route("/")
def home():
    return render_template('index.html')

@app.route("/save", methods=['POST'])
def save():
    json = request.get_json()
    text = json['text']
    filename = json['filename']
    with open(filename, 'w', encoding='utf-8', newline='') as f:
        f.write(text)
    return jsonify({ 'status': 'ok' })

@app.route("/preview", methods=['GET', 'POST'])
@app.route("/preview/<view>", methods=['GET', 'POST'])
def preview(view=None, auto_print=False, auto_full=False):
    text = request.form.get('text')
    rendered = render_text_with_view(text, view)
    handle_workdir(rendered)
    return render_template('preview.html', **rendered, auto_print=auto_print, auto_full=auto_full)

@app.route("/print", methods=['GET', 'POST'])
@app.route("/print/<view>", methods=['GET', 'POST'])
def print_preview(view=None):
    return preview(view, auto_print=True)

@app.route("/present", methods=['GET', 'POST'])
@app.route("/present/<view>", methods=['GET', 'POST'])
def present_preview(view=None):
    return preview(view, auto_full=True)

@app.route("/file/<path:location>")
def file(location):
    return send_file(getcwd() + '/' + location)

@app.route("/render", methods=['POST'])
def render():
    json = request.get_json()
    text = json.get('text')
    view = json.get('view')
    rendered = render_text_with_view(text, view)
    handle_workdir(rendered)
    return jsonify(rendered)

if __name__ == '__main__':
    app.run(debug=True, port=5454)