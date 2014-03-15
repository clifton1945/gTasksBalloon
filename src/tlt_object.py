# 'tlt_object.py' in 'gTasksBalloon'
#   version 4.6.1 GIW  using a dict tlt_obj: {tasklist rsrc, list of task rsrcs}
#   '3/15/14'
#
# Model:
#   logic and rules operations for updating tasks.
#       operations are now a function of the tasklist.
#   interface to Data. Any data use goes thru Model.
# Style is Functional -
#   google Tasks data size is fairly small for now.
#   will loop more than once for simplicity.
#   The time bottleneck is trips to and from server;
#      any redundant looping wil lbe trivial part of performance


from datetime import datetime
# import _bsddb
import task_helpers as h
import server

### GLOBAL
GBL_SERVICE = server.get_service()  # REFACT just use h.functions


 #### MAIN PREDICATES ###
def update_shelve():
    tlt_obj_list = serve_data()
    ret = h.shelve_to_db(tlt_obj_list)  # REFACT doc in h.shelve data names
    assert isinstance(ret, list)
    return ret


def serve_data():
    """
    gets, returns tasklist='PILOTS' tlt_objects
    tlt_objects are now  dictionary
    {tl_rsrc: tasklist rsrc,
      t_list: list of tasks rsrcs
    )
    @return: list of 'PILOTS' tlt_objects: dict
    @rtype: list
    """
    # l0cals
    tlt_obj_list = []
    tlt_obj = {"tl_rsrc": None, "t_list": None}
    try:
        tls_list_response = GBL_SERVICE.tasklists().list().execute()  # predicate
        if 'items' in tls_list_response:
            for task_list_rsrc in tls_list_response['items']:
                tasks_list_response = GBL_SERVICE.tasks().list(tasklist=task_list_rsrc['id']).execute()  # predicate
                if 'items' in tasks_list_response:
                    tlt_obj["tl_rsrc"] = task_list_rsrc
                    tlt_obj["t_list"] = tasks_list_response['items']
                    tlt_obj_list.append(tlt_obj)
    except Exception as ex:
        template = "An exception of type {0} occured. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print "in [serve_pilot_data] ->" + message

    return tlt_obj_list


def set_due_list(tlt_data_list):  # TODO LEARNING GIW AS list comprehension.
    tltdl = tlt_data_list
    mod_list = [x for l in tltdl
                for tl in l
                for x in tl
                if isinstance(x, list)]
    return mod_list


def update_server_():
    # STUB
    return []


 #### MAIN PREDICATE FUNCTIONS


def update_data_(tlt_data_list, tst_now=None):
    """
     modifies each tlt with update_rules which are a function of (tasklist_ type).
     returns a list of just the modified tlts.
    """
    tst_now = datetime.now() if not tst_now else tst_now  # added for testing
    # ADD rules for TRIALS, IDEAS, GOALS, etc.
    modified_tasks_list = []
    modified_tlt_data_list = []
    for tlt_tup in tlt_data_list:
        tl_dict, t_list = tlt_tup  # unpack tlt_tup tuple
        # triage tasklist types for different update rules.
        is_modified = False
        for t in t_list:
            t, is_modified = Rules.apply_rule_near_due(t, tst_now)
            if is_modified:  # add this task_rsrc to list of tasks
                modified_tasks_list.append(t)
        tlt_tup = tl_dict, modified_tasks_list  # re build the tlt tuple
        if is_modified:  # append it to modified_tlt_data_list
            modified_tlt_data_list.append(tlt_tup)
    return modified_tlt_data_list


