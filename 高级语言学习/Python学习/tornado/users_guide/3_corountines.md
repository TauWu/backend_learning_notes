# COROUNTINES

Corountines are the recommended way to write asynchronous code in Tornado. Coroutines use the `yield` or `await` keyword to suspeng and resume execution instead of a chain of callbacks (cooperative light-weight threads as seen in frameworks like gevent are sometimes called coroutines as well, but in Tornado, all coroutines use explicit context switches and are called as asynchronous functions).
<p></p>

Coroutines are without the expense of threads, they also make concurrency easier to reason about by reducing the number of places where a context switch can happen.

```py
async def fetch_coroutine(url):
    client = AsyncHTTPClient()
    resp = await client.fetch(url)
    return resp.body
```

## Native \<-\> decorated `coroutines`
Python 3.5(or later) use `yield` or `await` to build native coroutines. With the old version of Python, you can use decorated or yield-based coroutines. In tornado, `tornado.gen.coroutine` provide it,
<p></p>

You can use coroutine with these two methods:

```py
@gen.coroutine
def fun():
    data = yield fun_wait()
    raise gen.Return(data)
```

```py
async def func():
    data = await func_wait()
    return data
```

The differences between the two forms of coroutines:
- Native coroutines are generally faster.
- Native coroutines can use `async for` and `async with` statements which make some patterns much simlper.
- Native coroutines **don't run at all unless you `await` or `yield` them**. Decorated coroutines can **start running in the background** as soon as they are called. Both kinds of coroutines is important to use `await` or `yield` so that any exceptions have somewhere to go.
- Decorated coroutines has additional integration with the `coroutine.future` package, allowing the result of `executor.submit` to be yielded directly. For native coroutines, use `tornado.gen.convert_yielded`.
- Decorated coroutines always return a Future object. Native coroutines return an awaitable object.

## How it works
Native coroutines are conceptually similar, but a little more complicated because of the extra integration with the Python runtime.
<p></p>

A function containing yield is a generator. **All generator are asynchronous**, when called they return a generator object instead of running to completion. The `@gen.coroutine` decorater communicates with the generator via the yield expressions, and with the coroutine's caller by returning a *Future*.
<p></p>

Here is a sample for decorater version of coroutine:
```py
# Inner code in tornado.gen.Runner
def run(self):
    # send(x) makes the current_yield return x,
    # It returns when the next yield is reached.
    def callback(f):
        self.next = f.result()
        self.run()
    future.add_done_callback(callback)
```

The decorator receives a Future from the generator, waits(without blocking) for that Future to conpelete, then **`unwarps` the Future and sends the result back into the generator** as the result of the yield expression.

## How to call a coroutine
Coroutines don't raise exceptions in the nromal way: any exception they raise will be trapped in the awaitable object util it is yielded. This means it is important to call coroutines in the right way, or you may have errors that go unnoticed:

```py
async def divide(x, y):
    return x/y

def bad_call():
    # This would raise a ZeroDivisionError, but it won't because the coroutine is call incorrectly.
    divide(1, 0)
```

In nearly all cases, any function that calls a coroutine must be a coroutine itself, and use await or yield in the call. When you are overriding a method defined in a superclass, consult the documentation to see if coroutines are allowed(the documentation should say that the method *may be a coroutine* or may *return a Future*)

```py
async def good_call():
    # await will unwrap the object returned by divide() and raise the exception
    await divide(1, 0)
```

Sometimes, you may want to "fire and forget" a coroutine without waiting for its result. In this case it is recommended to use `IOLoop.spawn_callback`, which makes the `IOLOOP` responsible for the call. If it fails, The IOLoop will log a stack Trace.

```py
# The IOLoop will catch the exception and print a stack trace in the logs. Note that this doesn't look like a normal call, since we pass the function object to be called by the IOLoop.
IOLoop.current().spawn_callback(divide, 1, 0)
```

Using `IOLoop.spawn_callback` in this way is recommended for functions using `@gen.coroutines`, but it is required for functions using async def (otherwise the coroutine runner will not start).
<p></p>

Finally, at the top level of a program, if the IOLoop is not yet running, you can start the IOLoop, run the coroutine, and then stop the IOLoop with the `IOLoop.run_sync` method. This is often used to start the main function of a batch-oriented program:
```py
# run_sync() dosen't take arguments, so we must wrap the call in a lambda.
IOLoop.current().run_sync(lambda: divide(0, 1))
```

## Coroutine patterns
### calling blocking functions
The simplest way to call a blocking functions from a coroutine is to use `IOLoop.run_in_executor`, which returns Future object.
```py
async def call_blocking():
    await IOLoop.current().run_in_executor(blocking_func, args)
```

### Parallelism
The mutli function accepts lists and dicts whose values are Future, and waits for all of those Futures in parallel:
```py
from tornado.gen import mutil

async def parallel_fetch(url1, url2):
    resp1, resp2 = await mutil([
        http_client.fetch(url1), http_client.fetch(url2)
    ])

async def parallel_fetch_many(urls):
    respones = await mutil([http_client.fetch(url) for url in urls])
```

In decorated coroutines, ou should use yield in the list or dict.
```py
@gen.coroutine
def parallel_fetch_decorated(url1, url2):
    resp1, resp2 = yield [
        http_client.fetch(url1),
        http_client.fetch(url2)
    ]
```
