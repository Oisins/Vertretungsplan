# -*- coding: utf-8 -*-
#
# (c) 2016 Oisín Smith All Rights Reserved
#

import mock
import unittest
import VertretungPlan


class TestVertretungPlan(unittest.TestCase):
    def setUp(self):
        with open("tests/test_VT_room.html") as f:
            self.room = f.read()
        with open("tests/test_VT_no_room.html") as f:
            self.no_room = f.read()

        self.expected_room = '{"2a": [{"1. Stunde": ["En", "Ge R220"]}]}'
        self.expected_no_room = '{"2a": [{"1. Stunde": ["En", "Aufgaben"]}]}'
        VertretungPlan.Uploader = mock.MagicMock()

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
