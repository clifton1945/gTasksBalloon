import unittest
from datetime import datetime, timedelta
import _bsddb
import src.tlt_object as tlt
import src.task_helpers as h


### GLOBALS
PILOT = tlt.Pilot


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
        self.assertIsInstance(tlt['tl_rsrc'], dict, "exp: tl_rsrc is a dict resource")
        self.assertIsInstance(tlt['t_list'], list, "exp: a lisst of tasks rsrcs.")
        print "serve_pilot_data ->\n  " \
              "tasklist title:{} has {} task rsrcs.". \
            format(tlt['tl_rsrc']['title'], len(tlt['tl_rsrc']['t_list']))

    def test_update_pilot_shelve(self):
        tlt_obj_list = PILOT.update_pilot_shelve()
        self.assertIsInstance(tlt_obj_list, list, "expect a tlt_obj_list ")

    def test_unshelve_pilot_data(self):
        data = PILOT.unshelve_pilot_data()  # -> tlt_obj_list
        self.assertIsInstance(data, list, 'expect a list w/ or w/o data.')
        self.assertTrue(len(data) == 1, "expect one onlytasklist: PILOT")
        tl_rsrc, lotasks = data[0]  # therefore there is at least one tasklist
        self.assertIsInstance(tl_rsrc, dict, "expect a tl resource dict")
        self.assertIsInstance(lotasks, list, "expect a list of tasks list")
        print "unshelve_pilot_data ->.\n  " \
              "tasklist title:{} has {} task rsrcs.". \
            format(tl_rsrc['title'], len(lotasks))

    def test_tup2dict(self):
        """
        tlt_list  [tlt, .....]: list
        tlt_obj -> (
            tl_rsrc: dict,
            list_of_tasks: list
            ):  tuple
        @return: tlt_dict
        @rtype: dict
        """
        cut = tlt.tup2dict

        data = PILOT.unshelve_pilot_data()
        self.assertIsInstance(data, list, 'expect data is a list w/ or w/o data.')
        ret = [cut(lst) for lst in data]
        self.assertIsInstance(ret, list, 'expect return is a list w/ or w/o data.')
        print ret

    def test_update_data_(self):
        cut = tlt.update_data_  # -> tlt_obj_list
        # REFACT lousy test - cut must work to test it working!.
        # confirm there is some test data.
        tlt_obj_list = data = PILOT.unshelve_pilot_data()
        self.assertIsInstance(data, list, 'expect a list w/ or w/o data.')
        self.assertTrue(len(data) == 1, "expect one onlytasklist: PILOT")
        tl_rsrc, lotasks = data[0]  # therefore there is at least one tasklist
        self.assertIsInstance(tl_rsrc, dict, "expect a tl resource dict")
        self.assertIsInstance(lotasks, list, "expect a list of tasks list")

        # apply cut -> modified data as a reference
        mdata = cut(data)
        self.assertIsInstance(mdata, list, 'expect a list w/ or w/o data.')
        ref_len = len(mdata)

        # now add a mock task to mod data reference: it will be modified.
        mock_tlt = (tl_rsrc, [self.mock_task_hide])
        mdata.append(mock_tlt)

        # now cut
        new_tlt_mdata = cut(mdata, self.mock_now)
        self.assertIsInstance(new_tlt_mdata, list, 'expect a list w/ data.')
        self.assertTrue(len(new_tlt_mdata) == 1, "expect one only tasklist: PILOT")
        tl_rsrc, lotasks = new_tlt_mdata[0]  # therefore there is at least one tasklist
        self.assertIsInstance(tl_rsrc, dict, "expect a tl resource dict")
        self.assertIsInstance(lotasks, list, "expect a list of tasks list")
        pass



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
