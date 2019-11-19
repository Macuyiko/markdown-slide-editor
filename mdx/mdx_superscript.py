"""
Superscript using ^

"""

import markdown
from markdown.inlinepatterns import SimpleTagPattern
from markdown.util import etree
import re

SUPERSCRIPT_RE = r"(\^)([^\^]+)\2"

class SuperscriptExtension(markdown.Extension):
    def extendMarkdown(self, md):
        md.registerExtension(self)
        md.inlinePatterns.add("superscript", SimpleTagPattern(SUPERSCRIPT_RE, "sup"), "<not_strong")

def makeExtension(*args, **kwargs):
    return SuperscriptExtension(*args, **kwargs)
