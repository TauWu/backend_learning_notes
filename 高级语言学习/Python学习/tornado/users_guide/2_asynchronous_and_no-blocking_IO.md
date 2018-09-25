# ASYNCHRONOUS AND NO-BLOCKING IO

Real-Time web features require a long-lived mostly-idle connection per user. In a traditional synchronous web server, this implies devoting one thread to each other, which can be expensive. To **minimize the cost of concurrent connections**, Tornado uses a single-threaded event-loop. Thus, all application code shoule aim to be asynchronous and non-blocking because only one operation can be active as a time.

## Blocking
A function blocks when it waits for something happen before returning. A function may block for many reasons: network IO, disk IO, mutexes, etc. In fact, every functions blocks, at least a little bit, while it is running and using CPU.

## Asynchronous
An asynchronous functions returns befaore it is finished, and generally causes some work to happen in the background before triggering some future action in the application(as opposed to normal synchronous functions, which do everything they are going to do bdfore returning). There are many styles of asynchronous interfaces:
- Callback argument
- Return a placeholder (Future, Promise, Deferred)
- Deliver a queue
- Callback registry (e.g. POSIX signals)
<p></p>

Regardless of which types of interface is used, asynchronous functions by def interact differently with their callers; **there is no free way to make a synchronous functions asynchronous in a way that is transplant to its callers**(sys like gevent use lightweight threads to offer performance comparable to asynchronous systems, however, they don't actually make things asynchronous).
<p></p>

Asynchronous operations in Tornado generally return placeholder objects(Futures), with the exception of some low-level components like the IOLoop that use callbacks. Futures are usually transformed into their result with the `await` or `yield` keyword.

## Examples

- Sample synchronous function

```py
from tornado.httpclient import HTTPClient

def sync_fetch(url):
    client = HTTPClient()
    resp = client.fetch(url)
    return resp.body
```

- Sample asynchronous function

```py
from tornado.httpclient import AsyncHTTPClient

async def async_fetch(url):
    client = AsyncHTTPClient(url)
    resp = await client.fetch(url)
    return resp.body
```

- Older version with tornado.gen

```py
from tornado.httpclient import AsyncHTTPClient
from tornado import gen

@gen.coroutine
def async_fetch_gen(url)
    client = AsyncHTTPClient()
    resp = yield client.fetch(url)
    raise gen.Return(resp.body)
```

- Manual Use

```py
from tornado.concurrent import Future
from tornado.httpclient import AsyncHTTPClient

def async_fetch_manual(url):
    client = AsyncHTTPClient()
    future = Future()
    fetch_future = client.fetch(url)
    def on_fetch(f):
        future.set_result(f.result().boby)
    fetch_future.add_done_callback(on_fetch)
    return future
```
We can see that this function **return this Future object before the fetch is done**, which makes coroutines asynchronous,
