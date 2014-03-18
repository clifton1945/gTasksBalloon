import presenter_TESTS

__author__ = 'CLIF'

import unittest
import server_TESTS
# import task_model_TESTS
import task_model_server_tests


class ProjectTests(unittest.TestCase):
    def test_something(self):
        self.assertEqual(True, True)

loader = unittest.TestLoader()

suite = loader.loadTestsFromModule(server_TESTS)
# suite.addTests(loader.loadTestsFromModule(task_model_TESTS))
suite.addTests(loader.loadTestsFromModule(presenter_TESTS))
suite.addTests(loader.loadTestsFromModule(task_model_server_tests))

runner = unittest.TextTestRunner(verbosity=1)
result = runner.run(suite)

if __name__ == '__main__':
    unittest.main()