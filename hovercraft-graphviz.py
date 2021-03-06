from docutils import nodes
from docutils.parsers.rst import Directive, directives

import hovercraft
import sys

import subprocess
import base64

class Dot(Directive):
    required_arguments = 0
    optional_arguments = 0
    has_content = True
    final_argument_whitespace = True
    option_spec = {
        'height': directives.unchanged,
        'width': directives.unchanged
    }

    '''dot image generator'''
    def run(self):
        self.assert_has_content()
        p = subprocess.Popen(['dot', '-Tsvg'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, encoding="utf8")
        p.stdin.write('\n'.join(self.content))
        img = p.communicate()[0]
        p.stdin.close()
        ret = p.wait()
        if ret:
            return [nodes.error('some error occured')]
        else:
            image = img[img.find("viewBox"):]
            height = self.options.get("height", "100%")
            width = self.options.get("width", "100%")
            return [nodes.raw('', f"<svg class=\"dot\" height=\"{height}\" width=\"{width}\" {image}", format='html')]

directives.register_directive('dot', Dot)


if __name__ == "__main__":
    hovercraft.main(sys.argv[1:])