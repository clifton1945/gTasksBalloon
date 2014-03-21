# '$NAME' in 'gTasksBalloon'
#   '3/19/14'/'2:55 PM'
from unittest import TestCase
from datetime import datetime, timedelta
import src.tlt_object as tlt
import src.task_helpers as h

mock_task_rsrc = {
    "kind": "tasks#task",
    "id": "string",
    "etag": "etag",
    "title": "string",
    "updated": "datetime",
    "selfLink": "string",
    "parent": "string",
    "position": "string",
    "notes": "string",
    "status": "string",
    "due": "datetime",
    "completed": "datetime",
    "deleted": "boolean",
    "hidden": "boolean",
    "links": [
        {
            "type": "string",
            "description": "string",
            "link": "string"
        }
    ]
}


def x():
    """
     something in here.
    """
    # dfghjkl;'
    # dfghjkl;
    pass


class TestRules(TestCase):
    def setUp(self):
        # build test tasks both in and out of near_due rule:
        deltas = [-3, -2, 0, 1, 4]
        self.template = '  task.title[{0}] .due[{2}] status=[{1}].'

        def make_mock_task(delta):
            # these are ALL VISIBLE !
            t_rsrc = t = mock_task_rsrc.copy()
            t['title'] = 'mock' + str(delta)
            t['status'] = 'needsAction'
            t.pop('completed')
            t['due'] = h.rfc_from_(datetime.now() + timedelta(delta))
            # print(self.template.format(t['title'], t['status'], t['due']))
            return t_rsrc

        self.mock_tasks_list = [make_mock_task(_due_dt) for _due_dt in deltas]  # NOT tlt list

    def test_apply_rule_near_due(self):
        cut = tlt.Rules.apply_rule_near_due
        # data
        bas_t_list = self.mock_tasks_list
        mock_2 = [t for t in bas_t_list if t['title'] == 'mock-2'][0]
        mock1 = [t for t in bas_t_list if t['title'] == 'mock1'][0]

        print "base list"
        for bas in bas_t_list:
            print(self.template.format(bas['title'], bas['status'], bas['due']))

        #  PREDICATE
        mod_t_list = cut(bas_t_list)

        print "modified list"
        for mod in mod_t_list:
            print(self.template.format(mod['title'], mod['status'], mod['due']))

        # visual compare
        # test specific task
        exp = [t for t in mod_t_list if t['title'] == 'mock-3'][0]['status']
        self.assertEqual(exp, 'completed', "exp: default mock-3 modified to show completed.")
        self.assertNotIn(mock_2, mod_t_list, "exp: mock_2 is included as modified.")



