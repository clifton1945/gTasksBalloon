import unittest
from datetime import datetime
import src.tlt_object as model
import src.task_helpers as h


tlt_list = model.update_shelve(False)
print '************* UPDATED SHELVE *********'


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

    #@unittest.skip("skip: test_update_data_()  till base is stable.")
    def test_update_data_(self):
        """
        update_data in the main PREDICATE of th project. Each tlt_object is subjected to a series of Rules.
        If the rule dictates the object is modifed, and returned to a modified_tlt_objs list.

        """
        # noinspection PyPep8Naming
        CUT = model.update_data_
        # locals
        do_print = False
        msg = self._testMethodName + ".ALL lists"

        # data = self.tlt_list  # data as received from server
        data = self.tlt_list  # data as received from server

        h.print_summary_ttl_list_(data, self._testMethodName + ".BASE")

        mod = model.update_data_(data)    # MAIN PREDICATE
        exp = CUT(mod)

        # as modified
        self.assertTrue(h.is_valid_tlt_list_(exp, do_print, msg), "modified still valid list.")

        h.print_summary_ttl_list_(exp, self._testMethodName + ".MODIFIED.")


class ServerTltTests(unittest.TestCase):
    def setUp(self):
        """
        invokes tests using real, current server/shelve data invoked IN the test.
        by calling update_shelve() get current server responces shelved.
        NOTE: shelving may add time to date return.
        """
        # noinspection PyPep8Naming,PyPep8Naming
        self.longMessage = True
        do_print = False
        my_name = "ServerTltTests.setUp." + self._testMethodName

    #@unittest.skip("SKIP: unless shelve data is corrupt.")
    def test_serve_data_is_valid_tlt_list_(self):
        do_print = False
        my_name = self._testMethodName
        # noinspection PyPep8Naming
        CUT = model.serve_data()
        # list of tasklists
        self.assertTrue(h.is_valid_tlt_list_(CUT, do_print, my_name))

    def test_update_shelve_seem_to_be_same(self):
        do_print = False
        my_name = self._testMethodName
        # noinspection PyPep8Naming
        CUT = model.update_shelve  # which calls serve_data() first.

        shelved_tlt_list = CUT()
        unshelved_tlt_list = h.unshelve_from_db()
        self.assertDictEqual(unshelved_tlt_list[0], shelved_tlt_list[0],
                             "exp unshelved[0] and shelved[0] are same")
        l = len(shelved_tlt_list) - 1
        self.assertDictEqual(unshelved_tlt_list[l], shelved_tlt_list[l],
                             "exp unshelved[l] and shelved[l] are same")

    # noinspection PyPep8Naming
    def test_update_data_PILOTS(self):
        """
        updates SERVER.PILOTS Tasklist ONLY -
        """
        CUT = model.update_data_
        # locals
        do_print = False
        msg = self._testMethodName + ".PILOTS list."
        # data as received
        data = h.unshelve_from_db()
        data = [d for d in data
                if d['tl_rsrc']['title'] == 'PILOTS']
        a_tlt_obj = data[0] if data else None

        h.print_summary_ttl_list_(data, self._testMethodName + ".BASE")
        h.print_t_objs_in_t_list_in_(a_tlt_obj, msg)  # NOTE: ONE tlt+obj

        data = CUT(data)  # PREDICATE
        a_tlt_obj = data[0] if data else None

        h.print_summary_ttl_list_(data, self._testMethodName + ".MODIFIED.")
        h.print_t_objs_in_t_list_in_(a_tlt_obj, msg)  # NOTE: ONE tlt+obj

    # noinspection PyPep8Naming
    def test_update_server_PILOTS(self):
        """
        updates SERVER.PILOTS Tasklist ONLY -
        """
        CUT = model.update_server
        # locals
        # do_print = True
        msg = self._testMethodName + ".PILOTS list."
        # data as received
        data = h.unshelve_from_db()
        data = [d for d in data
                if d['tl_rsrc']['title'] == 'PILOTS']
        a_tlt_obj = tlt = data[0] if data else None

        # FORCE WRONG STATUS
        t = [t for t in tlt['t_list'] if t['title'] == 'expect needsAction'].pop()
        t['due'] == h.rfc_from_(datetime.now())
        t['status'] = 'completed'

        t = [t for t in tlt['t_list'] if t['title'] == 'expect completed'].pop()
        t['due'] == h.rfc_from_(datetime(2000, 3, 2, 1))
        t['status'] = 'needsAction'

        h.print_summary_ttl_list_(data, self._testMethodName + ".BASE")
        h.print_t_objs_in_t_list_in_(a_tlt_obj, msg)  # NOTE: ONE tlt+obj

        # FIRST modifiy the data if needed
        mod = model.update_data_(data)
        # NOW update_server()
        data = CUT(mod)
        a_tlt_obj = data[0] if data else None

        h.print_summary_ttl_list_(data, self._testMethodName + ".MODIFIED")
        h.print_t_objs_in_t_list_in_(a_tlt_obj, msg)  # NOTE: ONE tlt+obj

    unittest.skip("SKIP: until sure update_data and update_server ARE WORKING RIGHT!")
    def test_update_server(self):
        """
        updates SERVER after first updating_data() ALL DATA
        """
        # noinspection PyPep8Naming
        CUT = model.update_server
        # locals
        do_print = False
        msg = self._testMethodName + ".ALL lists"

        data = model.update_shelve() # data as received from server and shelved.
        a_tlt_obj = data[0] if data else None
        h.print_summary_ttl_list_(data, self._testMethodName + ".BASE")
        h.print_t_objs_in_t_list_in_(a_tlt_obj, msg)  # NOTE: ONE tlt+obj

        # FIRST modifiy the data if needed
        mod = model.update_data_(data)
        # NOW update_server()
        data = CUT(mod)
        a_tlt_obj = data[0] if data else None
        h.print_summary_ttl_list_(data, self._testMethodName + ".MODIFIED")
        h.print_t_objs_in_t_list_in_(a_tlt_obj, msg)  # NOTE: ONE tlt+obj


if __name__ == '__main__':
    unittest.main()