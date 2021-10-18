# `drawtree`: draw tree diagrams from indented text input

Given a text file with an outline indented with spaces or tabs (but not both),
_drawtree.py_ displays a tree diagram made with the Unicode box drawing characters.

For example, this command:

```
$ drawtree.py examples/httpx_exceptions.txt
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
