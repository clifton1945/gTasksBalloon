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
        h.print_t_list_(data[0]["t_list"], self._testMethodName + ".base")

        # as received
        exp = cut(data)
        self.assertTrue(h.is_valid_tlt_list_(exp, do_print, msg), "modified still valis list.")

        h.print_t_list_(exp[0]['t_list'], self._testMethodName + ".updated.")
        pass  # has anything changed??


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

        # SERVER DATA ---
        self.tlt_obj_list = tlt_obj_list = tlt.serve_data()
        h.is_valid_tlt_list_(tlt_obj_list, do_print, my_name)
        # TEST DATA --- filter data to just run test on non essential stuff
        self.tlt_test_list = [tlt_obj for tlt_obj in tlt_obj_list
                              if tlt_obj["tl_rsrc"]['title'] == "PILOTS"]

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
        self.assertTrue(h.is_valid_tlt_list_(tlt_obj_list, do_print, my_name), "exp valid list of tlt objects.")

    def test_update_server_PILOTS(self):
        """
        updates SERVER after first updating_test data - in this case PILOTS -
        """
        cut = tlt.update_server
        # locals
        do_print = False
        msg = self._testMethodName + ".PILOTS list."
        # data as received
        data = self.tlt_test_list  # just PILOTS list for now
        h.print_summary_ttl_list_(data, self._testMethodName + ".BASE")

        mod = tlt.update_data_(data)    # TEST DATA
        exp = cut(mod)

        # as modified
        self.assertTrue(h.is_valid_tlt_list_(exp, do_print, msg), "modified still valid list.")

        h.print_summary_ttl_list_(exp, self._testMethodName + ".MODIFIED.")

    def test_update_server(self):
        """
        updates SERVER after first updating_data() ALL DATA
        """
        cut = tlt.update_server
        # locals
        do_print = False
        msg = self._testMethodName + ".ALL lists"

        data = self.tlt_obj_list  # data as received from server
        tlt.update_shelve()
        # shelve in case
        h.print_summary_ttl_list_(data, self._testMethodName + ".BASE")

        mod = tlt.update_data_(data)    # TEST DATA
        exp = cut(mod)

        # as modified
        self.assertTrue(h.is_valid_tlt_list_(exp, do_print, msg), "modified still valid list.")

        h.print_summary_ttl_list_(exp, self._testMethodName + ".MODIFIED.")


if __name__ == '__main__':
    tlt_list = tlt.update_shelve(True)
    print '************* UPDATED SHELVE *********'

    unittest.main()