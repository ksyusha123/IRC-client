from unittest import TestCase
from unittest.mock import patch
from client import IRCClient
from link_parser import get_opengraph_tags
import re
from chat_window import ChatWindow

test_client = IRCClient('test', 'irc.libera.chat')


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
        self.assertEqual(actual['site_name'], 'Модуль Mock: макеты-пустышки в тестировании')

    def test_empty_link(self):
        with self.assertRaises(Exception):
            get_opengraph_tags('')

    @patch('re.findall', return_value=[])
    def test_empty_tags(self, obj):
        actual = get_opengraph_tags('https://profteh.com/')
        self.assertEqual(actual, {})

    @patch('re.findall', return_value=[('og:site_name', 'content="Купить баллы за питон-таски без регистрации и смс"')])
    def test_no_image_tag(self, obj):
        actual = get_opengraph_tags('https://mail.ru/')
        self.assertEqual(actual, {'site_name': 'Купить баллы за питон-таски без регистрации и смс'})


