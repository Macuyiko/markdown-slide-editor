# A browser-based Markdown slide editor

The rationale behind developing this basically boils down to me getting increasingly fed up by PowerPoint. As such, I wanted an editor which allowed me to:

- Author slides using Markdown
- Basic theming support focusing more on content than beauty
- Support for Markdown extensions. Mainly tables, Graphviz and math
- Support to deal with image placement, deliberately simple
- Export to PDF support and a simple presentation mode

I considered various HTML/CSS/JS based alternatives such as [Reveal](https://revealjs.com/) and [WebSlides](https://webslides.tv/), but those focus too much on HTML authoring and beauty.

I also heavily used [Marp](https://yhatt.github.io/marp/) in the past, but wanted an alternative since Marp is going full on Node.js nowadays and doesn't support all the functionality I wanted. Nevertheless, a lot of the CSS code was directly taken and modified from Marp -- so strong shoutout to this project!

## Setup

Requires Python 3.12. The easiest way to run it is with [uv](https://docs.astral.sh/uv/):

```sh
uv sync
uv run python app.py
```

Then open <http://localhost:5010>. Alternatively, install the dependencies into any Python 3.12 environment with `pip install .` and start the app with `python app.py`.

Note that this is a local, single-user tool: the Flask server runs with debug mode enabled and is not meant to be exposed to a network.

### Optional: Graphviz

Graph diagrams via `{% dot %}` (and `neato`, `fdp`, `sfdp`, `twopi`, `circo`) blocks require a [Graphviz](https://graphviz.org/) installation. The executables are located through the `GRAPHVIZ_BIN_DIR` environment variable, your `PATH`, or a best-effort scan of the Program Files directories on Windows. Everything else works without Graphviz.

## Usage

Type Markdown on the left and see the slides render live on the right. The most important shortcuts:

| Key | Action |
| --- | --- |
| `Ctrl+S` | Save |
| `Ctrl+O` | Open |
| `Ctrl+L` | New file |
| `Ctrl+V` | Toggle preview layout (list / screen / document) |
| `Ctrl+P` | Print preview (use the browser dialog to export PDF) |
| `F11` | Presentation mode |

See [Example.md](Example.md) for a full overview of the slide syntax: meta keys such as `slide-theme` and `code-theme`, image and background placement, captions, inline HTML attributes, math, Graphviz, p5.js sketches, and the bundled themes.
