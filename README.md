# Draw tree diagrams from indented text input

Given a text file with an outline indented with spaces,
_drawtree.py_ displays a tree diagram made with Unicode box drawing characters.

> **NOTE**: I wrote a much simpler similar script in 
> the [Fluent Python 2e repository](https://github.com/fluentpython/example-code-2e/tree/master/17-it-generator/tree/extra)

For example, this command:

```
$ ./drawtree.py examples/httpx_exceptions.txt
```

Produces this output:

```
builtins.Exception
├───builtins.RuntimeError
│   └───StreamError
│       ├───StreamConsumed
│       ├───StreamClosed
│       ├───ResponseNotRead
│       └───RequestNotRead
├───HTTPError
│   ├───RequestError
│   │   ├───TransportError
│   │   │   ├───TimeoutException
│   │   │   │   ├───ConnectTimeout
│   │   │   │   ├───ReadTimeout
│   │   │   │   ├───WriteTimeout
│   │   │   │   └───PoolTimeout
│   │   │   ├───NetworkError
│   │   │   │   ├───ReadError
│   │   │   │   ├───WriteError
│   │   │   │   ├───ConnectError
│   │   │   │   └───CloseError
│   │   │   ├───ProxyError
│   │   │   ├───UnsupportedProtocol
│   │   │   └───ProtocolError
│   │   │       ├───LocalProtocolError
│   │   │       └───RemoteProtocolError
│   │   ├───DecodingError
│   │   └───TooManyRedirects
│   └───HTTPStatusError
├───InvalidURL
└───CookieConflict
```

> **NOTE**: The tree will always have a single root (the first line),
therefore the input outline must have a single top-level item.
