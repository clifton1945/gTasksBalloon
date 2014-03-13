# 'tlt_object.py' in 'gTasksBalloon'
#   '3/12/14'/'3:26 PM'
#
# version 4.5 GIW  tasklist_style meaning logic is a function of the tasklist
# TODO UAE dict instead of tuple unless 2.7 has named tuples
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
import _bsddb
import task_helpers as h
import server

### GLOBAL
GBL_SERVICE = server.get_service()  # REFACT just use h.functions


 #### MAIN PREDICATES ###
def update_shelve():
    ret = h.shelve_to_db(serve_data_())  # REFACT doc in h.shelve data names
    assert isinstance(ret, list)
    return ret


def update_server_():
    # STUB
    return []


 #### MAIN PREDICATE FUNCTIONS


def serve_data_():
    """
    provides a list of tuples( tasklist resources, list of task resources FOR THIS tasklist)
    response ->
        {
          "kind": "tasks#taskLists",
          "etag": string,
          "nextPageToken": string,
          "items": [
            tasklists Resource
          ]
        }

    The list maybe empty: NO tasklists.

    gets a list of task resources:
    reponse ->
    {
      "kind": "tasks#tasks",
      "etag": string,
      "nextPageToken": string,
      "items": [
        tasks Resource
      ]
    }

    @rtype: list
    @return tlt_list: - a list of tuples
     ( "update_shelve: dict,
       "list_of_tasks": list
       )
    """
    tlt_list = []
    list_o_tasklists = GBL_SERVICE.tasklists().list().execute()  # predicate
    if 'items' in list_o_tasklists:
        for a_tasklist in list_o_tasklists['items']:
            list_o_tasks = GBL_SERVICE.tasks().list(tasklist=a_tasklist['id']).execute()
            if 'items' in list_o_tasks:
                tlt_list.append((a_tasklist, list_o_tasks['items']))
    return tlt_list


def update_data_(tlt_data_list):
    """
     modifies each tlt with update_rules which are a function of (tasklist_ type).
     returns a list of just the modified tlts.
    """
    # ADD rules for TRIALS, IDEAS, GOALS, etc.
    modified_tasks_list = []
    modified_tlt_data_list = []
    for tlt_tup in tlt_data_list:
        tl_dict, t_list = tlt_tup  # unpack tlt_tup tuple
        # triage tasklist types for different update rules.
        is_modified = False
        for t in t_list:
            t, is_modified = Rules.apply_rule_near_due(t)
            if is_modified:  # add this task_rsrc to list of tasks
                modified_tasks_list.extend(t)
        tlt_tup = tl_dict, modified_tasks_list  # re build the tlt tuple
        if is_modified: # append it to modified_tlt_data_list
            modified_tlt_data_list.extend(tlt_tup)
    return modified_tlt_data_list


# noinspection PyClassHasNoInit
class Pilot():

    DB_FILE_NAME = 'tests.myPilotDB'
    DB_ROOT_NAME = 'MyPilotTLT'
    FILTER_TRIALS = 'PILOTS'
    FILTER_FACETS = 'FACETS'

    def __init__(self):
        pass


    @staticmethod
    def update_pilot():
        """
        fundamentely a test tasklist. mocking production update_server()
        """
        tlt_list = Pilot.unshelve_pilot_data()
        assert isinstance(tlt_list, list)
        assert len(tlt_list) > 0
        tlt_list = update_data_(tlt_list)
        assert isinstance(tlt_list, list)
        # tlt_list = Pilot.shelve_pilot(tlt_list)
        # maybe print results
        return tlt_list


    @staticmethod
    def serve_pilot_data():
        """
        gets, returns tasklist='PILOTS' tlt_obj
        (tasklist rsrc: rsrc,
         list of tasks rsrcs: list
        )
        """
        tlt_obj_list = []
        pilot_id = "MTEzMzE3MDg1MTgzNjAxMjA2MzM6MTA4MzM1MTE1ODow"
        try:
            tl_rsrc = GBL_SERVICE.tasklists().get(tasklist=pilot_id).execute()
            t_rsrc_list = GBL_SERVICE.tasks().list(tasklist=pilot_id).execute()  # predicate
        except Exception as ex:
            template = "An exception of type {0} occured. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print "in [serve_pilot_data] ->" + message

        if 'items' in t_rsrc_list:
            tlt_obj = tl_rsrc, t_rsrc_list['items']
            tlt_obj_list.append(tlt_obj)

        return tlt_obj_list

    @staticmethod
    def update_pilot_shelve():
        tlt_obj_list = Pilot.unshelve_pilot_data()
        Pilot.shelve_pilot_data(tlt_obj_list)


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
        assert isinstance(ret, list)


# noinspection PyClassHasNoInit
class Rules():
    @staticmethod
    def update_tls_from_(tl_rsrc_dict):
        # update each tasklist in it's own scope.
        #i.e. justthe tasks in that tasklist.
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
    def apply_rule_near_due(task_rsrc, now_dt=None):
        """
        applies the rule;
        sets 'modified' bool;
        May or may not modify task_rsrc 'status' and 'completed'.
        @type task_rsrc: dict
        @param task_rsrc: i.e. task_rsrc
        @param now_dt: datetime - defaults to actual now() if no test now_date passed in.
        @type now_dt: datetime

        @return (
            "task_rsrc": dict,
            "is_modified": bool
            ): tuple
        """
        t = task_rsrc
        if 'due' in t:  # now add new ke: modified
            due_dt = h.dt_from_(t['due'])
            now_dt = datetime.now() if not now_dt else now_dt  # added for testing
            is_modified = False  # default - so there is always a modified attr.
            is_completed = t['status'] == 'completed'
            # MAIN PREDICATE
            if Rules.near_due_rule(due_dt, now_dt):
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
        tdel = due - now  # days to go IS POSITIVE
        return after_near <= tdel.days <= before_near


if __name__ == '__main__':
    update_shelve()
    # add a some super test or print function here.
