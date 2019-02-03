import asyncio
import ucp_py as ucp

ucp.init()


async def serve(ep, listener):
    print('serving', ep)
    ucp.destroy_ep(ep)
    ucp.stop_listener(listener)
    print('stopped', ep)


async def main():
    a = ucp.start_listener(serve, listener_port=13337, is_coroutine=True)
    if None == a:
        print("Unable to listen")
    ucp.get_endpoint(b'10.149.160.6', 13337)
    b = ucp.start_listener(serve, listener_port=13338, is_coroutine=True)
    if None == a:
        print("Unable to listen")
    ucp.get_endpoint(b'10.149.160.6', 13338)
    await a.coroutine
    print('finished a')
    await b.coroutine
    print('finished b')


if __name__ == '__main__':
    asyncio.run(main())
