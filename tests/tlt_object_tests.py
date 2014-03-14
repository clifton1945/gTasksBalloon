import unittest
from datetime import datetime
import _bsddb
import src.tlt_object as tlt
from src.task_helpers import dt_from_, rfc_from_


### GLOBALS
PILOT = tlt.Pilot


class PilotTests(unittest.TestCase):
    def setUp(self):
        """
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
        self.longMessage
        self.mock_task_hide = {
            "title": "mock_needsAction",
            "status": "needsAction",
            "due": "2014-03-14T12:00:10.000Z",
            "notes": "a mock task."
        }
        self.mock_now = datetime(2014, 03, 11, 12, 00)

    def test_serve_pilot_data(self):
        tlt_obj_list = PILOT.serve_pilot_data()
        self.assertIsInstance(tlt_obj_list, list, "expect a tlt_obj_list ")
        assert len(tlt_obj_list) == 1  # expect just PILOTS tasklist rsrc.
        tl_rsrc, task_list = tlt_obj_list[0]
        self.assertIsInstance(tl_rsrc, dict, "tl is tasklist resource ")
        self.assertIsInstance(task_list, list, "list of tasks")
        print "serve_pilot_data ->\n  " \
              "tasklist title:{} has {} task rsrcs.". \
            format(tl_rsrc['title'], len(task_list))

    def test_update_pilot_shelve(self):
        tlt_obj_list = PILOT.update_pilot_shelve()
        self.assertIsInstance(tlt_obj_list, list, "expect a tlt_obj_list ")

    def test_unshelve_pilot_data(self):
        tlt_obj_list = data = PILOT.unshelve_pilot_data()
        self.assertIsInstance(data, list, 'expect a list w/ or w/o data.')
        self.assertTrue(len(data) == 1, "expect one onlytasklist: PILOT")
        tl_rsrc, lotasks = data[0]  # therefore there is at least one tasklist
        self.assertIsInstance(tl_rsrc, dict, "expect a tl resource dict")
        self.assertIsInstance(lotasks, list, "expect a list of tasks list")
        print "unshelve_pilot_data ->.\n  " \
              "tasklist title:{} has {} task rsrcs.". \
            format(tl_rsrc['title'], len(lotasks))

    def test_update_data_(self):
        cut = tlt.update_data_
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
