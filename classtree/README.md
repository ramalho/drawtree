# Draw tree diagrams from Python classes

Run `drawtree.py` with one argument which may be:

1. The simple name of a built-in class—e.g. `BaseException` is interesting.
2. The qualified name of any class available to import—e.g. `httpx.HTTPError`,
   if you installed [*HTTPX*](https://www.python-httpx.org/).

Example:

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

> **NOTE**: A class name may appear more than once in the tree
> because of multiple inheritance.
