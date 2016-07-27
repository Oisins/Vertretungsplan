# -*- coding: utf-8 -*-
#
# (c) 2016 Oisín Smith All Rights Reserved
#

from mock import MagicMock, mock_open, patch
import unittest
import config
import logging
import json


class TestVertretungPlan(unittest.TestCase):
    def setUp(self):
        logging.disable(logging.CRITICAL)  # Disable Logging

    def tearDown(self):
        logging.disable(logging.NOTSET)  # Re-enable Logging

    @patch("os.path.exists", MagicMock().return_value(True))
    def test_get(self):
        test_dict = {'log': 'ABC', 'file': 'test.txt', 'Item': 'ABC', 'url': 'http://www.test.org'}

        with patch('config.open', mock_open(read_data=json.dumps(test_dict)), create=True):
            conf = config.Config("test.txt")
            for key, value in test_dict.items():
                self.assertEqual(value, conf.get(key))  # Test every value in dict

            string = "Default"
            self.assertEqual(string, conf.get("Missing", string))  # Test Default return Value


if __name__ == '__main__':
    unittest.main()
