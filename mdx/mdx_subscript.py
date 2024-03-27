"""
Subscript using ~

"""

import markdown
from markdown.inlinepatterns import SimpleTagPattern
import re

SUBSCRIPT_RE = r"(\~)([^\~]+)\2"

class SubscriptExtension(markdown.Extension):
    def extendMarkdown(self, md):
        md.registerExtension(self)
        md.inlinePatterns.register(SimpleTagPattern(SUBSCRIPT_RE, "sub"), "subscript", 65)

def makeExtension(*args, **kwargs):
    return SubscriptExtension(*args, **kwargs)
