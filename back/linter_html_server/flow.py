from typing import List


class ParseError(Exception):
    pass


class NodeError(Exception):
    pass


class LinterErrorMessage:

    def __init__(self, lines: List[str], linenum: int):
        self.lines = lines
        self.linenum = linenum


class Node:

    def __init__(self, name):
        self.name = name
        self.children = []
        self.messages = []

    def child(self, name, create=False):
        for child in self.children:
            if child.name == name:
                return child
        else:
            if create:
                child = Node(name)
                self.children.append(child)
                return child
            else:
                raise NodeError(f'Node {self.name} has no child {name}')

    def as_dict(self):
        return {
            'name': self.name,
            'children': [ child.as_dict() for child in self.children ],
            'errors': [[line.replace(' ', '\u00A0') for line in m.lines] for m in self.messages]
        }


def add_message(root: Node, path: List[str], msg):
    node = root
    for name in path:
        node = node.child(name, create=True)
    node.messages.append(msg)


def parse_header(header):
    # something like:
    # Error: src/components/DateLabel/index.js:12
    words = header.split()
    if len(words) != 2 or words[0] != 'Error:':
        raise ParseError
    filepath, linenum = words[1].split(':')
    return filepath, int(linenum)


def extract_errors(flow_output):
    root = Node('root')

    for error in flow_output.split('\n\n'):
        lines = error.strip().split('\n')
        try:
            filepath, linenum = parse_header(lines[0])
        except ParseError:
            # Ignore output that is not flow error.
            # For example, flow stdout ends with the line: 'Found 92 errors'
            continue

        msg = LinterErrorMessage(lines[1:], linenum)
        path = filepath.split('/')

        add_message(root, path, msg)

    if len(root.children) == 1:
        root = root.children[0]
    return root.as_dict()
