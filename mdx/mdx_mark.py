"""
Mark using ==

"""

import markdown
from markdown.inlinepatterns import SimpleTagPattern
import re

MARK_RE = r"(==)([^=]+)\2"

class MarkExtension(markdown.Extension):
    def extendMarkdown(self, md):
        md.registerExtension(self)
        md.inlinePatterns.register(SimpleTagPattern(MARK_RE, "mark"), "mark", 65)

def makeExtension(*args, **kwargs):
    return MarkExtension(*args, **kwargs)
