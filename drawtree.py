#!/usr/bin/env python3

import re
import sys
from textwrap import dedent
from typing import Tuple

INDENTATION = re.compile(r'^(\s*)(.+)')

BranchId = Tuple[int, ...]
Outline = dict[BranchId, str]


def sibling(branch: BranchId) -> BranchId:
    return branch[:-1] + (branch[-1] + 1,)


def parent(branch: BranchId) -> BranchId:
    return branch[:-1]


def child(branch: BranchId) -> BranchId:
    return branch + (0,)


class Tree:
    def __init__(
        self,
        outline: Outline | None,
        *,
        indent_char: str = ' ',
        indent_len: int = 1,
    ):
        self.indent_char = indent_char
        self.indent_len = indent_len
        self.outline = {} if outline is None else outline

    def indent(self, branch):
        if len(branch) < 2:
            return ''
        else:
            indents = []
            for level in range(2, len(branch)):
                ancestor = branch[:level]
                if sibling(ancestor) in self.outline:
                    indents.append('│' + (self.indent_len - 1) * self.indent_char)
                else:
                    indents.append(self.indent_len * self.indent_char)
            return ''.join(indents)

    def connector(self, branch: BranchId) -> str:
        if sibling(branch) in self.outline:
            wire = '├'
        else:
            wire = '└'
        return wire + ('─' * self.indent_len)[1:]

    def draw_line(self, branch):
        if len(branch) < 2:
            return self.outline[branch]

        return (
            self.indent(branch) + self.connector(branch) + self.outline[branch]
        )

    def draw(self):
        return [self.draw_line(branch) for branch in self.outline]

    @classmethod
    def from_text(cls, text: str) -> 'Tree':
        text = dedent(text).strip()
        indent_char, indent_len = '', 0
        outline = {}
        branch: BranchId = (0,)
        level = 0
        for line in text.split('\n'):
            indent, label = INDENTATION.match(line).groups() # type: ignore[union-attr]
            if indent and indent_char == '':
                indent_char = indent[0]
                indent_len = len(indent)
            if indent:
                for char in indent:
                    if char != indent_char:
                        raise ValueError(
                            f'unexpected indent char {char!r} at {label!r}'
                        )
                if len(indent) % indent_len:
                    raise ValueError(f'inconsistent indentation at {label!r}')
                new_level = len(indent) // indent_len
                if new_level == (level + 1):
                    branch = child(branch)
                elif new_level == level:
                    branch = sibling(branch)
                elif new_level < level:
                    branch = sibling(branch[: new_level + 1])
                else:
                    raise ValueError(f'excessive indentation at {label!r}')

                level = new_level
            outline[branch] = label

        return cls(outline, indent_char=indent_char, indent_len=indent_len)


def main():
    if len(sys.argv) != 2:
        print(f'Usage:\t{sys.argv[0]} <filename>')
        sys.exit(1)
    with open(sys.argv[1]) as fp:
        text = fp.read()
    for line in Tree.from_text(text).draw():
        print(line)


if __name__ == '__main__':
    main()
