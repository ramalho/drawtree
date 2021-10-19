from textwrap import dedent
from classtree import tree, render_lines, main


def test_1_level():
    result = list(render_lines(tree(TabError)))
    expected = [
        'TabError',
    ]
    assert expected == result


def test_2_levels_1_leaf():
    result = list(render_lines(tree(IndentationError)))
    expected = [
        'IndentationError',
        '└── TabError',
    ]
    assert expected == result


def test_3_levels_1_leaf():
    class X: pass
    class Y(X): pass
    class Z(Y): pass
    result = list(render_lines(tree(X)))
    expected = [
        'X',
        '└── Y',
        '    └── Z',
    ]
    assert expected == result


def test_4_levels_1_leaf():
    class Level0: pass
    class Level1(Level0): pass
    class Level2(Level1): pass
    class Level3(Level2): pass

    result = list(render_lines(tree(Level0)))
    expected = [
        'Level0',
        '└── Level1',
        '    └── Level2',
        '        └── Level3',
    ]
    assert expected == result


def test_2_levels_2_leaves():
    class Branch: pass
    class Leaf1(Branch): pass
    class Leaf2(Branch): pass
    result = list(render_lines(tree(Branch)))
    expected = [
        'Branch',
        '├── Leaf1',
        '└── Leaf2',
    ]
    assert expected == result


def test_3_levels_2_leaves_dedent():
    class A: pass
    class B(A): pass
    class C(B): pass
    class D(A): pass
    class E(D): pass

    result = list(render_lines(tree(A)))
    expected = [
        'A',
        '├── B',
        '│   └── C',
        '└── D',
        '    └── E',
    ]
    assert expected == result


def test_4_levels_4_leaves_dedent():
    class A: pass
    class B1(A): pass
    class C1(B1): pass
    class D1(C1): pass
    class D2(C1): pass
    class C2(B1): pass
    class B2(A): pass
    expected = [
        'A',
        '├── B1',
        '│   ├── C1',
        '│   │   ├── D1',
        '│   │   └── D2',
        '│   └── C2',
        '└── B2',
    ]

    result = list(render_lines(tree(A)))
    assert expected == result


def test_main_simple(capsys):
    main('IndentationError')
    expected = dedent("""
        IndentationError
        └── TabError
    """).lstrip()
    captured = capsys.readouterr()
    assert captured.out == expected


def test_main_dotted(capsys):
    main('collections.abc.Sequence')
    expected = dedent("""
        Sequence
        ├── ByteString
        ├── MutableSequence
        │   └── UserList
    """).lstrip()
    captured = capsys.readouterr()
    assert captured.out.startswith(expected)


def test_main_class_not_found(capsys):
    main('NoSuchClass')
    expected = "*** 'NoSuchClass' not found in 'builtins'.\n"
    captured = capsys.readouterr()
    assert captured.out == expected


def test_main_module_not_found(capsys):
    main('nosuch.module')
    expected = "*** Could not import 'nosuch'.\n"
    captured = capsys.readouterr()
    assert captured.out == expected


def test_main_not_a_class(capsys):
    main('collections.abc')
    expected = "*** 'abc' is not a class.\n"
    captured = capsys.readouterr()
    assert captured.out == expected
