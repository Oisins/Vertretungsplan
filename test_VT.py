# -*- coding: utf-8 -*-
#
# (c) 2016 Oisín Smith All Rights Reserved
#

from mock import MagicMock, mock_open, patch
import unittest
import VertretungPlan
import logging
import json


class TestVertretungPlan(unittest.TestCase):
    def setUp(self):
        logging.disable(logging.CRITICAL)  # Disable Logging

        self.room = open("tests/test_VT_room.html", "rb").read()
        self.no_room = open("tests/test_VT_no_room.html", "rb").read()

        self.expected_room = json.loads('{"date": "2016-03-11 00:00:00", '
                                        '"data": {"2a": [{"1. Stunde": ["En", "Ge R220"]}]}, '
                                        '"created": "2016-03-10 08:25:00"}')

        self.expected_no_room = json.loads('{"date": "2016-03-11 00:00:00", '
                                           '"data": {"2a": [{"1. Stunde": ["En", "Aufgaben"]}]}, '
                                           '"created": "2016-03-10 08:25:00"}')
        VertretungPlan.Uploader = MagicMock()

    def tearDown(self):
        logging.disable(logging.NOTSET)  # Re-enable Logging

    def test_with_room(self):
        self.run_mock(self.room, self.expected_room)

    def test_without_room(self):
        self.run_mock(self.no_room, self.expected_no_room)

    @patch("json.dumps")  # Mock json.dumps
    @patch("os.path")  # Mock os.path
    @patch("os.listdir", MagicMock(return_value=["File.htm"]))  # Mock os.listdir
    def run_mock(self, input_file, expected, *args):
        """
        Takes a Mock file, runs the VT Program and then compared the results
        :param input_file: Mock of file to be processed
        :param expected: Expected Json output
        :return:
        """
        open_mock = mock_open(read_data=input_file)

        print(input_file)
        dump = args[1]  # Json Dumps Mock

        with patch('builtins.open', open_mock, create=True):  # Mock open()

            VertretungPlan.main()

            call_args, call_kwargs = dump.call_args  # args and keyword_args from Mock call
            output = str(call_args[0]).replace("\'", "\"")  # format Json

            self.assertEqual(json.loads(output), expected)


if __name__ == '__main__':
    unittest.main()
