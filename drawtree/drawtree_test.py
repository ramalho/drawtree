from textwrap import dedent

import pytest

from drawtree import sibling, parent, child
from drawtree import Tree


@pytest.mark.parametrize(
    'given, expected',
    [
        [(0,), (1,)],
        [(1, 1), (1, 2)],
    ],
)
def test_sibling(given, expected):
    got = sibling(given)
    assert got == expected


@pytest.mark.parametrize(
    'given, expected',
    [
        [(0, 0), (0,)],
        [(1, 2, 3), (1, 2)],
    ],
)
def test_parent(given, expected):
    got = parent(given)
    assert got == expected


@pytest.mark.parametrize(
    'given, expected',
    [
        [(0,), (0, 0)],
        [(1, 2, 3), (1, 2, 3, 0)],
    ],
)
def test_child(given, expected):
    got = child(given)
    assert got == expected


def test_from_text_trunk():
    tree = Tree.from_text('Alpha')
    assert tree.indent_char is ''
    assert tree.indent_len == 0
    assert tree.outline == {(0,): 'Alpha'}


simplest_2_levels = """
    Alfa
    \tBravo
    """


def test_from_text_trunk_simplest_2_levels():
    tree = Tree.from_text(simplest_2_levels)
    assert tree.indent_char == '\t'
    assert tree.indent_len == 1
    assert tree.outline == {(0,): 'Alfa', (0, 0): 'Bravo'}


def test_from_text_trunk_2_levels_with_4_spaces():
    src = """
        Alfa
            Bravo
            Charlie
        """

    tree = Tree.from_text(src)
    assert tree.indent_char == ' '
    assert tree.indent_len == 4
    assert tree.outline == {
        (0,): 'Alfa',
        (0, 0): 'Bravo',
        (0, 1): 'Charlie',
    }


def test_from_text_trunk_3_levels_with_4_spaces():
    src = """
        Alfa
            Bravo
                Charlie
                Delta
                Echo
        """

    tree = Tree.from_text(src)
    assert tree.indent_char == ' '
    assert tree.indent_len == 4
    assert tree.outline == {
        (0,): 'Alfa',
        (0, 0): 'Bravo',
        (0, 0, 0): 'Charlie',
        (0, 0, 1): 'Delta',
        (0, 0, 2): 'Echo',
    }


four_levels_with_dedent = """
        Alfa
            Bravo
                Charlie
                Delta
            Echo
                Foxtrot
                    Golf
            Hotel
"""

def test_from_text_trunk_4_levels_with_dedent():
    tree = Tree.from_text(four_levels_with_dedent)
    assert tree.indent_char == ' '
    assert tree.indent_len == 4
    assert tree.outline == {
        (0,): 'Alfa',
        (0, 0): 'Bravo',
        (0, 0, 0): 'Charlie',
        (0, 0, 1): 'Delta',
        (0, 1): 'Echo',
        (0, 1, 0): 'Foxtrot',
        (0, 1, 0, 0): 'Golf',
        (0, 2): 'Hotel',
    }


def test_draw_simplest_2_levels():
    tree = Tree.from_text("""
    Alfa
     Bravo
    """)
    want = [
        'Alfa',
        '└Bravo',
    ]
    got = tree.draw()
    assert got == want


def test_draw_2_levels():
    tree = Tree.from_text("""
    Alfa
      Bravo
      Charlie
    """)
    want = [
        'Alfa',
        '├─Bravo',
        '└─Charlie',
    ]
    got = tree.draw()
    assert got == want


def test_draw_3_levels():
    tree = Tree.from_text("""
    Alfa
        Bravo
            Charlie
    """)
    want = [
        'Alfa',
        '└───Bravo',
        '    └───Charlie',
    ]
    got = tree.draw()
    assert got == want

def test_draw_3_levels_2_branches():
    tree = Tree.from_text("""
    Alfa
        Bravo
        Charlie
            Delta
            Echo
    """)
    want = [
        'Alfa',
        '├───Bravo',
        '└───Charlie',
        '    ├───Delta',
        '    └───Echo',
    ]
    got = tree.draw()
    assert got == want

def test_draw_3_levels_dedent():
    tree = Tree.from_text("""
    Alfa
        Bravo
        Charlie
            Delta
        Echo
    """)
    want = [
        'Alfa',
        '├───Bravo',
        '├───Charlie',
        '│   └───Delta',
        '└───Echo',
    ]
    got = tree.draw()
    assert got == want

def test_draw_4_levels_dedent_2():
    tree = Tree.from_text("""
    Alfa
        Bravo
        Charlie
            Delta
                Echo
        Foxtrot
    """)
    want = [
        'Alfa',
        '├───Bravo',
        '├───Charlie',
        '│   └───Delta',
        '│       └───Echo',
        '└───Foxtrot',
    ]
    got = tree.draw()
    assert got == want


##################################### error checking

def test_from_text_mixed_indent_chars_forbidden():
    src = """
        Alfa
            Bravo
        \tCharlie
        """
    with pytest.raises(ValueError) as excinfo:
        tree = Tree.from_text(src)
    assert r"unexpected indent char '\t' at 'Charlie'" == str(excinfo.value)


def test_from_text_inconsistent_indent_len():
    src = """
        Alfa
            Bravo
              Charlie
        """
    with pytest.raises(ValueError) as excinfo:
        tree = Tree.from_text(src)
    assert "inconsistent indentation at 'Charlie'" == str(excinfo.value)


def test_from_text_excessive_indentation():
    src = """
        Alfa
            Bravo
                    Charlie
        """
    with pytest.raises(ValueError) as excinfo:
        tree = Tree.from_text(src)
    assert "excessive indentation at 'Charlie'" == str(excinfo.value)
