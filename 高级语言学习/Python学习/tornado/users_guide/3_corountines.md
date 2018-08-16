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
