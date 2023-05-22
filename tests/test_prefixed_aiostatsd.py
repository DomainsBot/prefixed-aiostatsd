import unittest
from unittest.mock import MagicMock

from prefixed_aiostatsd import EmptyStatsdClient, StatsdClient


class StatsdClientTest(unittest.TestCase):
    def setUp(self):
        self.client = MagicMock()
        self.subject = StatsdClient("prefix", self.client)

    def test_when_sending_counter_then_it_sends_it_with_the_right_prefix(self):
        self.subject.send_counter("test")
        self.client.send_counter.assert_called_with("prefix.test")

    def test_when_sending_timer_then_it_sends_it_with_the_right_prefix(self):
        self.subject.send_timer("test")
        self.client.send_timer.assert_called_with("prefix.test")

    def test_when_sending_gauge_then_it_sends_it_with_the_right_prefix(self):
        self.subject.send_gauge("test")
        self.client.send_gauge.assert_called_with("prefix.test")

    def test_when_incrementing_then_it_sends_it_with_the_right_prefix(self):
        self.subject.incr("test")
        self.client.incr.assert_called_with("prefix.test")

    def test_when_decrementing_then_it_sends_it_with_the_right_prefix(self):
        self.subject.decr("test")
        self.client.decr.assert_called_with("prefix.test")

    def test_when_using_timer_then_it_does_not_break(self):
        with self.subject.timer("test"):
            pass
        self.client.send_timer.assert_called_with("prefix.test", 0, rate=1.0)

    def test_when_adding_a_suffix_then_it_returns_the_same_type(self):
        subject = self.subject.with_suffix("suffix")

        self.assertIsInstance(subject, type(self.subject))

    def test_when_adding_a_suffix_then_it_sends_metrics_including_the_suffix(self):
        self.subject.with_suffix("extra").incr("test")
        self.client.incr.assert_called_with("prefix.extra.test")


class EmptyStatsdClientTest(unittest.TestCase):
    def setUp(self):
        self.subject = EmptyStatsdClient()

    def test_when_calling_distinct_operations_then_it_does_not_break(self):
        try:
            self.subject.send_counter("test")
            self.subject.send_timer("test")
            self.subject.send_gauge("test")
            self.subject.incr("test")
            self.subject.decr("test")

            with self.subject.timer("test"):
                pass

        except Exception as e:
            raise AssertionError(f"Unexpected error: {e}")

    def test_when_adding_a_suffix_then_it_returns_the_same_type(self):
        subject = self.subject.with_suffix("suffix")

        self.assertIsInstance(subject, EmptyStatsdClient)
