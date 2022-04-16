import contextlib
import time
from typing import Any, Iterator

from aiostatsd.client import StatsdClient as StatsdClientBase


class StatsdClient:
    """This class is needed in order to add the param :prefix: to the
    statsd client since is not supported in aiostatsd."""

    @staticmethod
    def from_host(
        prefix: str,
        host: str,
        port: int,
        packet_size: int = 512,
        flush_interval: float = 5.0,
    ) -> "StatsdClient":
        client = StatsdClientBase(host, port, packet_size, flush_interval)
        return StatsdClient(prefix, client)

    def __init__(self, prefix: str, client: StatsdClientBase) -> None:
        assert prefix is not None

        self._client = client
        self._prefix = prefix

    def send_counter(self, name: str, *args: Any, **kwargs: Any) -> None:
        name = "%s.%s" % (self._prefix, name)
        self._client.send_counter(name, *args, **kwargs)

    def send_timer(self, name: str, *args: Any, **kwargs: Any) -> None:
        name = "%s.%s" % (self._prefix, name)
        self._client.send_timer(name, *args, **kwargs)

    def send_gauge(self, name: str, *args: Any, **kwargs: Any) -> None:
        name = "%s.%s" % (self._prefix, name)
        self._client.send_gauge(name, *args, **kwargs)

    def incr(self, name: str, *args: Any, **kwargs: Any) -> None:
        name = "%s.%s" % (self._prefix, name)
        self._client.incr(name, *args, **kwargs)

    def decr(self, name: str, *args: Any, **kwargs: Any) -> None:
        name = "%s.%s" % (self._prefix, name)
        self._client.decr(name, *args, **kwargs)

    @contextlib.contextmanager
    def timer(self, name: str, rate: float = 1.0) -> Iterator[None]:
        start = time.time()
        try:
            yield
        finally:
            duration_sec = time.time() - start
            duration_msec = int(round(duration_sec * 1000))
            self.send_timer(name, duration_msec, rate=rate)

    async def run(self) -> None:
        await self._client.run()

    async def stop(self) -> None:
        await self._client.stop()


class EmptyStatsdClient:
    """Null implementation of StatsdClient."""

    def send_counter(self, name: str, *args: Any, **kwargs: Any) -> None:
        pass

    def send_timer(self, name: str, *args: Any, **kwargs: Any) -> None:
        pass

    def send_gauge(self, name: str, *args: Any, **kwargs: Any) -> None:
        pass

    def incr(self, name: str, *args: Any, **kwargs: Any) -> None:
        pass

    def decr(self, name: str, *args: Any, **kwargs: Any) -> None:
        pass

    @contextlib.contextmanager
    def timer(self, name: str, rate: float = 1.0) -> Iterator[None]:
        yield

    async def run(self) -> None:
        pass

    async def stop(self) -> None:
        pass
