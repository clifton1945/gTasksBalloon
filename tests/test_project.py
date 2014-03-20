import presenter_TESTS

__author__ = 'CLIF'

import unittest
import test_server
import tlt_object_tests


class ProjectTests(unittest.TestCase):
    def test_something(self):
        self.assertEqual(True, True)

loader = unittest.TestLoader()

suite = loader.loadTestsFromModule(test_server)
suite.addTests(loader.loadTestsFromModule(tlt_object_tests))
suite.addTests(loader.loadTestsFromModule(presenter_TESTS))

runner = unittest.TextTestRunner(verbosity=1)
result = runner.run(suite)

if __name__ == '__main__':
    unittest.main()