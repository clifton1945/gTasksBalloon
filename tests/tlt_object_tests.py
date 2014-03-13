
import unittest
import src.tlt_object as cut


class TlTSecondaryPredicates(unittest.TestCase):
    def setUp(self):
        # noinspection PyPep8Naming,PyPep8Naming
        self.longMessage = True

    def test_unshelve_pilot_data(self):
        exp = cut.unshelve_pilot_data()
        self.assertIsInstance(exp, list, "expect a tlt_list ")
        if len(exp) > 0:
            exp = exp[0]  # NOTE this test is for tlt -> a list of tuples (tl, list of tasks)
            self.assertIsInstance(exp[0], dict, "tl is tasklist resource ")
            self.assertIsInstance(exp[1], list, "list of tasks")


class TasklistMainPredicate(unittest.TestCase):
    def setUp(self):
        # noinspection PyPep8Naming,PyPep8Naming
        self.longMessage = True
        # self.cut = tl_m.update_server

    def test_update_shelve(self):
        exp = cut.update_shelve()
        self.assertIsInstance(exp, list, "expect tlt_list ")
        if len(exp) > 0:
            exp = exp[0]  # NOTE this test is for tlt -> a list of tuples (tl, list of tasks)
            self.assertIsInstance(exp[0], dict, "tl is tasklist resource ")
            self.assertIsInstance(exp[1], list, "list of tasks")

    def test_update_pilot(self):
        exp = cut.update_pilot()
        self.assertIsInstance(exp, list, "expect tlt_list with only PILOTS objects. ")
        if len(exp) > 0:
            exp = exp[0]  # NOTE this test is for tlt -> a list of tuples (tl, list of tasks)
            self.assertIsInstance(exp[0], dict, "expect tl is a tasklist resource ")
            self.assertIsInstance(exp[1], list, "espect a list of tasks")


if __name__ == '__main__':
    unittest.main()
