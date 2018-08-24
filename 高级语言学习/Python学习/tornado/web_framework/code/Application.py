class Application(ReversibleRouter):
    """A collection of request handlers that make up a web application.

    Instances of this class are callable and can be passed directly to
    HTTPServer to serve the application::

        application = web.Application([
            (r"/", MainPageHandler),
        ])
        http_server = httpserver.HTTPServer(application)
        http_server.listen(8080)
        ioloop.IOLoop.current().start()

    The constructor for this class takes in a list of `~.routing.Rule`
    objects or tuples of values corresponding to the arguments of
    `~.routing.Rule` constructor: ``(matcher, target, [target_kwargs], [name])``,
    the values in square brackets being optional. The default matcher is
    `~.routing.PathMatches`, so ``(regexp, target)`` tuples can also be used
    instead of ``(PathMatches(regexp), target)``.

    A common routing target is a `RequestHandler` subclass, but you can also
    use lists of rules as a target, which create a nested routing configuration::

        application = web.Application([
            (HostMatches("example.com"), [
                (r"/", MainPageHandler),
                (r"/feed", FeedHandler),
            ]),
        ])

    In addition to this you can use nested `~.routing.Router` instances,
    `~.httputil.HTTPMessageDelegate` subclasses and callables as routing targets
    (see `~.routing` module docs for more information).

    When we receive requests, we iterate over the list in order and
    instantiate an instance of the first request class whose regexp
    matches the request path. The request class can be specified as
    either a class object or a (fully-qualified) name.

    A dictionary may be passed as the third element (``target_kwargs``)
    of the tuple, which will be used as keyword arguments to the handler's
    constructor and `~RequestHandler.initialize` method. This pattern
    is used for the `StaticFileHandler` in this example (note that a
    `StaticFileHandler` can be installed automatically with the
    static_path setting described below)::

        application = web.Application([
            (r"/static/(.*)", web.StaticFileHandler, {"path": "/var/www"}),
        ])

    We support virtual hosts with the `add_handlers` method, which takes in
    a host regular expression as the first argument::

        application.add_handlers(r"www\.myhost\.com", [
            (r"/article/([0-9]+)", ArticleHandler),
        ])

    If there's no match for the current request's host, then ``default_host``
    parameter value is matched against host regular expressions.


    .. warning::

       Applications that do not use TLS may be vulnerable to :ref:`DNS
       rebinding <dnsrebinding>` attacks. This attack is especially
       relevant to applications that only listen on ``127.0.0.1` or
       other private networks. Appropriate host patterns must be used
       (instead of the default of ``r'.*'``) to prevent this risk. The
       ``default_host`` argument must not be used in applications that
       may be vulnerable to DNS rebinding.

    You can serve static files by sending the ``static_path`` setting
    as a keyword argument. We will serve those files from the
    ``/static/`` URI (this is configurable with the
    ``static_url_prefix`` setting), and we will serve ``/favicon.ico``
    and ``/robots.txt`` from the same directory.  A custom subclass of
    `StaticFileHandler` can be specified with the
    ``static_handler_class`` setting.

    .. versionchanged:: 4.5
       Integration with the new `tornado.routing` module.

    """
    def __init__(self, handlers=None, default_host=None, transforms=None,
                 **settings):
        if transforms is None:
            self.transforms = []
            if settings.get("compress_response") or settings.get("gzip"):
                self.transforms.append(GZipContentEncoding)
        else:
            self.transforms = transforms
        self.default_host = default_host
        self.settings = settings
        self.ui_modules = {'linkify': _linkify,
                           'xsrf_form_html': _xsrf_form_html,
                           'Template': TemplateModule,
                           }
        self.ui_methods = {}
        self._load_ui_modules(settings.get("ui_modules", {}))
        self._load_ui_methods(settings.get("ui_methods", {}))
        if self.settings.get("static_path"):
            path = self.settings["static_path"]
            handlers = list(handlers or [])
            static_url_prefix = settings.get("static_url_prefix",
                                             "/static/")
            static_handler_class = settings.get("static_handler_class",
                                                StaticFileHandler)
            static_handler_args = settings.get("static_handler_args", {})
            static_handler_args['path'] = path
            for pattern in [re.escape(static_url_prefix) + r"(.*)",
                            r"/(favicon\.ico)", r"/(robots\.txt)"]:
                handlers.insert(0, (pattern, static_handler_class,
                                    static_handler_args))

        if self.settings.get('debug'):
            self.settings.setdefault('autoreload', True)
            self.settings.setdefault('compiled_template_cache', False)
            self.settings.setdefault('static_hash_cache', False)
            self.settings.setdefault('serve_traceback', True)

        self.wildcard_router = _ApplicationRouter(self, handlers)
        self.default_router = _ApplicationRouter(self, [
            Rule(AnyMatches(), self.wildcard_router)
        ])

        # Automatically reload modified modules
        if self.settings.get('autoreload'):
            from tornado import autoreload
            autoreload.start()

    def listen(self, port, address="", **kwargs):
        """Starts an HTTP server for this application on the given port.

        This is a convenience alias for creating an `.HTTPServer`
        object and calling its listen method.  Keyword arguments not
        supported by `HTTPServer.listen <.TCPServer.listen>` are passed to the
        `.HTTPServer` constructor.  For advanced uses
        (e.g. multi-process mode), do not use this method; create an
        `.HTTPServer` and call its
        `.TCPServer.bind`/`.TCPServer.start` methods directly.

        Note that after calling this method you still need to call
        ``IOLoop.current().start()`` to start the server.

        Returns the `.HTTPServer` object.

        .. versionchanged:: 4.3
           Now returns the `.HTTPServer` object.
        """
        # import is here rather than top level because HTTPServer
        # is not importable on appengine
        from tornado.httpserver import HTTPServer
        server = HTTPServer(self, **kwargs)
        server.listen(port, address)
        return server

    def add_handlers(self, host_pattern, host_handlers):
        """Appends the given handlers to our handler list.

        Host patterns are processed sequentially in the order they were
        added. All matching patterns will be considered.
        """
        host_matcher = HostMatches(host_pattern)
        rule = Rule(host_matcher, _ApplicationRouter(self, host_handlers))

        self.default_router.rules.insert(-1, rule)

        if self.default_host is not None:
            self.wildcard_router.add_rules([(
                DefaultHostMatches(self, host_matcher.host_pattern),
                host_handlers
            )])

    def add_transform(self, transform_class):
        self.transforms.append(transform_class)

    def _load_ui_methods(self, methods):
        if isinstance(methods, types.ModuleType):
            self._load_ui_methods(dict((n, getattr(methods, n))
                                       for n in dir(methods)))
        elif isinstance(methods, list):
            for m in methods:
                self._load_ui_methods(m)
        else:
            for name, fn in methods.items():
                if not name.startswith("_") and hasattr(fn, "__call__") \
                        and name[0].lower() == name[0]:
                    self.ui_methods[name] = fn

    def _load_ui_modules(self, modules):
        if isinstance(modules, types.ModuleType):
            self._load_ui_modules(dict((n, getattr(modules, n))
                                       for n in dir(modules)))
        elif isinstance(modules, list):
            for m in modules:
                self._load_ui_modules(m)
        else:
            assert isinstance(modules, dict)
            for name, cls in modules.items():
                try:
                    if issubclass(cls, UIModule):
                        self.ui_modules[name] = cls
                except TypeError:
                    pass

    def __call__(self, request):
        # Legacy HTTPServer interface
        dispatcher = self.find_handler(request)
        return dispatcher.execute()

    def find_handler(self, request, **kwargs):
        route = self.default_router.find_handler(request)
        if route is not None:
            return route

        if self.settings.get('default_handler_class'):
            return self.get_handler_delegate(
                request,
                self.settings['default_handler_class'],
                self.settings.get('default_handler_args', {}))

        return self.get_handler_delegate(
            request, ErrorHandler, {'status_code': 404})

    def get_handler_delegate(self, request, target_class, target_kwargs=None,
                             path_args=None, path_kwargs=None):
        """Returns `~.httputil.HTTPMessageDelegate` that can serve a request
        for application and `RequestHandler` subclass.

        :arg httputil.HTTPServerRequest request: current HTTP request.
        :arg RequestHandler target_class: a `RequestHandler` class.
        :arg dict target_kwargs: keyword arguments for ``target_class`` constructor.
        :arg list path_args: positional arguments for ``target_class`` HTTP method that
            will be executed while handling a request (``get``, ``post`` or any other).
        :arg dict path_kwargs: keyword arguments for ``target_class`` HTTP method.
        """
        return _HandlerDelegate(
            self, request, target_class, target_kwargs, path_args, path_kwargs)

    def reverse_url(self, name, *args):
        """Returns a URL path for handler named ``name``

        The handler must be added to the application as a named `URLSpec`.

        Args will be substituted for capturing groups in the `URLSpec` regex.
        They will be converted to strings if necessary, encoded as utf8,
        and url-escaped.
        """
        reversed_url = self.default_router.reverse_url(name, *args)
        if reversed_url is not None:
            return reversed_url

        raise KeyError("%s not found in named urls" % name)

    def log_request(self, handler):
        """Writes a completed HTTP request to the logs.

        By default writes to the python root logger.  To change
        this behavior either subclass Application and override this method,
        or pass a function in the application settings dictionary as
        ``log_function``.
        """
        if "log_function" in self.settings:
            self.settings["log_function"](handler)
            return
        if handler.get_status() < 400:
            log_method = access_log.info
        elif handler.get_status() < 500:
            log_method = access_log.warning
        else:
            log_method = access_log.error
        request_time = 1000.0 * handler.request.request_time()
        log_method("%d %s %.2fms", handler.get_status(),
                   handler._request_summary(), request_time)
