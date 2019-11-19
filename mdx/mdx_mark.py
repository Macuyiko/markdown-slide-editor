"""
Mark using ==

"""

import markdown
from markdown.inlinepatterns import SimpleTagPattern
from markdown.util import etree
import re

MARK_RE = r"(==)([^=]+)\2"

class MarkExtension(markdown.Extension):
    def extendMarkdown(self, md):
        md.registerExtension(self)
        md.inlinePatterns.add("mark", SimpleTagPattern(MARK_RE, "mark"), "<not_strong")

def makeExtension(*args, **kwargs):
    return MarkExtension(*args, **kwargs)
