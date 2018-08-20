# Structure of a tornado web application

A tornado web application generally consists of once or more RequestHandler subclasses, an Application object which routes incoming requests to handlers, and a main() function to start the server.
<p></p>

Here is a sample of Tornado web application

```py
import tornado.ioloop
import tornado.web

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write('Hello world')

def make_app():
    return tornado.web.Application([
        (r"/", MainHandler)
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8080)
    tornado.ioloop.IOLoop.current().start()

```

## The Application object
The Application object is responsible for global configuration, including the routing table that maps requests to handlers.
<p></p>

The routing table is a list of URLSepc objects(or tuples), each of which contains a regular expression and a handler class. Order matters; the first matching rule is used. If the regular expressing contains capturing groups, these groups are the path arguments and will be passed to the handler's HTTP method. If a dictionary is passed as the third element of the URLSpec, it supplies the initialization arguments which will be passed to RequestHandler.initialize, Finally, the URLSpec may have a name, which allow it to be used with RequestHandler.reverse\_url.
<p></p>

For example, in this fragment the root URL / is mapped to MainHandler, and URLs of the form /story/ followed by a number are mapped to StoryHandler. That number is passed(as a string) to StoryHandler.get

```py
class MainHandler(RequestHandler):
    def get(self):
        self.write('<a href="%s">link to story 1</a>'%(self.reverse_url("story", "1")))

class StoryHandler(RequestHandler):
    def initialize(self, db):
        self.db = db

    def get(self, story_id):
        self.write("This is story %s"%story_id)

app = Application([
    url(r'/', MainHandler),
    url(r'/story/([0-9]+)', StoryHandler, dict(db=db), name="story")
])

```
The Application constructor takes many keyword arguments that can be used to customize the behavior of the application and enable optional features.

## Subclasses RequestHandler
Most of the work of a Tornado web app is done in the subclasses RequestHandler. The main entry point for a handler subclass is a method named after the HTTP method being handled: get(), post(), etc. Each handler may define one or more these methods to handle different HTTP actions. As described above, these methods will be called with arguments corresponding to the capturing groups of the routing rule that matched.
<p></p>

Within a handler, call methods such as RequestHandler.render or RequestHandler.wirte to produce a response. render() loads a Template by name and renders it with the given arguments. write() is used for non-template-based output; it accepts strings, bytes and dict(dict will be encoded as JSON).
<p></p>

Many methods in RequestHandler **are designed to be overridden in subclasses** and be used throughout the application. It is common to define a BaseHandler class that the overrides methods such as write\_error and get\_current\_user and the subclass your own BaseHandler instead of RequestHandler for all your specific handlers.

## Handling request input
The request handler can access the object representing the current request with self.request.
<p></p>

Request data in the formats used by HTML forms will be parsed for you and is made available in methods like `get_query_argument` and `get_body_argument`
```py
class MyFormHandler(RequestHandler):
    def post(self):
        self.set_header("Content-Type", "text/plain")
        self.write("You write {}".format(self.get_body_argument("message")))
```
Since the HTML form encoding is ambiguous as to whether an argument is single value or a list with one element, RequestHandler has distinct methods to allow the application to indicate whether or not it expects a list. For lists, use `get_query_arguments` and `get_body_arguments` instead of their singular counterparts.
<p></p>

File uploaded via a form are availbale in self.request.files, which maps names(the name of the HTML `<input type="file">` element) to a list of files. Each file is a dictionary of the form `{"filename":..., "content_type":..., "body":...}`. The files object is only present if the files were uploaded with a form wrapper; if this format was not used the raw uploaded data is available in self.request.body.
<p></p>

By default uploaded files are fully buffered in the memory; if you need to handle files that are too large to comfortably keep in memory, see the `stream_request_body` class decorator.

## Overriding RequestHandler methods
In addition rto `get()`/`post()`, certain other methods in RequestHandler are designed to be overridden by subclasses when neccessary. On every request, the following sequence of calls takes place:
- 1. A new RequestHandler object is created on each request.
- 2. initialize() is called with the initialize arguments from the Application configuration. initialize should typically just save the arguments passed into member variables; it may not produce any output or call methods like `send_error`
- 3. perpare() is called. This is most useful in a base class shared by all of your handler subclasses, as prepare is call no matter which HTTP method is used. prepare may produce output; if it calls finish(or redirect, etc), processing stop here.
- 4. One of the HTTP methods is called: get(), post(), put(), etc. If the URL regular expression contains capturing groups, they are passed as arguments to this methods.
- 5. When the request is finished, `on_finish()` is called. For most handlers this is immediately after get() return; for handlers using the tornado.web.asynchronous decorator it is after the call to finish().
<p></p>

All methods designed to be overridden are noted as such in the RequestHandler documentation. Some of the most commonly overridden methods include:
- `write_error` => outputs HTML for use on error pages
- `on_connection_close` => called when the client disconnects; application may choose to detect this case and halt futher processing. Note that there is no guarantee that a closed connection can be detected promptly.
- `get_current_user`
- `get_user_locale` => returns Locale object to use for the current user.
- `set_default_headers` => may be used to set additional headers on the response(such as a custom Server Handler)

## Error Handling
If a handler raises an Exception, Tornado will call `RequestHandler.write_error` to generate an error page. **tornado.web.HTTPError can be used to generate a specified status code**; all other exceptions return a 500 status.
<p></p>

The default error page includes a stack trace in debug mode and one-line description of the error.(e.g. "500:Internal Server Error") otherwise. To produce a custom error page, override `RequestHandler.write_error`. This method may produce output normally via methods such as write and render. If the error was caused by an exception, an `exc_info` triple will be passed as a keyword argument( note that this exception is not guaranteed to be the current exception in sys.exc\_info, so write\_error must use e.g. traceback.format\_exception instead of traceback.format\_exc).
<p></p>

It is also possible to generate an error page from regular handler methods instead of write\_error by calling set\_status, writing a response, and returning. The special exception tornado.web.Finish may be raised to terminate the handler without calling write\_error in situations where simply returning is not convenient.

## Redirection
Here are two methods to redirect requests in Tornado: RequestHandler.redirect and RedirectHandler. You can just use self.redirect() in the subclasses in RequestHandler, while RedirectHandler letting you configure redirects in your Application routing table.
```py
app = Application([
    url(r'/app', RedirectHandler, dict(url="http://www.app.com")),
    url(r'/pic/(.*)', PictureHandler),
    url(r'/photo/(.*)', RedirectHandler, dict(url=r'/pic/{0}'))
])

```

## Asynchronous handlers
You can override the methods in RequestHandler to make the handler asynchronous. For example, here is a simple handler using a coroutines:
```py
class MainHandler(RequestHandler):
    async def get(self):
        http = tornado.httpclient.AsyncHTTPClient()
        resp = await http.fetch("http://www.qq.com/json")
        json = tornado.escape.json_decode(resp.body)
        self.write(json)
```
