import httpx

def tree(cls, level=0):
    yield cls, level
    for sub_cls in cls.__subclasses__():
        if sub_cls.__module__ == 'httpx' or sub_cls is RuntimeError:
            yield from tree(sub_cls, level+1)


def display(root):
    for cls, level in tree(root):
        indent = ' ' * 4 * level
        prefix = 'builtins.' if cls.__module__ == 'builtins' else ''
        print(f'{indent}{prefix}{cls.__name__}')


def find_roots(module):
    exceptions = []
    for name in dir(module):
        obj = getattr(module, name)
        if isinstance(obj, type) and issubclass(obj, BaseException):
            exceptions.append(obj)
    roots = []
    for exc in exceptions:
        root = True
        for other in exceptions:
            if exc is not other and issubclass(exc, other):
                root = False
                break
        if root:
            roots.append(exc)
    return roots


def main():
    display(Exception)

if __name__ == '__main__':
    main()
