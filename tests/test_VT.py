# -*- coding: utf-8 -*-
import mock
import VertretungPlan
import unittest
import os

os.chdir("../")


class TestVertretungPlan(unittest.TestCase):
    def setUp(self):
        with open("tests/test_VT_room.html") as f:
            self.room = f.read()
        with open("tests/test_VT_no_room.html") as f:
            self.no_room = f.read()

        self.expected_room = '{"2a": [{"1. Stunde": ["En", "Ge R220"]}]}'
        self.expected_no_room = '{"2a": [{"1. Stunde": ["En", "Aufgaben"]}]}'

    def test_with_room(self):
        m = mock.mock_open(read_data=self.room)
        with mock.patch('VertretungPlan.open', m, create=True):
            VertretungPlan.main()

        handle = m()
        handle.write.assert_called_once_with(self.expected_room)

    def test_without_room(self):
        m = mock.mock_open(read_data=self.no_room)
        with mock.patch('VertretungPlan.open', m, create=True):
            VertretungPlan.main()

        handle = m()
        handle.write.assert_called_once_with(self.expected_no_room)


if __name__ == '__main__':
    unittest.main()
