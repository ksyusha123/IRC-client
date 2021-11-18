from unittest import TestCase
from unittest.mock import patch
from client import IRCClient as client
from link_parser import get_opengraph_tags

test_client = client('test', 'irc.libera.chat')


class TestClient(TestCase):

    @patch('client.IRCClient.send_cmd')
    def test_send_command(self, obj):
        test_client.process_commands('/join #test_room')
        obj.assert_called_once_with('JOIN', '#test_room')

    @patch('client.IRCClient.send_cmd')
    def test_send_empty_message(self, obj):
        test_client.process_commands('')
        obj.assert_called_once_with("PRIVMSG", f"{test_client.channel} :")

    def test_parse_simple_link(self):
        actual = get_opengraph_tags('https://habr.com/ru/post/141209/')
        self.assertIsNot(len(actual), 0)
        self.assertEqual(actual['site_name'], 'Хабр')

    def test_empty_link(self):
        with self.assertRaises(TypeError):
            get_opengraph_tags('')


