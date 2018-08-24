# Authentication and Security

## Cookies and secure cookies
You can set cookies in the user's browser with the `set_cookie` methods.
```py
class MainHandler(tornado.web.RequestHandler):
    def get(self):
        if not self.get_cookie("mycookie"):
            self.set_cookie("mycookie", "myvalue")
            self.write("Set your cookie success.")
        else:
            self.write("Your cookie is set.")
```

Cookies are not secure and can easily be modified by clients. If you need to set cookies to e.g., identify the currently logged in user, you need to sign your cookies to prevent forgery. Tornado supports signed cookies with the `set_secure_cookie` and `get_secure_cookie` methods. To use these methods, you need to specify a secure key named `cookie_secure` when you create your application. You can pass in application settings as keyword arguments to you application:
```py
application = tornado.web.Application([
    (r"/", MainHandler),
], cookie_secure="ASDASDASDASDDSDADA")

```

Signed cookies contain the encoded value of the cookie in addition to a timestamp and an HMAC signature. If the cookie is old or if the signature doesn't match, `get_secure_cookie` will return None just as if the cookie isn't set. The secure version of the example above:
```py
class MainHandler(tornado.web.RequestHandler):
    def get(self):
        if not self.get_secure_cookie("mycookie"):
            self.set_secure_cookie("mycookie", "myvalue")
            self.wirte("Your cookie was not set yet.")
        else:
            self.write("Your cookie was set.")
```

Tornado's secure cookie guarantee integrity but not confidentiality. That is, the cookie cannot be modified but its contents can be seen by the user. The `cookie_secret` is a symmetric key and must be kept secure.
<p></p>

By default, Tornado's secure cookies expire after 30 days. To change this, use the `expires_days` keyword argument to `set_secure_cookie` and the `max_age_days` argument to `get_secure_cookie`. For certain sensitive actions(such as changing billing information) you use a smaller `max_age_days` when you reading the cookie.

## User Authentication
The currently authed-user is available in every request handler as `self.current_user`, and in every template as `current_user`. By default, the value is None.
<p></p>

To implement user authentication in your application, you need to override the `get_current_user()` method in your request handler to determine the current user based on, e.g., the value of a cookie. Here is an example that lets users log into the application simply by specifying a nickname, which is then saved in a cookie:
```py
class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("user")

class MainHandler(BaseHandler):
    def get(self):
        if not self.current_user:
            self.redirect("/login")
            return
        name = tornado.escape.xhtml_escape(self.current_user)
        self.write("Hello, %s" % name)

class LoginHandler(BaseHandler):
    def get(self):
        self.write('<html><body><form action="/login" method="post">'
                   'Name: <input type="text" name="name">'
                   '<input type="submit" value="Sign in">'
                   '</form></body></html>')
    
    def post(self):
        self.set_secure_cookie("user", self.get_argument("name"))
        self.redorect("/")

application = tornado.web.Application([
    (r'/', MainHandler),
    (r'/login', LoginHandler),
], cookie_secret="ASDASDAdasdasadawd")

```

You can require that the user be logged in **using the Python decorator `tornado.web.authenticated`**. If the result goes to a method with this decorator, and the user is not logged in, they will be redirected to login\_url.
```py
class MainHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        name = tornado.escape.xhtml_escape(self.current_user)
        self.write("Hello %s" % name)

settings = {
    "cookie_secret":"ASDASDASDASDASDAS",
    "login_url":"/login"
}

application = tornado.web.Application([
    (r'/', MainHandler),
    (r'/login', LoginHandler),
], **settings)
```

If you decorate post() methods with the authenticated decorator and the user is not logged in, the server will send a 403 response.

## Third-party authentication
The tornado.auth module implements the authentication and authorization protocols for a number of most popular sites on the web, which is named `OAuth2 Login`. Here is the sample:
```py
class GoogleOAuth2LoginHandler(tornado.web.RequestHandler, tornado.auth.GoogleOAuth2Mixin):
    async def get(self):
        if self.get_argument("code", False):
            user = await self.get_authenticated_user(
                redirect_url = "http://yourweb.com",
                code = self.get_argument("code")
            )
        else:
            await self.authorize_redirect(
                redirect_url = "http://youweb.com",
                client_id = self.settings["google_oauth"]["key"],
                scope = ["profile", "email"],
                response_type = 'code',
                extra_params = {"k":"v"}
            )
```

## Cross-site request forgery(CSRF/XSRF) protection
CSRF(or XSRF) is a common problem for personalized web applications. The generally accepted solution to prevent CSRF is to cookie every user with an unpredictable value and include that value in the form submission don't match, then the request is likely forged.
<p></p>

Tornado comes with build-in XSRF protection. To include it in your site, include the application setting `xsrf_cookies`.

```py
settings = {
    "cookie_secret":"ADADADASDASDASDA",
    "login_url":"./login",
    "xsrf_cookie":True
}

application = tornado.web.Application([
    (r'/', MainHandler),
    (r'/login', LoginHandler)
], **settings)
```

If `xsrf_cookie` is set, the Tornado web application will set the `_xsrf` cookie for all users and reject all POST, PUT and DELETE requests that don't contain a correct `_xsrf` value. If you turn this setting on, you need to instrument all forms that submit via POST to contain this field. You can do this with the special `UIModule xsrf_form_html()`, available in all templates:
```html
<form action="/new_message" method="post">
    {% module sxrf_form_html() %}
    <input type="text" name="message"/>
    <input type="submit" value="post"/>
</form>
```

If you submit with AJAX, you will also need to instrument your Javascript to include the `_xsrf` value with each request. This is the jQuery function we use at FriendFeed for AJAX POST requests that automantically adds the `_xsrf` value to all requests:
```js
function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

jQuery.postJSON = function(url, args, callback) {
    args._xrsf = getCookie("_xsrf");
    $.ajax({url:url, data: $.params(args), dataType:"text", type:"POST",
        success: function(response){
        callback(eval("("+ response + ")"));
    }});
};
```

For PUT and DELETE requests(as well as POST requests that don't use form-encode arguments), the XSRF token may also be passed via an HTTP header named `X-XSRFToken`. The XSRF cookie is normally set when `xsrf_form_html` is used, but in a pure-Javascript application that dosen't use any regular forms you may need to access `self.xsrf_token` manually (just reading the property is enough to set the cookie as a side effect).


## DNS Rebinding
**_PASSED_**