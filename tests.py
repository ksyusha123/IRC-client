from unittest import TestCase
from unittest.mock import patch
from client import IRCClient
from link_parser import get_opengraph_tags

test_client = IRCClient('test', 'irc.libera.chat')
actual = get_opengraph_tags('https://profteh.com/session_expired')
actual2 = get_opengraph_tags('https://github.com/')
print()


class TestClient(TestCase):
    @patch('client.IRCClient.send_cmd')
    def test_send_command(self, obj):
        test_client.process_commands('/join #test_room')
        obj.assert_called_once_with('JOIN #TEST_ROOM', '#test_room')

    @patch('client.IRCClient.send_cmd')
    def test_send_empty_message(self, obj):
        test_client.process_commands('')
        obj.assert_called_once_with("PRIVMSG", f"{test_client.channel} :")

    def test_parse_simple_link(self):
        actual = get_opengraph_tags('https://habr.com/ru/post/141209/')
        self.assertIsNot(len(actual), 0)
        self.assertEqual(actual['site_name'], 'Модуль Mock: макеты-пустышки в тестировании')

    def test_empty_link(self):
        with self.assertRaises(Exception):
            get_opengraph_tags('')

    @patch('re.findall', return_value=[])
    def test_empty_tags(self):
        actual = get_opengraph_tags('https://profteh.com/')
        self.assertEqual(actual, {})
