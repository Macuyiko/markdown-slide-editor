"""
Images with caption

Usage: ![alt text](href){ attributes }

"""

import markdown
import re
from tag_attribute_parser import parse_attribute_string, attributes_to_tag

LINE_RE = re.compile(r'^\!\[(?P<alt>.*?)\]\((?P<href>.*?)\)(?P<attributes>\{.*?\})\s*$')

class ImageInlineExtension(markdown.Extension):
    def extendMarkdown(self, md):
        md.registerExtension(self)
        md.preprocessors.register(ImageInlineProcessor(md), 'captioned_image', 24)

class ImageInlineProcessor(markdown.preprocessors.Preprocessor):
    def __init__(self, md):
        super().__init__(md)

    def run(self, lines):
        new_lines = []
        for line in lines:
            m = LINE_RE.search(line)
            if m:
                alt = m.group('alt').strip()
                href = m.group('href').strip()
                attributes = m.group('attributes').strip()
                parsed = parse_attribute_string(attributes)
                if parsed:
                    if 'caption' in parsed['attrs']:
                        alt = parsed['attrs']['caption']
                    parsed['classes'].append('figure')
                    parsed['attrs']['alt'] = alt
                    parsed['attrs']['markdown'] = 'span'
                    parsed['attrs']['title'] = alt
                    parsed['attrs']['src'] = href
                    parsed['attrs']['tagname'] = None
                    img = attributes_to_tag(parsed, default='img', autoclose=True)
                    parsed['attrs'] = {}
                    div = attributes_to_tag(parsed, default='div', autoclose=False)
                    fig = attributes_to_tag(parsed, default='figure', autoclose=False)
                    md_alt = markdown.Markdown()
                    alt_html = md_alt.convert(alt) if alt else ''
                    line = div + fig + img + '</figure>' + '<figcaption>' + alt_html + '</figcaption>' + '</div>'
            new_lines.append(line)
        return new_lines


def makeExtension(*args, **kwargs):
    return ImageInlineExtension(*args, **kwargs)
