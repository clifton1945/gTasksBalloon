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


class TestRules(TestCase):
    def setUp(self):
        # build test tasks both in and out of near_due rule:
        deltas = [-3, -2, 0, 1, 4]
        self.template = '  task.title[{0}] .due[{2}] status=[{1}].'

        def make_mock_task(delta):
            t_rsrc = t = mock_task_rsrc.copy()
            t['title'] = 'mock' + str(delta)
            t['status'] = 'completed'
            t['due'] = h.rfc_from_(datetime.now() + timedelta(delta))
            # print(self.template.format(t['title'], t['status'], t['due']))
            return t_rsrc

        self.mock_tasks_list = [make_mock_task(_due_dt) for _due_dt in deltas]  # NOT tlt list

    def test_updating_data_(self):
        # data
        bas_t_list = self.mock_tasks_list
        for bas in bas_t_list:
            print "base list"
            print(self.template.format(bas['title'], bas['status'], bas['due']))

        # cut = tlt.Rules.apply_rule_near_due
        # cut = tlt.Rules.near_due_rule
        mod_t_list = [tlt.Rules.apply_rule_near_due(t) for t in bas_t_list
                      if tlt.Rules.near_due_rule(t)]  # modified_t_rsrcs_list
        for mod in mod_t_list:
            print "modified list"
            print(self.template.format(mod['title'], mod['status'], mod['due']))

        # visual compare
        compare_list = [(base, mod) for base, mod in zip(bas_t_list, mod_t_list)]
        for b, m in compare_list:
            print(self.template.format(b['title'], b['status'], b['due']))
            print(self.template.format(m['title'], m['status'], m['due']))

        pass


