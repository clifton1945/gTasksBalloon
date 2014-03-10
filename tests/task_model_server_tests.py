# task_model_TESTS.py
#

import unittest
import datetime
import task_model as model
import task_helpers as helper


class TaskModelUpdatingTEST(unittest.TestCase):
    def setUp(self):
        ### actual server data: particularly from tasklist 'TEST
        self.all_rsrcs = model.get_rsrcs_from_server()  # all the tasks in this project
        ### just TRIAL server data.
        self.trial_ttl_rsrcs = ttls = model.get_rsrcs_from_server(helper.FILTER_TRIALS)  # all the tasks in this project
        self.trial_ttl_list = ttll = [ttl for ttl in ttls.itervalues()]
        self.trial_testtask_list = tl = [ttl for ttl in ttll
                                         if 'title' in ttl['task']
                                         and ttl['task']['title'] == 'TestTask']

        ### test datetimes
        self.now_dt = n = datetime.datetime.now()
        self.now_str = n.strftime('%Y-%m-%dT%H:%M:%S.%f')

    @unittest.skip("dirty tasks test needed but not now.")
    def test_update_server_dirty_tasks(self):
        # build dirty, i.e. will be modified, tasks.
        self.assertTrue(False)  # expect some modified tasks.

    def test_update_server(self):
        cut = model.update_server
        # """ calls api get, update ttls, update server, shelve ttl -> ttl_rsrcs: dict.
        #
        # @rtype ttl_rsrcs_dict: dict
        # @return : ttl_rsrcs_dict: dict of updated tasktasklist resources [ttl_rsrc_dict]

        ttl_rsrcs = self.trial_ttl_rsrcs
        self.assertIsInstance(ttl_rsrcs, dict)          # expect one ttl in this list
        # print('TestTask: status:{} due:{}'.format(tt_status, tt_t_due))
        exp = cut()
        self.assertIsInstance(exp, dict)        # expect modified ttl_rsrcs dict

    def test_update_server_from_update_from_ttls(self):
        """ toggle a modification.
        """
        cut = model.update_server_from_
            # update server for each task_rsrc in a list.

            # @type modfd_ttl_list: list
            # @param modfd_ttl_list:
            # @return : server returned ttl_rsrcs_dict

        # first see if modified
        print "{} trial_ttl_rsrcs".format(len(self.trial_ttl_rsrcs))
        t_ttl_rsrcs_list = model.update_ttls_from_(self.trial_ttl_rsrcs)
        print "{} modified t_ttl_rsrcs_list:".format(len(t_ttl_rsrcs_list))
        for itm in t_ttl_rsrcs_list:
            t = itm['task']
            print "  title:{} s:{}, due:{}." \
                .format(t['title'], t['status'], t['due'])
            # print "  title:{} is modified[{}] s:{}, due:{}." \
            #     .format(t['title'], t['modified'], t['status'], t['due'])

        ttl_rsrcs_dict = cut(t_ttl_rsrcs_list)

        print "{} modified ttl_rsrcs_dict: ".format(len(ttl_rsrcs_dict))
        for ttl in ttl_rsrcs_dict.itervalues():
            t = ttl['task']
            if len(t) > 0:
                print "  title:{}  s:{}, due:{}." \
                    .format(t['title'], t['status'],   t['due'])
            else:
                print "ttl['task'] is empty."

        self.assertIsInstance(ttl_rsrcs_dict, dict)


if __name__ == '__main__':
    model.update_server()  # FILL Shelve with current state of ALL TASKS.
    model.get_and_shelve_all_ttls()  # this is used for testing.



