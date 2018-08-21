# Templates and UI
Tornado can be used with any other Python template language, although there is no provision for integrating these systems into RequestHandler.render. Simply render the template to a string and pass it to RequestHandler.write.

## Configuring templates
Tornado looks for template files in the same dir as the .py files that refer to them. To put your template files in a different dir, use `template_path Application setting`(or override `RequestHandler.get_templdate_path`).
<p></p>

To load templates from a non-filesystem location, subclass `tornado.template.BaseLoader` and pass an instance as the `template_loader`application setting.
<p></p>

Compiled templates are cached by default; to turn off this caching and reload templates so changes to the underlying files are always visible, use the application settings `compiled_template_cache=False` or `debug=True`
## Template syntax
A Tornado template is just HTML with Python control sequences and expressions embedded within the markup:
```html
<html>
   <head>
      <title>{{ title }}</title>
   </head>
   <body>
     <ul>
       {% for item in items %}
         <li>{{ escape(item) }}</li>
       {% end %}
     </ul>
   </body>
 </html>
```
If you saved this template as "template.html" and put it in the same dir as your Python file, you can render this template by this:
```py
class MainHandler(RequestHandler):
    def get(self):
        items = ["Item1", "Item2", "Item3"]
        self.render("template.html", title="Mytitle", items=items)
```

Tornado templates support control statements and expressions. Control statements are surrounded by `{%` and `%}` and Expressions are surrounded by `{{` and `}}`.
<p></p>

Control statements more or less map exactly to Python statements. We support if, for, while and try, all of which are terminated with `{% end %}`.
<p></p>

Expressions can be any Python expression, including function calls. Template code is executed in a namespace that includes the following objects and functions:
<p></p>

Alias | Deatil
:-: | :-:
`escape` | `tornado.escape.xhtml_escape`
`xhtml_escape` | `tornado.escape.xhtml_escape`
`url_escape` | `tornado.escape.url_escape`
`json_encode` | `tornado.escape.json_encode`
`squeeze` | `tornado.escape.squeeze`
`linkify` | `tornado.escape.linkify`
`datetime`| `datetime`
`handler` | current `RequestHandler`
`request` | `handler.request`
`current_user` | `handler.current_user`
`locale` | `handler.locale`
`_` | `handler.locale.translate`
`static_url` | `handler.static_url`
`xsrf_form_html` | `handler.xsrf_form_html`
`reverse_url` | `Application.reverse_url`

## Internationalization
You can use `_` in your template to translate for current user.
```
_("translate this string.")
``` 


## UI modules
pass
