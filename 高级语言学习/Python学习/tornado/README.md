# TORNADO

## Description
This is a folder about tornado framework DOC, you can [click here](http://www.tornadoweb.org/en/stable/index.html) to goto the raw website.
> Current version: 5.1
> source: [github](https://github.com/tornadoweb/tornado)

## MENU

- [ ] User's guide
    - [ ] Introduction
    - [ ] Asynchhronous and non-Blocking I/O
    - [ ] Queue example - a concurrent web spider
    - [ ] Structure of a Tornado web application
    - [ ] Templates and UI
    - [ ] Authentication and security
    - [ ] Runing and deploying

- [ ] Web framework
    - [ ] tornado.web - RequestHandler and Application classes
    - [ ] tornado.template - Flexible output generation
    - [ ] tornado.routing - Basic routing implementation
    - [ ] tornado.escape - Escaping and string manipulation
    - [ ] tornado.locale - Internationalization support
    - [ ] tornado.websocket - Bidirectional communication to the browser

- [ ] HTTP servers and clients
    - [ ] tornado.httpserver - Non-blocking HTTP server
    - [ ] tornado.httpclient - Asynchronous HTTP client
    - [ ] tornado.httputil - Manipulate HTTP headers and URLs
    - [ ] http.http1connection - HTTP/1.x client/server implementation

- [ ] Asynchronous networking
    - [ ] tornado.ioloop - Main event loop
    - [ ] tornado.iostream - Conveninet wrappers for non-blocking sockets
    - [ ] tornado.netutil - Miscellaneous network utilities
    - [ ] tornado.tcpclient - IOStream connection factory
    - [ ] tornado.tcpserver - Basic IOStream-based TCP server

- [ ] Coroutines and concurrency
    - [ ] tornado.gen - Generator-based coroutines
    - [ ] tornado.locks - Synchronization primitives
    - [ ] tornado.queues - Queues for corountines
    - [ ] tornado.process - Utilities for multiple processes

- [ ] Integration with other services
    - [ ] tornado.auth - Third-party login with OpenID and OAuth
    - [ ] tornado.wsgi - Interoperability with other python frameworks and servers
    - [ ] tornado.platform.caresresolver - Asynchronous DNS Resolver with C-Ares
    - [ ] tornado.platform.twisted - Brideges between Twisted and Tornado
    - [ ] tornado.platform.asyncio - Bridege between asyncio and Tornado

- [ ] Utilities
    - [ ] tornado.autoreload - Automatically detect code changes in development
    - [ ] tornado.concurrent - Work with Future objects
    - [ ] tornado.log - Logging support
    - [ ] tornado.options - Command-line parsing
    - [ ] tornado.stack\_context - Exception halding across asynchronous callbacks
    - [ ] tornado.testing - Unit testing support for asynchronous code
    - [ ] tornado.util - General-purpose utilities

- [ ] Frequently asked questions

## Start to tornado

### hello, world
Here is a sample web app for Tornado.

```py
import tornado.ioloop
import tornado.web

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello world!")

def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8089)
    tornado.ioloop.IOLoop.Current().Start()
```
This sample doesn't use any of Tornado's asynchronous features.

### Threads and WSGI
Tornado is different from most Python web frameworks. **It isn't based on WSGI**, and it is typically run with only one thread per process. Thus, Tornado is able to asynchronous program.
<p></p>

However, there is some support of WSGI in `tornado.wsgi` module, it isn't a focus of development and most applications should be written to use Tornado's own interfaces(such as `tornado.web`) directly instead of using WSGI.
<p></p>

In general, **Tornado code is not thread-safe**. The only method in Tornado that is safe to call from other threads is `IOLoop.add_callback`. You can also use `IOLoop.run_in_executor` to asynchronously run a blocking function on another thread, but note that the function passed to run\_in\_executor should avoid referencing any Tornado objects.

### Installation
```sh
pip install tornado
```
You are supposed to execute this command with root/Administrator's privileges.


