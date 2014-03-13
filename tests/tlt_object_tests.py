
import unittest
import _bsddb
import src.tlt_object as tlt


 ### GLOBALS
PILOT = tlt.Pilot


class PilotTests(unittest.TestCase):

    def setUp(self):
        # noinspection PyPep8Naming,PyPep8Naming
        self.longMessage
        try:
            self.data = PILOT.unshelve_pilot_data()

        except _bsddb.DBNoSuchFileError:
            print 'in PilotTests.setUp' \
                  'PILOT.unshelve_pilot_data() FAILED;\n' \
                  'called PILOT.serve_pilot_data()'
            data = PILOT.serve_pilot_data()
            PILOT.shelve_pilot_data(data)
            self.data = PILOT.unshelve_pilot_data()

        except Exception as ex:
            template = "An exception of type {0} occured. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print message

    def test_serve_pilot_data(self):
        exp = self.data
        self.assertIsInstance(self.data, list, "expect a tlt_list ")
        if len(exp) > 0:
            exp = exp[0]  # NOTE this test is for tlt -> a list of tuples (tl, list of tasks)
            self.assertIsInstance(exp[0], dict, "tl is tasklist resource ")
            self.assertIsInstance(exp[1], list, "list of tasks")


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
        self.assertIsInstance(exp, list, "expect tlt_list ")
        if len(exp) > 0:
            exp = exp[0]  # NOTE this test is for tlt -> a list of tuples (tl, list of tasks)
            self.assertIsInstance(exp[0], dict, "tl is tasklist resource ")
            self.assertIsInstance(exp[1], list, "list of tasks")


if __name__ == '__main__':
    unittest.main()
