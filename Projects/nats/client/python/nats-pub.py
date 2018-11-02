import asyncio
from nats.aio.client import Client as NATS
from nats.aio.errors import ErrConnectionClosed, ErrTimeout, ErrNoServers

async def run(loop):

    nc = NATS()

    await nc.connect("127.0.0.1:4222", loop=loop)

    async def message_handler(msg):
        subject = msg.subject
        reply = msg.reply
        data = msg.data.decode()

        print("received a message on '{sub} {rpl}': {data}".format(
            sub=subject, rpl=reply, data=data
        ))

    sid = await nc.subscribe("foo", cb=message_handler)

    print(sid)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run(loop))
    try:
        loop.run_forever()
    finally:
        loop.close()