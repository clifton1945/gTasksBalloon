# 'tlt_object.py' in 'gTasksBalloon'
#   version 4.7.0 GIW  using a dict tlt_obj: {tasklist rsrc, list of task rsrcs}
#   '3/17/14'
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
GBL_SERVICE = server.get_service()  # REFACT just use h.functions OR from server as s


 #### MAIN PREDICATES ###
def serve_data():
    """
    creates and returns a tlt {
        tasklist rsrc: dict'
         tasks_list: list
         }: dict

    tls_list_response ->
    {
      "kind": "tasks#taskLists",
      "etag": string,
      "nextPageToken": string,
      "items": [
        tasklists Resource
      ]
    }
    tasks_list_response ->
    {
      "kind": "tasks#tasks",
      "etag": string,
      "nextPageToken": string,
      "items": [
        tasks Resource
      ]
    }

    @return: list of tlt_objects: dict
    @rtype: list
    """
    # l0cals
    do_print = False
    name = "f: serve_data"
    tlt_obj_list = []
    try:
        tls_list_response = GBL_SERVICE.tasklists().list().execute()  # predicate
        # tlt_obj = {"tl_rsrc": None, "t_list": None}
        if 'items' in tls_list_response:  # each tasklist
            for a_tasklist_rsrc in tls_list_response['items']:
                tasks_list_response = GBL_SERVICE.tasks().list(tasklist=a_tasklist_rsrc['id']).execute()  # predicate
                if 'items' in tasks_list_response:
                    # build a new tlt obj.
                    tlt_obj = dict()
                    tlt_obj["t_list"] = tasks_list_response['items']
                    tlt_obj["tl_rsrc"] = a_tasklist_rsrc
                    tlt_obj_list.append(tlt_obj)
                    # building list of tlt objects.
                # else no tasks in this tasklist: try another tasklist.
        # else there are no tasklists: return empty list
    except Exception as ex:
        template = "An exception of type {0} occured. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print "in [serve_pilot_data] ->" + message

    valid = h.is_valid_tlt_list_(tlt_obj_list, do_print, name)

    return tlt_obj_list


def update_shelve():
    """
    selves server data -> list of tlt objects..
    """
    do_print = True
    my_name = "update_shelve"

    tlt_obj_list = h.shelve_to_db(serve_data())
    assert h.is_valid_tlt_list_(tlt_obj_list, do_print, my_name)  # expect valis list of tlt objects.
    return tlt_obj_list


def update_data_(tlt_obj_list, tst_now=None):
    """
     modifies each tlt with update_rules which are a function of (tasklist_ type).
     returns a list of just the modified tlts.
    """
    tst_now = datetime.now() if not tst_now else tst_now  # added for testing
    # ADD rules for TRIALS, IDEAS, GOALS, etc.

    modified_tasks_list = []
    modified_tlt_data_list = []

    # TODO NEXT GIW  Rules.apply_rule_near_due(tlt_list, tst_now)  # PREDICATE
    for tlt_dict in tlt_obj_list:
        # triage tasklist types for different update rules.
        is_modified = False
        for t in tlt_dict['t_list']:

            t, is_modified = Rules.apply_rule_near_due(t, tst_now)  # PREDICATE

            if is_modified:  # add this task_rsrc to list of tasks
                modified_tasks_list.append(t)
        tlt_dict['t_list'] = modified_tasks_list
        if is_modified:  # append it to modified_tlt_data_list
            modified_tlt_data_list.append(tlt_dict)

    return modified_tlt_data_list


def set_due_list(tlt_obj_list):  # TODO LEARNING GIW AS list comprehension.
    tltdl = tlt_obj_list
    mod_list = [x for l in tltdl
                for tl in l
                for x in tl
                if isinstance(x, list)]
    return mod_list


def filter_modified_tlts(tlt_list):
    """
    return list of tlts the rules modified.
    """

 #### MAIN PREDICATE FUNCTIONS


# noinspection PyClassHasNoInit
class Rules():
    # @staticmethod
    # def sift_by_rule__near_due(task_rsrc, tst_now=None):
    #     """
    #     applies the rule;
    #     sets 'modified' bool;
    #     May or may not modify task_rsrc 'status' and 'completed'.
    #     @type task_rsrc: dict
    #     @param task_rsrc: i.e. task_rsrc
    #     @param tst_now: datetime - defaults to actual now() if no test now_date passed in.
    #     @type tst_now: datetime
    #
    #     @return (
    #         "task_rsrc": dict,
    #         "is_modified": bool
    #         ): tuple
    #     """
    #     if 'due' in task_rsrc:  # now add new ke: modified
    #         due_dt = h.dt_from_(task_rsrc['due'])
    #         tst_now = datetime.now() if not tst_now else tst_now  # added for testing
    #         # MAIN PREDICATE
    #         task_rsrc = Rules.modify_task_rsrc(task_rsrc, tst_now, due_dt)
    #     return task_rsrc

    @staticmethod
    def depr_apply_rule_near_due(task_rsrc, tst_now=None):
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
        is_modified = False  # default - so there is always a modified attr.
        if 'due' in task_rsrc:  # now add new ke: modified
            due_dt = h.dt_from_(task_rsrc['due'])
            tst_now = datetime.now() if not tst_now else tst_now  # added for testing
            is_completed = task_rsrc['status'] == 'completed'

            # MAIN PREDICATE
            is_modified = Rules.modify_task_rsrc(task_rsrc, tst_now, due_dt)

        return task_rsrc, is_modified

    def apply_rule_near_due(tlt_objs_list, tst_now=None):
        """ REFACT THIS
        # applies this rule ;
        # sets 'modified' bool;
        # May or may not modify task_rsrc 'status' and 'completed'.
        # @type task_rsrc: dict
        # @param task_rsrc: i.e. task_rsrc
        # @param tst_now: datetime - defaults to actual now() if no test now_date passed in.
        # @type tst_now: datetime
        #
        # @return (
        #     "task_rsrc": dict,
        #     "is_modified": bool
        #     ): tuple
        """
        #locals
        tlt_lst = tlt_objs_list
        rule = Rules.modify_task_rsrc

        mod_tlt_list = []  # modified_tlt_objs_list
        ret = [rule(tlt) for tlt in tlt_lst]

        return mod_tlt_list

    @staticmethod
    def modify_task_rsrc(task_rsrc, tst_now=None, due_dt=None):
        """
        modifies task rsrc w/ near_due_rule()
        """
        is_completed = True if task_rsrc['status'] == 'completed' else False
        if Rules.near_due_rule(due_dt, tst_now):
            if is_completed:  #
                is_modified = True
                task_rsrc['status'] = 'needsAction'
                task_rsrc.pop('completed')
        else:  # not near enough, assure status is completed
            if not is_completed:
                is_modified = True
                task_rsrc['status'] = 'completed'
        return task_rsrc

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


if __name__ == '__main__':
    tlts_list = update_shelve()
    pass
    # add a some super test or print function here.
