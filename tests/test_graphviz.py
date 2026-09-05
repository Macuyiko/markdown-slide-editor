import shutil
from pathlib import Path

import pytest

from mdx.mdx_inline_graphviz import GRAPHVIZ_BIN_ENV, find_graphviz_executable
from mdx.renderer import render_text_with_view

DOT = shutil.which("dot")
requires_dot = pytest.mark.skipif(DOT is None, reason="graphviz dot not installed")


def test_unknown_executable_returns_none(monkeypatch):
    monkeypatch.delenv(GRAPHVIZ_BIN_ENV, raising=False)
    assert find_graphviz_executable("definitely-not-a-graphviz-tool") is None


@requires_dot
def test_env_var_takes_precedence(monkeypatch):
    monkeypatch.setenv(GRAPHVIZ_BIN_ENV, str(Path(DOT).parent))
    found = find_graphviz_executable("dot")
    assert found is not None
    assert Path(found).parent == Path(DOT).parent


@requires_dot
def test_bogus_env_var_falls_back_to_path(monkeypatch):
    monkeypatch.setenv(GRAPHVIZ_BIN_ENV, r"C:\definitely\not\a\real\dir")
    found = find_graphviz_executable("dot")
    assert found is not None
    assert Path(found).exists()


def render(text):
    return render_text_with_view(text, None)["html"]


def test_unsupported_command_keeps_raw_block():
    html = render("{% notacommand out.svg\ndigraph G { a -> b }\n%}")
    assert "{% notacommand" in html


def test_unsupported_filetype_keeps_raw_block():
    html = render("{% dot out.gif\ndigraph G { a -> b }\n%}")
    assert "{% dot" in html


@requires_dot
def test_svg_output_is_rendered_inline():
    html = render("{% dot plan.svg\ndigraph G { a -> b }\n%}")
    assert 'class="graphviz"' in html
    assert "<svg" in html


@requires_dot
def test_png_output_is_rendered_as_data_uri():
    html = render("{% dot plan.png\ndigraph G { a -> b }\n%}")
    assert "data:image/png;base64" in html
