# Draw tree diagrams

This repository contains two *very different* scripts
to produce hierarchical tree diagrams like this one:

```
$ ./classtree.py collections.abc.Container
Container
└── Collection
    ├── Set
    │   ├── MutableSet
    │   ├── KeysView
    │   │   └── _OrderedDictKeysView
    │   └── ItemsView
    │       └── _OrderedDictItemsView
    ├── Mapping
    │   └── MutableMapping
    │       ├── _Environ
    │       ├── ChainMap
    │       └── UserDict
    ├── ValuesView
    │   └── _OrderedDictValuesView
    └── Sequence
        ├── ByteString
        ├── MutableSequence
        │   └── UserList
        └── UserString
```

Please see the `README.md` files in each directory:

- [`classtree/classtree.py`](classtree/) draws trees for Python classes;
- [`drawtree/drawtree.py`](drawtree/) draws trees from indented text files.

I wrote the scripts at different times.
They illustrate different approaches to the same basic problem.
`classtree.py` is much simpler.
