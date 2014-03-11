
import unittest
import src.tasklist_model as tl_m


class TasklistSecondaryPredicates(unittest.TestCase):
    def setUp(self):
        # noinspection PyPep8Naming,PyPep8Naming
        self.longMessage = True
        self.lotls = lotls = tl_m.get_server_tasklist_items()
        assert isinstance(lotls, list)
        self.tl = tl = [tl for tl in lotls if tl['title'] == 'TRIALS'][0]
        assert isinstance(tl, dict)
        pass

    def test_get_server_tl_task_items_in_(self):
        cut = tl_m.get_server_tl_task_items_in_(self.lotls)

        self.assertIsInstance(cut, list, "expect type list.")

    @unittest.skip("skipped: FORCE empty by looking for say 'XXX' or 'xitems' in the code.")
    def test_empty_tasklist(self):
        cut = tl_m.get_server_tasklist_items()
        # FORCE empty by looking for say 'XXX' or 'xitems'.
        self.assertIsInstance(cut, list, "expect type list even if there was no tasklists.")
        self.assertIs(len(cut), 0, "used when I force empty.")


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


if __name__ == '__main__':
    unittest.main()
