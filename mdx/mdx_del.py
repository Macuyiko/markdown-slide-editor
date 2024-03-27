"""
Del using @@

"""

import markdown
from markdown.inlinepatterns import SimpleTagPattern
import re

DEL_RE = r"(@@)([^@]+)\2"

class DelExtension(markdown.Extension):
    def extendMarkdown(self, md):
        md.registerExtension(self)
        md.inlinePatterns.register(SimpleTagPattern(DEL_RE, "del"), "del",  65)

def makeExtension(*args, **kwargs):
    return DelExtension(*args, **kwargs)
