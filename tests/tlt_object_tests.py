import unittest
from datetime import datetime
import src.tlt_object as tlt
import src.task_helpers as h


### GLOBALS
PILOT = tlt.Pilot


def print_tlt_(s, tlt_obj):
    # noinspection PyProtectedMember
    print "{}->\n    " \
        "tlt[tl_rsrc][title]:{}, len(tlt[t_list]):{}.". \
        format(s._testMethodName, tlt_obj['tl_rsrc']['title'], len(tlt_obj['t_list']))


def print_tlt_list_(s, tlt_list):
    # noinspection PyProtectedMember
    print "{}->\n  " \
        "tlt list, len(tlt_list):{}.". \
        format(s._testMethodName, len(tlt_list))


class PilotTests(unittest.TestCase):
    def setUp(self):
        """
        tasklist rsrc
        {
          "kind": "tasks#taskList",
          "id": string,
          "etag": string,
          "title": string,
          "updated": datetime,
          "selfLink": string
        }
        task rsrc
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
        self.mock_tasklist = tl = {
            "kind": "tasks#taskList",
            "id": "id here",
            "etag": "etag here.",
            "title": "PILOTS",
        }
        self.mock_task_hide = t = {
            "title": "mock_needsAction",
            "status": "needsAction",
            "due": self.mock_due_str,
            "notes": "a mock task."}
        self.mock_tlt_obj = (tl, t)
        self.mock_tlt_obj_list = [self.mock_tlt_obj]

    def test_serve_pilot_data(self):
        tlt_obj_list = PILOT.serve_pilot_data()
        self.assertIsInstance(tlt_obj_list, list, "expect a tlt_obj_list ")
        assert len(tlt_obj_list) == 1  # expect just PILOTS tasklist rsrc.
        tlt_obj = tlt_obj_list[0]
        self.assertIsInstance(tlt_obj, dict, "expect tlt is dict.")
        self.assertIsInstance(tlt_obj['tl_rsrc'], dict, "exp: tl_rsrc is a dict resource")
        self.assertIsInstance(tlt_obj['t_list'], list, "exp: a list of tasks rsrcs.")
        print_tlt_(self, tlt_obj)

    def test_update_pilot_shelve(self):
        tlt_obj_list = PILOT.update_pilot_shelve()
        self.assertIsInstance(tlt_obj_list, list, "expect a tlt_obj_list ")
        assert len(tlt_obj_list) > 0  # expect just PILOTS tasklist rsrc.
        tlt_obj = tlt_obj_list[0]
        print_tlt_(self, tlt_obj)

    def test_unshelve_pilot_data(self):
        data = PILOT.unshelve_pilot_data()  # -> tlt_obj_list
        self.assertIsInstance(data, list, 'expect a list w/ or w/o data.')
        self.assertTrue(len(data) == 1, "expect one onlytasklist: PILOT")
        tlt_obj = data[0]  # therefore there is at least one tasklist
        self.assertIsInstance(tlt_obj, dict, "expect tlt is dict.")
        self.assertIsInstance(tlt_obj['tl_rsrc'], dict, "exp: tl_rsrc is a dict resource")
        self.assertIsInstance(tlt_obj['t_list'], list, "exp: a lisst of tasks rsrcs.")
        print_tlt_(self, tlt_obj)


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

    def test_serve_data_(self):
        tlt_obj_list = tlt.serve_data()
        # list of tasklists
        self.assertIsInstance(tlt_obj_list, list, "expect a tlt_obj_list ")
        assert len(tlt_obj_list) > 0  # expect at least PILOTS tasklist.
        print_tlt_list_(self, tlt_obj_list)

        tlt_obj = tlt_obj_list[0]
        self.assertIsInstance(tlt_obj, dict, "expect tlt is dict.")
        self.assertIsInstance(tlt_obj['tl_rsrc'], dict, "exp: tl_rsrc is a dict resource")
        self.assertIsInstance(tlt_obj['t_list'], list, "exp: a list of tasks rsrcs.")
        print_tlt_(self, tlt_obj)

if __name__ == '__main__':
    unittest.main()
