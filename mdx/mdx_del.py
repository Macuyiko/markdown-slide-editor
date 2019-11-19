"""
Del using @@

"""

import markdown
from markdown.inlinepatterns import SimpleTagPattern
from markdown.util import etree
import re

DEL_RE = r"(@@)([^@]+)\2"

class DelExtension(markdown.Extension):
    def extendMarkdown(self, md):
        md.registerExtension(self)
        md.inlinePatterns.add("del", SimpleTagPattern(DEL_RE, "del"), "<not_strong")

def makeExtension(*args, **kwargs):
    return DelExtension(*args, **kwargs)
