"""
Subscript using ~

"""

import markdown
from markdown.inlinepatterns import SimpleTagPattern
from markdown.util import etree
import re

SUBSCRIPT_RE = r"(\~)([^\~]+)\2"

class SubscriptExtension(markdown.Extension):
    def extendMarkdown(self, md):
        md.registerExtension(self)
        md.inlinePatterns.add("subscript", SimpleTagPattern(SUBSCRIPT_RE, "sub"), "<not_strong")

def makeExtension(*args, **kwargs):
    return SubscriptExtension(*args, **kwargs)