# noinspection PyClassHasNoInit
class Rules():
    @staticmethod
    def update_tls_from_(tl_rsrc_dict):
        # update each tasklist in it's own scope.
        #i.e. just the tasks in that tasklist.
        # tl_r_d could be empty.
        if tl_rsrc_dict:
            return tl_rsrc_dict

        # locals
        tl_xt = tl_rsrc_dict.copy()
        tl = tl_xt['tasklist']

        # PREDICATE: triage tasks for updating
        if tl['title'] == h.FILTER_FACETS:
            tl_xt = tl_rsrc_dict.apply_rule_near_due(tl_xt)
            # tl_xt = update_tl_facets(tl_xt)
        else:  # update all the rest of the tasklists.
            tl_xt = tl_rsrc_dict.apply_rule_near_due(tl_xt)
        return tl_xt

    @staticmethod
    def apply_rule_near_due(task_rsrc, tst_now=None):
        """
        applies the rule;
        sets 'modified' bool;
        May or may not modify task_rsrc 'status' and 'completed'.
        @type task_rsrc: dict
        @param task_rsrc: i.e. task_rsrc
        @param tst_now: datetime - defaults to actual now() if no test now_date passed in.
        @type tst_now: datetime

        @return (
            "task_rsrc": dict,
            "is_modified": bool
            ): tuple
        """
        t = task_rsrc
        is_modified = False  # default - so there is always a modified attr.
        if 'due' in t:  # now add new ke: modified
            due_dt = h.dt_from_(t['due'])
            tst_now = datetime.now() if not tst_now else tst_now  # added for testing
            is_completed = t['status'] == 'completed'

            # MAIN PREDICATE

            if Rules.near_due_rule(due_dt, tst_now):
                if is_completed:  #
                    is_modified = True
                    t['status'] = 'needsAction'
                    t.pop('completed')
            else:  # not near enough, assure status is completed
                if not is_completed:
                    is_modified = True
                    t['status'] = 'completed'
        return task_rsrc, is_modified

    @staticmethod
    def near_due_rule(due, now):
        """now dt is near enough to due dt.
        sets default before and after days to be near.
        @type due: datetime
        @param due:
        @type now: datetime
        @param now:
        @rtype ret: bool
        @return: bool: True if near enough to due date.
        """
        before_near = 2
        after_near = -2
        # print "due: ", due,  type(due)
        # print "now: ", now,  type(now)
        tdel = due - now  # days to go IS POSITIVE
        return after_near <= tdel.days <= before_near


class Pilot():

    DB_FILE_NAME = 'myPilotDB'
    DB_ROOT_NAME = 'MyPilotRoot'
    FILTER_TRIALS = 'PILOTS'
    FILTER_FACETS = 'FACETS'

    def __init__(self):
        pass

    @staticmethod
    def serve_pilot_data():
        """
        gets, returns tasklist='PILOTS' tlt_objects
        tlt_objects are now  dictionary
        {tl_rsrc: tasklist rsrc,
          t_list: list of tasks rsrcs
        )
        @return: list of 'PILOTS' tlt_objects: dict
        @rtype: list
        """
        pilot_id = "MTEzMzE3MDg1MTgzNjAxMjA2MzM6MTA4MzM1MTE1ODow"
        # l0cals
        tlt_obj_list = []
        tlt_obj = {"tl_rsrc": None, "t_list": None}
        try:
            tl_rsrc = GBL_SERVICE.tasklists().get(tasklist=pilot_id).execute()
            task_list_rsrc = GBL_SERVICE.tasks().list(tasklist=pilot_id).execute()  # predicate
            if 'items' in task_list_rsrc:
                tlt_obj["tl_rsrc"] = tl_rsrc
                tlt_obj["t_list"] = task_list_rsrc['items']
                tlt_obj_list.append(tlt_obj)

        except Exception as ex:
            template = "An exception of type {0} occured. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print "in [serve_pilot_data] ->" + message

        return tlt_obj_list

    @staticmethod
    def update_pilot_shelve():
        tlt_obj_list = Pilot.serve_pilot_data()
        Pilot.shelve_pilot_data(tlt_obj_list)
        return tlt_obj_list

    @staticmethod
    def shelve_pilot_data(tlt_obj_list):
        """
        unshelves data, and
        @return:  a list with just tasklist 'PILOTS' objects.
        @rtype: list
        """
        ret = h.shelve_to_db(tlt_obj_list, Pilot.DB_FILE_NAME, Pilot.DB_ROOT_NAME)
        assert isinstance(ret, list)

    @staticmethod
    def unshelve_pilot_data():
        """
        unshelves data, and
        @return:  a list with just tasklist 'PILOTS' objects.
        @rtype: list
        """
        ret = h.unshelve_from_db(Pilot.DB_FILE_NAME, Pilot.DB_ROOT_NAME)
        assert isinstance(ret, list)  #
        return ret


if __name__ == '__main__':
    update_shelve()
    # add a some super test or print function here.
