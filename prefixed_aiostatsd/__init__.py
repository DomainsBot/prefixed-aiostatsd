import contextlib

from aiostatsd.client import StatsdClient as StatsdClientBase


class StatsdClient:
    """This class is needed in order to add the param :prefix: to the
    statsd client since is not supported in aiostatsd."""

    @staticmethod
    def from_host(prefix, host, port, packet_size=512, flush_interval=5.0):
        client = StatsdClientBase(host, port, packet_size, flush_interval)
        return StatsdClient(prefix, client)

    def __init__(self, prefix, client):
        assert prefix is not None

        self._client = client
        self._prefix = prefix

    def send_counter(self, name, *args, **kwargs):
        name = '%s.%s' % (self._prefix, name)
        self._client.send_counter(name, *args, **kwargs)

    def send_timer(self, name, *args, **kwargs):
        name = '%s.%s' % (self._prefix, name)
        self._client.send_timer(name, *args, **kwargs)

    def send_gauge(self, name, *args, **kwargs):
        name = '%s.%s' % (self._prefix, name)
        self._client.send_gauge(name, *args, **kwargs)

    def incr(self, name, *args, **kwargs):
        name = '%s.%s' % (self._prefix, name)
        self._client.incr(name, *args, **kwargs)

    def decr(self, name, *args, **kwargs):
        name = '%s.%s' % (self._prefix, name)
        self._client.decr(name, *args, **kwargs)

    @contextlib.contextmanager
    def timer(self, name, rate=1.0):
        name = '%s.%s' % (self._prefix, name)
        yield from self._client.timer(name, rate)

    async def run(self):
        await self._client.run()

    async def stop(self):
        await self._client.stop()


class EmptyStatsdClient:
    """Null implementation of StatsdClient."""

    def send_counter(self, name, *args, **kwargs):
        pass

    def send_timer(self, name, *args, **kwargs):
        pass

    def send_gauge(self, name, *args, **kwargs):
        pass

    def incr(self, name, value=1, rate=1.0):
        pass

    def decr(self, name, value=1, rate=1.0):
        pass

    @contextlib.contextmanager
    def timer(self, name, rate=1.0):
        yield

    async def run(self):
        pass

    async def stop(self):
        pass
