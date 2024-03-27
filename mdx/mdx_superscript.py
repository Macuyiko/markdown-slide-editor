"""
Superscript using ^

"""

import markdown
from markdown.inlinepatterns import SimpleTagPattern
import re

SUPERSCRIPT_RE = r"(\^)([^\^]+)\2"

class SuperscriptExtension(markdown.Extension):
    def extendMarkdown(self, md):
        md.registerExtension(self)
        md.inlinePatterns.register(SimpleTagPattern(SUPERSCRIPT_RE, "sup"), "superscript", 65)

def makeExtension(*args, **kwargs):
    return SuperscriptExtension(*args, **kwargs)
