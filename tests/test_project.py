import test_presenter

__author__ = 'CLIF'

import unittest
import test_server
import test_tlt_objects
import test_rules


class ProjectTests(unittest.TestCase):
    def test_something(self):
        self.assertEqual(True, True)

loader = unittest.TestLoader()

suite = loader.loadTestsFromModule(test_server)
suite.addTests(loader.loadTestsFromModule(test_rules))
suite.addTests(loader.loadTestsFromModule(test_tlt_objects))
suite.addTests(loader.loadTestsFromModule(test_presenter))

runner = unittest.TextTestRunner(verbosity=1)
result = runner.run(suite)

if __name__ == '__main__':
    unittest.main()