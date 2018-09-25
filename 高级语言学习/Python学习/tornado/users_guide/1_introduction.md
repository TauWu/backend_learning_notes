# INTRODUCTION

Tornado is a Python web framework and asynchronous networking library. By using non-blocking network I/O, Tornado can scale to tens of thousands of open connections, making it ideal for long polling, Websockets, and other applications that require a long-lived connection to each-other.

## Major compontents

- Web framwork
including RequestHandler which is subclassed to create web applications.

- Client- and server-side implementions of HTTP
HTTPServer and AsyncHTTPClient

- Asynchronous networking library
including classes IOLoop and IOStream, which serve as the building blocks for the HTTP components and can alsp be used to implement other protocols.

- Corountine library
Class tornado.gen allows asynchronous code to be written in a more straightforword way than chaining callbacks. This is similar to native coroutine feature introduced in Python3.5 (or later, async def).

## Others
The Tornado web framework and HTTP server together offer **a full-stack alternative on WSGI**. While it is possible to use the Tornado HTTP server as a container for other WSGI frameworks, each of these combinations has limitations and take full advantages of Tornado you will need to use the Tornado's web frameworks and HTTP server together.
