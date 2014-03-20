__author__ = 'CLIF'

import unittest
import datetime

import server


# these maybe out of date.
TESTlist_id = 'MTEzMzE3MDg1MTgzNjAxMjA2MzM6MjA2OTM2NjgzOjA'
TESTTask_id = 'MTEzMzE3MDg1MTgzNjAxMjA2MzM6MjA2OTM2NjgzOjExNTQyNzg2OTU'
TASKSlist_id = 'MTEzMzE3MDg1MTgzNjAxMjA2MzM6MDow'
TestDueDate_id = 'MTEzMzE3MDg1MTgzNjAxMjA2MzM6MjA2OTM2NjgzOjE3MzM4NjIyMjg'


class ServerTests(unittest.TestCase):
    """NOTE: CUT >> CodeUnderTest
    """
    def setUp(self):
        service = server.get_service()
        self.tasklists = service.tasklists()
        self.tasks = service.tasks()
        self.msg = "patched @ " + str(datetime.datetime.now())

    def test_seeing_tasks(self):
        """NOTES:
            affect returned task Resource:
                [show]hidden, [show]deleted, showCompleted <bool>
            can see if 'needsAction'
            can see if 'completed' and Not Clear Completed
            can see if 'completed' and Field: hidden=True
        @return:
        """
        self.assertTrue(True)

    def test_tasks_patch_modifies(self):
        """a patch modifies and returns a task Resource of Fields
        See patch notes in README
        """
        ### first get current test task resource with just these Filedl
        cut_get = self.tasks.get(tasklist=TESTlist_id, task=TESTTask_id,
                                 fields="status, completed, hidden, notes").execute()
        ### now modify the task
        cut_get['notes'] = self.msg
        cut_get['status'] = "needsAction"
        cut_get['completed'] = None
        ### now patch it to server.
        cut_patch = self.tasks.patch(tasklist=TESTlist_id, task=TESTTask_id, body=cut_get,
                                     fields="status, completed, hidden").execute()
        ### look at it
        self.assertIsInstance(cut_patch, dict)  # expect a returned dict
        self.assertNotIn('hidden', cut_get)     # NOT expected BECAUSE the task is NOT 'hidden'
        self.assertIn('completed', cut_get)     # expected BECAUSE key is there, we asked for it but it's set to None
        self.assertIn('status', cut_patch)      # expect a status property
        self.assertEqual(cut_patch['status'], "needsAction")

    def test_task_patch_does_not_modify_task(self):
        """patch doesn't have the modified field.
        """
        ### first establish test task properties
        cut_get = self.tasks.get(tasklist=TESTlist_id, task=TESTTask_id,
                                 fields="status").execute()
        ### now modify the task notes field
        cut_get['notes'] = self.msg
        cut_patch = self.tasks.patch(tasklist=TESTlist_id, task=TESTTask_id, body=cut_get,
                                     fields="status").execute()
        self.assertIsInstance(cut_patch, dict)  # expect a returned dict with just one key: status
        self.assertIn('status', cut_patch)      # expect status BECAUSE cut_get did asked for it.
        self.assertNotIn('notes', cut_patch)    # expect BECAUSE cut_get did NOT ask for notes field

    def test_tasks_get(self):
        """NOTE: CUT >> CodeUnderTest
         using patch formating. See notes in README
        @return:
        """
        t = self.tasks
        # first establish test task properties
        cut_get = t.get(tasklist=TESTlist_id, task=TESTTask_id, fields="title, status, notes").execute()
        self.assertIsInstance(cut_get, dict)
        self.assertIn('title', cut_get)  # expect title as dict key.
        self.assertIn('notes', cut_get)  # expect notes as dict key.
        self.assertIn('status', cut_get)  # expect status as dict key.
        self.assertNotIn('hidden', cut_get)  # don't expect hidden as dict key.
        self.assertNotIn('kind', cut_get)  # don't even expect default kind as dict key.

#
# def server_class_suites():
#     suite = unittest.BaseTestSuite()
#     suite.addTest(ServerTests())
#     return suite
#
# if __name__ == '__main__':
#     runner = unittest.TextTestRunner()
#     test_suite = server_class_suites()
#     runner.run(test_suite)
