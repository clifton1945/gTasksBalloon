# '$NAME' in 'gTasksBalloon'
#   '3/24/14'/'6:29 PM'
from unittest import TestCase
import task_helpers as h


class TestTaskHelpers(TestCase):
    def setUp(self):
        """
        """
        # noinspection PyPep8Naming,PyPep8Naming
        self.longMessage = True
        do_print = False
        my_name = "ShelvedTltTests.setUp." + self._testMethodName

        # data
        self.tlt_list = tltl = h.unshelve_from_db()
        self.tlt_list_pilots = [tl for tl in tltl
                                if tl['tl_rsrc']['title'] == "PILOTS"]
        self.tlt_rsrc_pilots = self.tlt_list_pilots[0]

    def test_print_tasks_in_t_list_in_(self):
        # noinspection PyPep8Naming,PyPep8Naming
        CUT = h.print_tasks_in_t_list_in_
        _tlt = self.tlt_rsrc_pilots
        CUT(_tlt)
