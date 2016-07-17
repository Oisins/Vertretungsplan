# -*- coding: utf-8 -*-
#
# (c) 2016 Oisín Smith All Rights Reserved
#

import mock
import unittest
import VertretungPlan
import logging
import json


class TestVertretungPlan(unittest.TestCase):
    def setUp(self):
        logging.disable(logging.CRITICAL)  # Disable Logging
        with open("tests/test_VT_room.html", "rb") as f:
            self.room = f.read()
        with open("tests/test_VT_no_room.html", "rb") as f:
            self.no_room = f.read()

        self.expected_room = json.loads('{"date": "2016-03-11 00:00:00", '
                                        '"data": {"2a": [{"1. Stunde": ["En", "Ge R220"]}]}, '
                                        '"created": "2016-03-10 08:25:00"}')

        self.expected_no_room = json.loads('{"date": "2016-03-11 00:00:00", '
                                           '"data": {"2a": [{"1. Stunde": ["En", "Aufgaben"]}]}, '
                                           '"created": "2016-03-10 08:25:00"}')
        VertretungPlan.Uploader = mock.MagicMock()

    def tearDown(self):
        logging.disable(logging.NOTSET)  # Enable Logging

    def test_with_room(self):
        self.run_mock(self.room, self.expected_room)

    def test_without_room(self):
        self.run_mock(self.no_room, self.expected_no_room)

    def run_mock(self, dump, input_file, expected):
        """
        Takes a Mock file, runs the VT Program and then compared the results
        :param input_file: Mock of file to be processed
        :param expected: Expected Json output
        :return:
        """
        mock_open = mock.mock_open(read_data=input_file)
        mock_listdir = mock.MagicMock(return_value=["File.htm"])

        with mock.patch('os.listdir', mock_listdir):
            with mock.patch('builtins.open', mock_open, create=True):  # Mock open()
                with mock.patch('json.dumps') as dump:  # Mock json.dumps()

                    VertretungPlan.main()

                    call_args, call_kwargs = dump.call_args  # args and keyword_args from Mock call
                    output = str(call_args[0]).replace("\'", "\"")  # format Json

                    self.assertEqual(json.loads(output), expected)


if __name__ == '__main__':
    unittest.main()
