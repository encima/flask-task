#!/usr/bin/env ../tf/bin/

from tw import TW_Loader
import unittest


class Test_TW(unittest.TestCase):

    def setUp(self):
        self.twl = TW_Loader()

    def test_add(self):
        parsed_task = self.twl.add_task(
            "task:hello there project:test_project +tag +tags urgency:h")
        self.assertEqual(parsed_task['task'], 'hello there')
        self.assertEqual(parsed_task['project'], 'test_project')
        self.assertEqual(parsed_task['tags'], ['tag', 'tags'])
        self.assertEqual(parsed_task['urgency'], 'H')


if __name__ == '__main__':
    unittest.main()
