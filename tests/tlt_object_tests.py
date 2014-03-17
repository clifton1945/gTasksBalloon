import unittest
from datetime import datetime
import src.tlt_object as tlt
import src.task_helpers as h


### GLOBALS
# PILOT = tlt.Pilot


class FunctionTests(unittest.TestCase):
    def setUp(self):
        """
        tl_rsrc: tasklist rsrc
        {
          "kind": "tasks#taskList",
          "id": string,
          "etag": string,
          "title": string,
          "updated": datetime,
          "selfLink": string
        }
        t_list: task rsrc
        {
          "kind": "tasks#task",
          "id": string,
          "etag": etag,
          "title": string,
          "updated": datetime,
          "selfLink": string,
          "parent": string,
          "position": string,
          "notes": string,
          "status": string,
          "due": datetime,
          "completed": datetime,
          "deleted": boolean,
          "hidden": boolean,
          "links": [
            {
              "type": string,
              "description": string,
              "link": string
            }
          ]
        }

        """
        # noinspection PyPep8Naming,PyPep8Naming
        self.longMessage = True
        _now = datetime.now()
        # set 3 days before now
        self.mock_now = _now
        _day = (_now.day + 3) % 28
        _due = _now.replace(day=_day)
        _due_str = h.rfc_from_(_due)
        self.mock_due_str = _due_str
        # tlt dictionary
        self.mock_tl_rsrc = tl_rsrc = {
            "kind": "tasks#taskList",
            "id": "id here",
            "etag": "etag here.",
            "title": "PILOTS",
        }
        self.mock_task_hide = t_list = {
            "title": "mock_needsAction",
            "status": "needsAction",
            "due": self.mock_due_str,
            "notes": "a mock task."}

        self.mock_tlt_obj = {"tl_rsrc": tl_rsrc, "t_list": t_list}
        self.mock_tlt_obj_list = [self.mock_tlt_obj]


class ShelvedTltTests(unittest.TestCase):
    def setUp(self):
        """
        tl_rsrc: tasklist rsrc
        {
          "kind": "tasks#taskList",
          "id": string,
          "etag": string,
          "title": string,
          "updated": datetime,
          "selfLink": string
        }
        t_list: task rsrc
        {
          "kind": "tasks#task",
          "id": string,
          "etag": etag,
          "title": string,
          "updated": datetime,
          "selfLink": string,
          "parent": string,
          "position": string,
          "notes": string,
          "status": string,
          "due": datetime,
          "completed": datetime,
          "deleted": boolean,
          "hidden": boolean,
          "links": [
            {
              "type": string,
              "description": string,
              "link": string
            }
          ]
        }

        """
        # noinspection PyPep8Naming,PyPep8Naming
        self.longMessage = True
        # data
        tlt_obj_list = h.unshelve_from_db()
        tlt_obj = {}
        assert h.is_valid_tlt_list_(tlt_obj_list, True, self._testMethodName)
        self.tlt_obj_list = tlt_obj_list
        l = len(tlt_obj_list)
        if l > 0:
            assert h.is_valid_tlt_(tlt_obj_list[0], True, self._testMethodName)
            tlt_obj = tlt_obj_list[0]
        if l > 1:
            assert tlt_obj_list[1] != tlt_obj
        self.tlt_obj_list = tlt_obj_list
        self.tlt_obj = tlt_obj

        _now = datetime.now()
        # set 3 days before now
        self.mock_now = _now
        _day = (_now.day + 3) % 28
        _due = _now.replace(day=_day)
        _due_str = h.rfc_from_(_due)

    def test_data_valid(self):
        """
        checks tlt_list and tlt obj are valid
        AND
        confirms tlt_rsrc 0 != tlt_rsrc 1
        """
        tlt_obj_list = self.tlt_obj_list

        do_print = False
        # list of tasklists
        h.is_valid_tlt_list_(tlt_obj_list, do_print, self._testMethodName)

    def test_sift_by_rule__near_due(self):
        cut = tlt.Rules.sift_by_rule__near_due  # TODO FIX  this test fails cause cut not right yet.
        do_print = False
        tlt_lst = cut(self.tlt_obj_list)

        self.assertTrue(h.is_valid_tlt_list_(tlt_lst, do_print, self)
                        , "exp: setUp data list is valid.")

    @unittest.skip("skip: test_update_data_()  till base is stable.")
    def test_update_data_(self):
        cut = tlt.update_data_

        exp = cut(self.tlt_obj_list)

        self.assertIsInstance(exp, list, "expect a tlt_obj_list ")
        assert len(exp) > 0  # expect at least PILOTS tasklist.
        h.print_tlt_list_(exp, self)

        tlt_obj = exp[0]
        self.assertIsInstance(tlt_obj, dict, "expect tlt is dict.")
        self.assertIsInstance(tlt_obj['tl_rsrc'], dict, "exp: tl_rsrc is a dict resource")
        self.assertIsInstance(tlt_obj['t_list'], list, "exp: a list of tasks rsrcs.")
        h.print_tlt_(tlt_obj)


class ServerTltTests(unittest.TestCase):
    def setUp(self):
        """
        tl_rsrc: tasklist rsrc
        {
          "kind": "tasks#taskList",
          "id": string,
          "etag": string,
          "title": string,
          "updated": datetime,
          "selfLink": string
        }
        t_list: task rsrc
        {
          "kind": "tasks#task",
          "id": string,
          "etag": etag,
          "title": string,
          "updated": datetime,
          "selfLink": string,
          "parent": string,
          "position": string,
          "notes": string,
          "status": string,
          "due": datetime,
          "completed": datetime,
          "deleted": boolean,
          "hidden": boolean,
          "links": [
            {
              "type": string,
              "description": string,
              "link": string
            }
          ]
        }

        """
        # noinspection PyPep8Naming,PyPep8Naming
        self.longMessage = True
        do_print = False
        # data
        tlt_obj_list = h.unshelve_from_db()
        tlt_obj = {}
        assert h.is_valid_tlt_list_(tlt_obj_list, do_print, self._testMethodName)
        self.tlt_obj_list = tlt_obj_list
        l = len(tlt_obj_list)
        if l > 0:
            assert h.is_valid_tlt_(tlt_obj_list[0], do_print, self._testMethodName)
            tlt_obj = tlt_obj_list[0]
        if l > 1:
            assert tlt_obj_list[1] != tlt_obj
        # test data
        self.tlt_obj_list = tlt_obj_list
        self.tlt_obj = tlt_obj

        _now = datetime.now()
        # set 3 days before now
        self.mock_now = _now
        _day = (_now.day + 3) % 28
        _due = _now.replace(day=_day)
        _due_str = h.rfc_from_(_due)

    @unittest.skip("SKIP: unless shelve data is corrupt.")
    def test_serve_data(self):
        do_print = True
        my_name = self._testMethodName
        cut = tlt.serve_data

        tlt_obj_list = cut()

        # list of tasklists
        self.assertTrue(h.is_valid_tlt_list_(tlt_obj_list, do_print, my_name))

    def test_update_shelve(self):
        do_print = False
        my_name = self._testMethodName
        cut = tlt.update_shelve

        tlt_obj_list = cut()

        # list of tasklists
        self.assertTrue(h.is_valid_tlt_list_(tlt_obj_list, do_print, my_name))



if __name__ == '__main__':
    tlt_list = tlt.update_server_()
    unittest.main()