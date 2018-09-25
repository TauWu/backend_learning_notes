# `Queue` example => a concurrent web spider

Tornado's `tornado.queues` module implements an asynchornous producer/consumer pattern for coroutines, analogous to the pattern implemented for threads by the Python standard libary's queue module.
<p></p>

A coroutine that yields Queue.get pauses until there is an item in the queue. If the queue has a max size se, a coroutine the yields Queue.put pauses until there is room for another item.
<p></p>

A Queue maintains a count of unfinished tasks, which begins at zero. put increments the count; task\_done decrements it.
<p></p>

In the web-spider example here, the queue begins containing only base\_url. When a worker fetches a page it parsers the links and puts new ones into the queue, then calls task\_done to decrement the counter one. Eventually, a worker fetches a page whose URLs have all been seen before, and there is also no work left in the queue. Thus, that worker's call to task\_done decrements the counter to zero. The main coroutine, which is waiting for join, is unpauseed and finishes.
<p></p>

[Click here](https://github.com/TauWu/backend_learning_notes/tree/master/高级语言学习/Python学习/tornado/users_guide/code/web_spider.py) to read web\_spider.py
