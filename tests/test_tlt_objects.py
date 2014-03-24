import unittest
# from datetime import datetime
import src.tlt_object as tlt
import src.task_helpers as h


### GLOBALS
# import tlt_object


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
        _tlt_list = h.unshelve_from_db()
        # elaborate way to get ->
        tlt_obj = {}
        assert h.is_valid_tlt_list_(_tlt_list, do_print, my_name)
        self._tlt_list = _tlt_list
        l = len(_tlt_list)
        if l > 0:
            assert h.is_valid_tlt_(_tlt_list[0], do_print, my_name)
            tlt_obj = _tlt_list[0]
        if l > 1:
            assert _tlt_list[1] != tlt_obj

        # THIS
        self.tlt_list = _tlt_list
        self.tlt_obj = tlt_obj

    def test_data_valid(self):
        """
        checks tlt_list and tlt obj are valid
        AND
        confirms tlt_rsrc 0 != tlt_rsrc 1
        """
        # locals
        do_print = False
        msg = self._testMethodName

        _tlt_list = self.tlt_list

        # list of tasklists
        h.is_valid_tlt_list_(_tlt_list, do_print, msg)

    #@unittest.skip("skip: test_update_data_()  till base is stable.")
    def test_update_data_(self):
        """
        update_data in the main PREDICATE of th project. Each tlt_object is subjected to a series of Rules.
        If the rule dictates the object is modifed, and returned to a modified_tlt_objs list.

        """
        # noinspection PyPep8Naming
        CUT = tlt.update_data_
        # locals
        do_print = False
        msg = self._testMethodName + ".ALL lists"

        # data = self.tlt_list  # data as received from server
        data = self.tlt_list  # data as received from server

        h.print_summary_ttl_list_(data, self._testMethodName + ".BASE")

        mod = tlt.update_data_(data)    # MAIN PREDICATE
        exp = CUT(mod)

        # as modified
        self.assertTrue(h.is_valid_tlt_list_(exp, do_print, msg), "modified still valid list.")

        h.print_summary_ttl_list_(exp, self._testMethodName + ".MODIFIED.")


class ServerTltTests(unittest.TestCase):
    def setUp(self):
        """
        invokes tests using real, current server +data.
        by calling update_shelve() which hs called server_data().
        
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

        # CURRENT SERVER & SHELVE DATA ---
        self.tlt_list = _tlt_list = tlt.update_shelve()
        h.is_valid_tlt_list_(_tlt_list, do_print, my_name)
        
        # TEST DATA --- filter data to just run test on non essential stuff
        self.tlt_test_list = [tlt_obj for tlt_obj in _tlt_list
                              if tlt_obj["tl_rsrc"]['title'] == "PILOTS"]

    @unittest.skip("SKIP: unless shelve data is corrupt.")
    def test_serve_data(self):
        do_print = False
        my_name = self._testMethodName
        # noinspection PyPep8Naming
        CUT = tlt.serve_data

        _tlt_list = CUT()

        # list of tasklists
        self.assertTrue(h.is_valid_tlt_list_(_tlt_list, do_print, my_name))

    def test_update_shelve(self):
        do_print = False
        my_name = self._testMethodName
        # noinspection PyPep8Naming
        CUT = tlt.update_shelve

        _tlt_list = CUT()

        # list of tasklists
        self.assertTrue(h.is_valid_tlt_list_(_tlt_list, do_print, my_name), "exp valid list of tlt objects.")

    # noinspection PyPep8Naming
    def test_update_server_PILOTS(self):
        """
        updates SERVER after first updating_test data - in this case PILOTS -
        """
        CUT = tlt.update_server
        # locals
        do_print = True
        msg = self._testMethodName + ".PILOTS list."
        # data as received
        data = self.tlt_test_list  # just PILOTS list for now
        h.print_summary_ttl_list_(data, self._testMethodName + ".BASE")

        mod = tlt.update_data_(data)    # TEST DATA
        exp = CUT(mod)

        # as modified
        self.assertTrue(h.is_valid_tlt_list_(exp, do_print, msg), "modified still valid list.")

        h.print_summary_ttl_list_(exp, self._testMethodName + ".MODIFIED.")

    def test_update_server(self):
        """
        updates SERVER after first updating_data() ALL DATA
        """
        # noinspection PyPep8Naming
        CUT = tlt.update_server
        # locals
        do_print = False
        msg = self._testMethodName + ".ALL lists"

        # data = self.tlt_list  # data as received from server
        data = self.tlt_list  # data as received from server

        tlt.update_shelve()
        # shelve in case
        h.print_summary_ttl_list_(data, self._testMethodName + ".BASE")

        mod = tlt.update_data_(data)    # TEST DATA
        exp = CUT(mod)

        # as modified
        self.assertTrue(h.is_valid_tlt_list_(exp, do_print, msg), "modified still valid list.")

        h.print_summary_ttl_list_(exp, self._testMethodName + ".MODIFIED.")


if __name__ == '__main__':
    tlt_list = tlt.update_shelve(True)
    print '************* UPDATED SHELVE *********'

    unittest.main()