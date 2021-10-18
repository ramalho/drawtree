#!/usr/bin/env python3

from importlib import import_module
import sys

SP =    '\N{SPACE}'
HLIN =  '\N{BOX DRAWINGS LIGHT HORIZONTAL}'                       # ─
ELBOW = f'\N{BOX DRAWINGS LIGHT UP AND RIGHT}{HLIN*2}{SP}'        # └──
TEE =   f'\N{BOX DRAWINGS LIGHT VERTICAL AND RIGHT}{HLIN*2}{SP}'  # ├──
PIPE =  f'\N{BOX DRAWINGS LIGHT VERTICAL}{SP*3}'                  # │


def tree(cls, level=0, last_sibling=True):
    yield cls, level, last_sibling
    try:
        subclasses = cls.__subclasses__()
    except TypeError:  # handle the `type` type
        subclasses = cls.__subclasses__(cls)
    if subclasses:
        last = subclasses[-1]
        for sub in subclasses:
            yield from tree(sub, level + 1, sub is last)


def render_lines(tree_iter):
    cls, _, _ = next(tree_iter)
    yield cls.__name__
    prefix = ''

    for cls, level, last in tree_iter:
        prefix = prefix[: 4 * (level - 1)]
        prefix = prefix.replace(TEE, PIPE).replace(ELBOW, SP * 4)
        prefix += ELBOW if last else TEE
        yield prefix + cls.__name__


def draw(cls):
    for line in render_lines(tree(cls)):
        print(line)


def main():
    if len(sys.argv) != 2:
        print(
            f'Usage:\t{sys.argv[0]} Class         # for builtins\n'
            f'\t{sys.argv[0]} module.Class  # for the rest'
        )
        sys.exit(1)
    if '.' in sys.argv[1]:
        parts = sys.argv[1].split('.')
        *module_parts, cls_name = parts
        module = import_module('.'.join(module_parts))
        cls = getattr(module, cls_name)
    else:
        module = __builtins__
        cls = getattr(module, sys.argv[1])
    draw(cls)


if __name__ == '__main__':
    main()
