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
import sys
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
            if not m:
                break
            command = m.group('command')
            # Whitelist command, prevent command injection.
            if command not in SUPPORTED_COMMAMDS:
                print('Graphviz: command not supported: %s' % command, file=sys.stderr)
                break
            filename = m.group('filename')
            content = m.group('content').encode()
            filetype = filename[filename.rfind('.')+1:].lower()

            if filetype not in ('svg', 'png'):
                print(
                    'Graphviz: unsupported output filetype "%s" (use .svg or .png)' % filetype,
                    file=sys.stderr)
                break

            args = [command, '-T'+filetype]
            try:
                proc = subprocess.run(
                    args,
                    input=content,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE)
            except FileNotFoundError:
                print('Graphviz: executable not found: %s' % command, file=sys.stderr)
                break

            if proc.returncode != 0:
                print(
                    'Graphviz: %s failed:\n%s' % (command, proc.stderr.decode(errors='replace')),
                    file=sys.stderr)
                break

            if filetype == 'svg':
                img = proc.stdout.decode('utf-8')
                # Remove graphviz XML header
                img = re.sub(r'\<\?xml.+?\?\>', '', img, flags=re.DOTALL)
                img = re.sub(r'\<\!DOCTYPE.+?\>', '', img, flags=re.DOTALL)
                img = '<div class="graphviz">' + img.replace('\n', '') + "</div>"
            else:
                data_url_filetype = 'png'
                encoding = 'base64'
                output = base64.b64encode(proc.stdout)
                data_path = "data:image/%s;%s,%s" % (
                    data_url_filetype,
                    encoding,
                    output)
                img = "![" + filename + "](" + data_path + ")"

            text = '%s\n%s\n%s' % (
                text[:m.start()], img, text[m.end():])
        return text.split("\n")


def makeExtension(*args, **kwargs):
    return InlineGraphvizExtension(*args, **kwargs)
