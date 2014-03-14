
import unittest
import _bsddb
import src.tlt_object as tlt


 ### GLOBALS
PILOT = tlt.Pilot


class PilotTests(unittest.TestCase):

    def setUp(self):
        # noinspection PyPep8Naming,PyPep8Naming
        self.longMessage

    def test_serve_pilot_data(self):
        tlt_obj_list = PILOT.serve_pilot_data()
        self.assertIsInstance(tlt_obj_list, list, "expect a tlt_obj_list ")
        assert len(tlt_obj_list) == 1  # expect just PILOTS tasklist rsrc.
        tl_rsrc, task_list = tlt_obj_list[0]
        self.assertIsInstance(tl_rsrc, dict, "tl is tasklist resource ")
        self.assertIsInstance(task_list, list, "list of tasks")
        print "serve_pilot_data ->\n  " \
            "tasklist title:{} has {} task rsrcs.".\
            format(tl_rsrc['title'], len(task_list))

    def test_update_pilot_shelve(self):
        tlt_obj_list = PILOT.update_pilot_shelve()
        self.assertIsInstance(tlt_obj_list, list, "expect a tlt_obj_list ")

    def test_unshelve_pilot_data(self):
        tlt_obj_list = PILOT.unshelve_pilot_data()
        self.assertIsInstance(tlt_obj_list, list, "expect a tlt_obj_list ")
        assert len(tlt_obj_list) == 1  # expect just PILOTS tasklist rsrc.
        tl_rsrc, task_list = tlt_obj_list[0]
        self.assertIsInstance(tl_rsrc, dict, "tl is tasklist resource ")
        self.assertIsInstance(task_list, list, "list of tasks")
        print "unshelve_pilot_data ->.\n  " \
            "tasklist title:{} has {} task rsrcs.".\
            format(tl_rsrc['title'], len(task_list))

    def test_update_date_(self):
        cut = tlt.update_data_

        tlt_obj_list = data = PILOT.unshelve_pilot_data()
        self.assertIsInstance(cut(data), list, 'expect a list w/ or w/o data.')



class TlTSecondaryPredicates(unittest.TestCase):
    def setUp(self):
        # noinspection PyPep8Naming,PyPep8Naming
        self.longMessage = True


class TasklistMainPredicate(unittest.TestCase):
    def setUp(self):
        # noinspection PyPep8Naming,PyPep8Naming
        self.longMessage = True
        # self.tlt = tl_m.update_server

    def test_update_shelve(self):
        exp = tlt.update_shelve()
        self.assertIsInstance(exp, list, "expect tlt_obj_list ")
        if len(exp) > 0:
            exp = exp[0]  # NOTE this test is for tlt -> a list of tuples (tl, list of tasks)
            self.assertIsInstance(exp[0], dict, "tl is tasklist resource ")
            self.assertIsInstance(exp[1], list, "list of tasks")


if __name__ == '__main__':
    unittest.main()
