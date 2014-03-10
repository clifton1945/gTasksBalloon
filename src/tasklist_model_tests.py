__author__ = 'CLIF'

import unittest
import tasklist_model as tl_m


class TasklistMainPredicate(unittest.TestCase):
    def setUp(self):
        # noinspection PyPep8Naming,PyPep8Naming
        self.longMessage = True
        # self.cut = tl_m.update_server

    def test_update_server(self):
        """
        process all functions: set from server, modify tasks, update server.
        @rtype: list
        @return: a modified list of tasklists with each tl maybe having modified task resources.
        """
        cut = tl_m.update_server()
        self.assertIsInstance(cut, list, 'expect a list of modified tasklist_tasks [tl_t]')


class TasklistSecondaryPredicates(unittest.TestCase):
    def setUp(self):
        # noinspection PyPep8Naming,PyPep8Naming
        self.longMessage = True

    def test_tasklist(self):
        cut = tl_m.get_server_tasklist_items()
        self.assertIsInstance(cut, list, "expect type list.")

    @unittest.skip("skipped: FORCE empty by looking for say 'XXX' or 'xitems' in the code.")
    def test_empty_tasklist(self):
        cut = tl_m.get_server_tasklist_items()
        # FORCE empty by looking for say 'XXX' or 'xitems'.
        self.assertIsInstance(cut, list, "expect type list even if there was no tasklists.")
        self.assertIs(len(cut), 0, "used when I force empty.")


if __name__ == '__main__':
    unittest.main()
