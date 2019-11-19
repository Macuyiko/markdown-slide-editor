import os, sys
my_env = os.environ
my_env["PATH"] = "C:\\Program Files (x86)\\Graphviz2.38\\bin\\" + os.pathsep + my_env["PATH"]
sys.path.append(os.path.dirname(__file__))

import markdown
import codecs
import re
from bs4 import BeautifulSoup

extensions = [
    'extra', 'codehilite', 'smarty', 'meta', 'nl2br',
    'mdx_math', 'mdx_inline_graphviz', 
    'mdx_attribute_block', 'mdx_attribute_inline', 'mdx_image_inline',
    'mdx_subscript', 'mdx_superscript', 'mdx_mark', 'mdx_del'
]

extension_configs = {
    'mdx_math': {
        'enable_dollar_delimiter': True,
        'add_preview': True
    }
}

percentage_regex = r'^s?(\d+(?:\.\d+)?)%$'
opacity_regex    = r'^o(\d+(?:\.\d+)?)%$'

def extract_percentage(text, rgx=None):
    if rgx is None:
        rgx = percentage_regex
    search = re.match(rgx, text)
    if search:
        return search.group(1)
    return False

def get_meta_or_default(meta, name, default):
    if not meta or not name in meta or not meta[name] or not meta[name][0]:
        return default
    return meta[name][0]

def render_text_with_view(text=None, view=None, also_postprocess=True):
    if view is None:
        view = 'slide-view list'
    md = markdown.Markdown(extensions=extensions)
    md.Meta = None
    html = md.convert(text) if text else ''
    meta = md.Meta
    slide_theme = get_meta_or_default(meta, 'slide-theme', 'default')
    code_theme  = get_meta_or_default(meta, 'code-theme', 'default')
    working_directory = get_meta_or_default(meta, 'work-dir', '.')
    if text and also_postprocess:
        html = postprocess(html, meta, view)
    return {
        'html': html,
        'meta': meta,
        'view': view,
        'slide_theme': slide_theme,
        'code_theme':  code_theme,
        'work_dir': working_directory
    }

def postprocess_pages(html, with_pages='allbutfirst', with_footer=''):
    pages = re.compile(r'<hr\s?\/?>').split(html)
    output = ''
    for p, page in enumerate(pages):
        page_num = p+1
        page_num_str = p+1
        page_num_data = 'true'
        if (with_pages == 'allbutfirst' and page_num == 1) or with_pages == 'none':
            page_num_str = ''
            page_num_data = 'true'
        output += '<div class="slide-wrapper" id="page_{}" data-page-number="{}">'.format(page_num, page_num_data)
        output += '<div class="slide"><div class="slide-bg"></div><div class="slide-inner">'
        output += page
        output += '</div>'
        output += '<footer class="slide-footer">{}</footer>'.format(with_footer)
        output += '<span class="slide-page" data-page="{}">{}</span></div></div>'.format(page_num, page_num_str)
    return output

def postprocess_backgrounds(html):
    h = BeautifulSoup(html, 'html.parser')
    for background_image in h.select('p > img[alt~="bg"]'):
        url = background_image.get('src', None)
        if url is None:
            continue
        alt = background_image.get('alt', '')
        parent_p = background_image.find_parent('p')
        parent_wrapper_bg = background_image.find_parent(class_='slide-wrapper').find(class_='slide-bg')
        new_style = "background-image: url({});".format(url)
        for alt_piece in re.compile(r'\s+').split(alt):
            percentage = extract_percentage(alt_piece)
            if percentage:
                new_style += "background-size: {}%;".format(percentage)
            percentage = extract_percentage(alt_piece, opacity_regex)
            if percentage:
                new_style += "opacity: {};".format(float(percentage) / 100.0)
        new_div = h.new_tag("div", **{'class': "slide-bg-img", 'style': new_style, 'data-alt': alt})
        parent_wrapper_bg.append(new_div)
        background_image.decompose()
        if not parent_p.find(lambda x : x.name != 'br') and not parent_p.get_text(strip=True):
            parent_p.decompose()
    return str(h)

def postprocess_images(html):
    h = BeautifulSoup(html, 'html.parser')
    for image in h.select('img[alt*="%"]'):
        alt = image.get('alt', '')
        for alt_piece in re.compile(r'\s+').split(alt):
            percentage = extract_percentage(alt_piece)
            if percentage:
                image['style'] = image.get('style', '') + "; zoom: {};".format(float(percentage) / 100.0)
            percentage = extract_percentage(alt_piece, opacity_regex)
            if percentage:
                image['style'] = image.get('style', '') + "; opacity: {};".format(float(percentage) / 100.0)
    return str(h)

def postprocess_only_elements(html):
    h = BeautifulSoup(html, 'html.parser')
    for slide_wrapper in h.select('.slide-wrapper'):
        inner = slide_wrapper.select('.slide > .slide-inner')
        if not inner:
            continue
        inner = inner[0]
        inner_children = inner.find_all(text=False, recursive=False)
        innerContents = [el for el in inner_children \
            if el.name not in ['base', 'link', 'meta', 'noscript', 'script', 'style', 'template', 'title']]
        innerHeads  = [el for el in inner_children if el.name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']]
        innerQuotes = [el for el in inner_children if el.name in ['blockquote']]
        if len(innerHeads) > 0 and len(innerContents) == len(innerHeads):
            slide_wrapper['class'] = slide_wrapper.get('class', []) + ["only-headings"]
        if len(innerQuotes) > 0 and len(innerContents) == len(innerQuotes):
            slide_wrapper['class'] = slide_wrapper.get('class', []) + ["only-blockquotes"]
    return str(h)

def postprocess(html, meta, view='slide-view list'):
    post = html
    with_pages = get_meta_or_default(meta, 'pages', 'allbutfirst').lower()
    with_footer = get_meta_or_default(meta, 'footer', '')
    if 'slide-view' in view:
        post = postprocess_pages(post, with_pages, with_footer)
        post = postprocess_backgrounds(post)
    post = postprocess_images(post)
    post = postprocess_only_elements(post)
    return post

