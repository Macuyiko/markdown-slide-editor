from mdx.renderer import postprocess_pages, render_text_with_view


def render(text, view="slide-view list"):
    return render_text_with_view(text, view)["html"]


def test_pages_are_split_on_horizontal_rules():
    html = render("# One\n\n---\n\n# Two")
    assert html.count('class="slide-wrapper') == 2
    assert 'id="page_1"' in html
    assert 'id="page_2"' in html


def test_first_page_number_hidden_by_default():
    html = render("# One\n\n---\n\n# Two")
    assert 'data-page-number="false"' in html
    assert '<span class="slide-page" data-page="2">2</span>' in html


def test_pages_none_hides_all_page_numbers():
    html = render("pages: none\n\n# One\n\n---\n\n# Two")
    assert 'data-page-number="true"' not in html
    assert html.count('data-page-number="false"') == 2


def test_footer_meta_is_rendered_on_every_page():
    html = render("footer: My Footer\n\n# One\n\n---\n\n# Two")
    assert html.count('<footer class="slide-footer">My Footer</footer>') == 2


def test_empty_inline_attributes_produce_plain_span():
    html = render("[hello]{}")
    assert '<span markdown="1">hello</span>' in html


def test_inline_attributes_with_class():
    html = render("[hello]{.warning}")
    assert 'class="warning"' in html
    assert ">hello</span>" in html


def test_inline_mark_tag():
    html = render("[x]{ /mark }")
    assert "<mark" in html
    assert ">x</mark>" in html


def test_background_images_become_slide_backgrounds():
    html = render("# One\n\n![bg](https://example.com/bg.jpg)\n")
    assert 'class="slide-bg-img"' in html
    assert 'background-image: url("https://example.com/bg.jpg")' in html
    assert '<img src="https://example.com/bg.jpg"' not in html


def test_background_url_with_spaces_is_quoted():
    html = render(
        "work-dir: 0 - About the Course\n\n![bg](/file/fig/nasa.jpg?)"
    )
    assert 'url("/file/0 - About the Course/fig/nasa.jpg?")' in html


def test_image_sizing_and_opacity_from_alt_tokens():
    html = render("![s50% o30%](https://example.com/i.png)", "doc-view")
    assert "zoom: 0.5;" in html
    assert "opacity: 0.3;" in html


def test_headings_only_slide_is_tagged():
    assert "only-headings" in render("# Just a heading")


def test_blockquotes_only_slide_is_tagged():
    assert "only-blockquotes" in render("> A quote")


def test_file_urls_are_prefixed_with_work_dir():
    html = render("work-dir: decks/test\n\n![a](/file/i.png)")
    assert 'src="/file/decks/test/i.png"' in html


def test_file_urls_are_not_prefixed_twice():
    html = render("work-dir: sub\n\n![a](/file/sub/i.png)")
    assert 'src="/file/sub/i.png"' in html
    assert "/file/sub/sub/" not in html


def test_file_urls_untouched_without_work_dir():
    html = render("![a](/file/i.png)")
    assert 'src="/file/i.png"' in html


def test_render_result_metadata():
    result = render_text_with_view("slide-theme: dark\n\n# X", "slide-view list")
    assert result["slide_theme"] == "dark"
    assert result["code_theme"] == "default"
    assert result["work_dir"] == "."
    assert result["view"] == "slide-view list"


def test_postprocess_pages_without_meta():
    html = postprocess_pages("<p>a</p><hr/><p>b</p>")
    assert 'id="page_1" data-page-number="false"' in html
    assert 'id="page_2" data-page-number="true"' in html
