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
        # locals
        # noinspection PyPep8Naming,PyPep8Naming
        self.longMessage = True
        do_print = False
        my_name = self._testMethodName

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
        do_print = False
        my_name = "ShelvedTltTests.setUp." + self._testMethodName

        # data
        tlt_obj_list = h.unshelve_from_db()
        tlt_obj = {}
        assert h.is_valid_tlt_list_(tlt_obj_list, do_print, my_name)
        self.tlt_obj_list = tlt_obj_list
        l = len(tlt_obj_list)
        if l > 0:
            assert h.is_valid_tlt_(tlt_obj_list[0], do_print, my_name)
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
        # locals
        do_print = False
        msg = self._testMethodName

        tlt_obj_list = self.tlt_obj_list

        # list of tasklists
        h.is_valid_tlt_list_(tlt_obj_list, do_print, msg)

    #@unittest.skip("skip: test_update_data_()  till base is stable.")
    def test_update_data_(self):
        cut = tlt.update_data_
        # locals
        do_print = False
        msg = self._testMethodName
        data = self.tlt_obj_list
        exp = cut(data)

        tst = h.is_valid_tlt_list_(data, do_print, msg)


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
        my_name = "ServerTltTests.setUp." + self._testMethodName

        # data
        tlt_obj_list = h.unshelve_from_db()
        tlt_obj = {}
        assert h.is_valid_tlt_list_(tlt_obj_list, do_print, my_name)
        self.tlt_obj_list = tlt_obj_list
        l = len(tlt_obj_list)
        if l > 0:
            assert h.is_valid_tlt_(tlt_obj_list[0], do_print, my_name)
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
        do_print = False
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
    tlt_list = tlt.update_shelve()
    print '************* UPDATED SHELVE *********'

    # unittest.main()