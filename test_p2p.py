import io
import subprocess
import time
import unittest
from io import *
from unittest.mock import patch

from comm import *
from console import *


class TestConsole(unittest.TestCase):

    def test_register(self):
        captured_output = StringIO()
        sys.stdout = captured_output
        fake_inputs = ['test1', '1.1.1.1']
        with patch('builtins.input', side_effect=fake_inputs):
            ret = register_to_db()
            self.assertEqual(ret, True)

        fake_inputs = ['test2', '1.1.1.2']
        with patch('builtins.input', side_effect=fake_inputs):
            ret = register_to_db()
            self.assertEqual(ret, True)

        fake_inputs = ['test3', '1.1.1.3']
        with patch('builtins.input', side_effect=fake_inputs):
            ret = register_to_db()
            self.assertEqual(ret, True)

    def test_list_clients(self):
        with patch('sys.stdout', new=StringIO()) as fake_stdout:
            list_clients()
            self.assertIn('test1  1.1.1.1\ttest2  1.1.1.2\ttest3  1.1.1.3', fake_stdout.getvalue())

    def test_help(self):
        with patch('sys.stdout', new=StringIO()) as fake_stdout:
            help_show()
            self.assertIn("Commands:\n\tlist: list all clients\n\tconnect <ip> <port>: connect to a "
                          "client\n\tregister: register a new client\n\tquit: quit the program\n\thistory: show "
                          "connection history\n\thelp: show help text", fake_stdout.getvalue())


class TestCommunication(unittest.TestCase):

    def test_socket_communication(self):
        self.server_thread = threading.Thread(target=server_unittest)
        self.server_thread.start()

        sleep(3)

        original_stdout = sys.stdout
        sys.stdout = io.StringIO()

        client_unittest()
        output = sys.stdout.getvalue().strip()
        expected_output = 'Accepted connection from 127.0.0.1\nReceived data: Hello from the client\nConnection ' \
                          'closed\nReceived response: Hello from the client\nConnection closed'

        expected_output_tuple = tuple(expected_output.split('\n'))

        output_list = output.split('\n')

        for i in output_list:
            self.assertIn(i, expected_output_tuple)

        sys.stdout = original_stdout

