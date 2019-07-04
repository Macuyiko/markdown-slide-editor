"""
HTML inlines

Usage: [Text content: will be Markdown formatted]{ attributes to use }

Examples:

[A normal span tag with a class]{ .warning }
[A mark tag]{ /mark }
[A del tag]{ /del }

"""

import markdown
from markdown.util import etree
import re
from tag_attribute_parser import parse_attribute_string, attributes_to_element

LINE_RE = r'\[(?P<content>.*?)\](?P<attributes>\{.*?\})'

class HtmlInlineExtension(markdown.Extension):
    def extendMarkdown(self, md):
        md.registerExtension(self)
        # 21 > 20 ('html_block') to make sure we ignore block parsing
        md.inlinePatterns.register(HtmlInlineProcessor(LINE_RE), 'html_attribute_inline', 21)

class HtmlInlineProcessor(markdown.inlinepatterns.InlineProcessor):
    def handleMatch(self, m, data):
        parsed = parse_attribute_string(m.group('attributes'))
        el = attributes_to_element(parsed, default='span') if parsed else etree.Element('span')
        el.text = m.group('content')
        return el, m.start(0), m.end(0)


def makeExtension(*args, **kwargs):
    return HtmlInlineExtension(*args, **kwargs)
