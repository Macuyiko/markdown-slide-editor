"""
Graphviz extensions for Markdown.
Renders the output inline, eliminating the need to configure an output
directory.

Supports outputs types of SVG and PNG. The output will be taken from the
filename specified in the tag. Example:

{% dot attack_plan.svg
    digraph G {
        rankdir=LR
        Earth [peripheries=2]
        Mars
        Earth -> Mars
    }
%}

Requires the graphviz library (http://www.graphviz.org/)

Inspired by jawher/markdown-dot (https://github.com/jawher/markdown-dot)

Modified to work with Python 3 and cleaned-up SVG output
"""

import re
import markdown
import subprocess
import base64

# Global vars
BLOCK_RE = re.compile(
    r'^\{% (?P<command>\w+)\s+(?P<filename>[^\s]+)\s*\n(?P<content>.*?)%}\s*$',
    re.MULTILINE | re.DOTALL)
# Command whitelist
SUPPORTED_COMMAMDS = ['dot', 'neato', 'fdp', 'sfdp', 'twopi', 'circo']


class InlineGraphvizExtension(markdown.Extension):

    def extendMarkdown(self, md):
        """ Add InlineGraphvizPreprocessor to the Markdown instance. """
        md.registerExtension(self)
        md.preprocessors.register(InlineGraphvizPreprocessor(md), 'graphviz_block', 1)


class InlineGraphvizPreprocessor(markdown.preprocessors.Preprocessor):

    def __init__(self, md):
        super().__init__(md)

    def run(self, lines):
        """ Match and generate dot code blocks."""

        text = "\n".join(lines)
        while 1:
            m = BLOCK_RE.search(text)
            if m:
                command = m.group('command')
                # Whitelist command, prevent command injection.
                if command not in SUPPORTED_COMMAMDS:
                    raise Exception('Command not supported: %s' % command)
                filename = m.group('filename')
                content = m.group('content').encode()
                filetype = filename[filename.rfind('.')+1:]

                args = [command, '-T'+filetype]
                try:
                    proc = subprocess.Popen(
                        args,
                        stdin=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        stdout=subprocess.PIPE)
                    proc.stdin.write(content)

                    output, err = proc.communicate()

                    if filetype == 'svg':
                        data_url_filetype = 'svg+xml'
                        encoding = 'utf-8'
                        img = output.decode(encoding)
                        # Remove graphviz XML header
                        img = re.sub(r'\<\?xml.+?\?\>', '', img, flags=re.DOTALL)
                        img = re.sub(r'\<\!DOCTYPE.+?\>', '', img, flags=re.DOTALL)
                        img = '<div class="graphviz">' + img.replace('\n', '') + "</div>"
                        
                    if filetype == 'png':
                        data_url_filetype = 'png'
                        encoding = 'base64'
                        output = base64.b64encode(output)
                        data_path = "data:image/%s;%s,%s" % (
                            data_url_filetype,
                            encoding,
                            output)
                        img = "![" + filename + "](" + data_path + ")"

                    text = '%s\n%s\n%s' % (
                        text[:m.start()], img, text[m.end():])

                except Exception as e:
                    import traceback
                    import sys
                    traceback.print_exc(file=sys.stdout)
                    break

            else:
                break
        return text.split("\n")


def makeExtension(*args, **kwargs):
    return InlineGraphvizExtension(*args, **kwargs)
