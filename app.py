from flask import Flask
from flask import render_template
from flask import request
from flask import jsonify
from flask import url_for
from flask_jsglue import JSGlue
from mdx.renderer import render_text_with_view

app = Flask(__name__)
jsglue = JSGlue(app)

@app.after_request
def add_header(r):
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r

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
    return render_template('preview.html', **render_text_with_view(text, view), auto_print=auto_print, auto_full=auto_full)

@app.route("/print", methods=['GET', 'POST'])
@app.route("/print/<view>", methods=['GET', 'POST'])
def print(view=None):
    return preview(view, auto_print=True)

@app.route("/present", methods=['GET', 'POST'])
@app.route("/present/<view>", methods=['GET', 'POST'])
def present(view=None):
    return preview(view, auto_full=True)

@app.route("/render", methods=['POST'])
def render():
    json = request.get_json()
    text = json.get('text')
    view = json.get('view')
    return jsonify(render_text_with_view(text, view))

if __name__ == '__main__':
    app.run(debug=True)