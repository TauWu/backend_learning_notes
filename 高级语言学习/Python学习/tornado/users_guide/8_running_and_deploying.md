# Running and Deploying
Instead of configuring a WSGI container to find your application, you just write a main() function that starts the server.

```py
def main():
    app = make_app()
    app.listen(8080)
    IOLoop.current().start()

if __name__ == "__main__":
    main()
```

## Processes and ports
Due to the Python GIL(Global Interpreter lock), it is necessary to run multiple Python processes to take full adavantage of multi-CPU machines.
<p></p>

Tornado includes a built-in multi-process mode to start several processes at once. This requires a slight alteration to the standard main function:

```py
def main():
    app = make_app()
    server = tornado.httpserver.HTTPServer(app)
    server.bind(8080)
    server.start(0) # fork on process per CPU
    IOLoop.current().start()
```

This is the easiest way to start multiple processes and have them all share the same port, although it has some limitations. First, each child process will have its Own IOLoop, so it is important that nothong touch the global IOLoop instance before the fork. Second, it is difficult to do zero-downtime updates in this module. Finally, since all the processes share the same port it is more difficult to monitor them indivdually.

## Running behind a load balancer
When running behind a load balancer like nginx, it is recommended to pass `xheaders=True` to the `HTTPServer` constructor. This will tell Tornado to use headers like `X-Real-IP` to get user's IP address instead of attributing all traffic to the balancer's IP address.

## Static files and aggressive file caching
You can serve static files from Tornado by specifying the `static_path` setting in your application:

```py
settings= {
    "static_path":os.path.join(os.path.dirname(__file__), "static"),
    "cookie_secret":"ASSSDASDASDADQWDASDW",
    "login_url":"/login",
    "xsrf_cookies":True,
}
application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/login", LoginHandler),
    (r"/(apple-touch-icon\.jpg)", tornado.web.StaticFileHandler, dict(path=settings['static_path'])),
])
```

This settings will automatically make all requests that start with `/start/` serve from that static dir, e.g. `http://localhost:8080/static/foo.png` will serve the file `foo.png` from the specified static dir.
<p></p>

Or you can use `static_url` method in your templates.

```html
<html>
   <head>
      <title>FriendFeed - {{ _("Home") }}</title>
   </head>
   <body>
     <div><img src="{{ static_url("images/logo.png") }}"/></div>
   </body>
 </html>

```

## Debug and automatic reloading
If you pass `debug=True` to the Application constructor, the app will be run in debug/development mode. In this mode, several features intended for convneience while developing will be enabled(each of which is also available as an indicidual flag; if both are specified the individual flag takes precedence):

- `autoreload=True` => The app will watch for changes to its source files and reload itself when anything changes. This reduces the need to manually restart the server during development. However, **certain failures (e.g. Syntax Error)can still take the server down** in a way that debug mode cannot currently recover from.

- `compiled_template_cache=False` => Templates will not be cached.

- `static_hash_cached=False` => Static file hashes(used by the `static_url` function) will not be cached.

- `serve_traceback=True` => When an exception in a RequestHandler is not caught, an error page including a stack trace will be generated.
<p></p>


Autoreload mode is not compatible with the multi-process mode of the HTTPServer. You must not give HTTPServer.start an argument other than 1(or call `tornado.process.fork_process`) if you are using autoreload mode.
<p></p>

The automatic reloading feature of debug mode is available as a standalone module in `tornado.autoreload`. The two can be used in combination to procide extra robustness against syntax error: set `autoreloaded=True` within the app to detect changes while it is running, and start it with `python -m tornado.autoreload myserver.py` to catch any syntax errors or other errors at startup.

## WSGI
Tornado is normally intented to be run on its own, without a WSGI container. However, in some environments, only WSGI is allowed and applications cannot run their own servers. In this case, Tornado supports a limited mode of operation that doesn't support asynchronous operation but allows a subset of Tornado's functionality in a WSGI-only env. The features that are not allowed in WSGI mode include coroutines, the `@asynchronous` decorator, `AsyncHTTPClient`, the `auth` module and Web Sockets.
<p></p>

You can convert a Tornado Application to a WSGI application with `tornado.wsgi.WSGIAdapter`. In this sample, configure your WSGI container to find the application object.
```py
import tornado.web
import tornado.wsgi

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello world")

tornado_app = tornado.web.Application([
    (r'/', MainHandler)
])
application = tornado.wsgi.WSGIAdapter(tornado_app)

```