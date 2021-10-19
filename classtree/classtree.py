#!/usr/bin/env python3

from importlib import import_module
import sys


SP    = '\N{SPACE}'
HLIN  = '\N{BOX DRAWINGS LIGHT HORIZONTAL}'                       # ─
TEE   = f'\N{BOX DRAWINGS LIGHT VERTICAL AND RIGHT}{HLIN*2}{SP}'  # ├──
PIPE  = f'\N{BOX DRAWINGS LIGHT VERTICAL}{SP*3}'                  # │
ELBOW = f'\N{BOX DRAWINGS LIGHT UP AND RIGHT}{HLIN*2}{SP}'        # └──


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


def main(name):
    if '.' in name:
        module_name, cls_name = name.rsplit('.', 1)
    else:
        module_name, cls_name = 'builtins', name
    try:
        module = import_module(module_name)
    except ModuleNotFoundError:
        print(f'*** Could not import {module_name!r}.')
    else:
        try:
            cls = getattr(module, cls_name)
        except AttributeError:
            print(f'*** {cls_name!r} not found in {module.__name__!r}.')
        else:
            if isinstance(cls, type):
                draw(cls)
            else:
                print(f'*** {cls_name!r} is not a class.')


if __name__ == '__main__':
    if len(sys.argv) == 2:
        main(sys.argv[1])
    else:
        print('Usage:'
            f'\t{sys.argv[0]} Class          # for builtins\n'
            f'\t{sys.argv[0]} package.Class  # for the rest'
        )
