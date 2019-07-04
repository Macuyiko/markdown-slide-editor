"""
HTML blocks

Usage:

::: { attributes }

::: 

or

::: { ClassName }

::: 

or

::: { attributes /section }

::: { attributes /section/ }

"""

import markdown
import re
from tag_attribute_parser import parse_attribute_string, attributes_to_tag

LINE_RE = re.compile(r'^:{3,}\s*(?P<attributes>\{.*?\}|\S*?)\s*$')

class HtmlBlockExtension(markdown.Extension):
    def extendMarkdown(self, md):
        md.registerExtension(self)
        # 21 > 20 ('html_block') to make sure we ignore block parsing
        md.preprocessors.register(HtmlBlockPreprocessor(md), 'html_attribute_block', 21)

class HtmlBlockPreprocessor(markdown.preprocessors.Preprocessor):
    def __init__(self, md):
        super().__init__(md)

    def run(self, lines):
        new_lines = []
        for line in lines:
            m = LINE_RE.search(line)
            if m:
                parsed = parse_attribute_string(m.group('attributes'))
                line = attributes_to_tag(parsed) if parsed else '</div>'
                if new_lines[-1].strip() != '':
                    new_lines.append('')
            new_lines.append(line)
        return new_lines


def makeExtension(*args, **kwargs):
    return HtmlBlockExtension(*args, **kwargs)
