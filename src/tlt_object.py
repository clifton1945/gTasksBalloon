# 'tlt_object.py' in 'gTasksBalloon'
# GIW  WORKING update_data() for apply rule near due
# stable 3 tests
#   version 4.9 GIW  using a dict tlt_obj: {tasklist rsrc, list of task rsrcs}
#   '3/18/14'
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


from datetime import datetime, timedelta
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
    test_name = "f: serve_data"
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
        #  now validate
        h.is_valid_tlt_list_(tlt_obj_list, do_print, test_name)

    except Exception as ex:  # return an empty list.
        template = "An exception of type {0} occured. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print "in [serve_pilot_data] ->" + message

    return tlt_obj_list


def update_shelve(do_print=False):
    """
    selves server data -> list of tlt objects..
    """
    my_name = "f.update_shelve"

    tlt_obj_list = h.shelve_to_db(serve_data())
    assert h.is_valid_tlt_list_(tlt_obj_list, do_print, my_name)  # expect valis list of tlt objects.
    return tlt_obj_list


def update_data_(tlt_obj_list):
    """
     modifies each tlt with update_rules which are a function of (tasklist_ type).
     returns a list of just the modified tlts.
    """
    # ADD rules for TRIALS, IDEAS, GOALS, etc.
    my_name = "f.update_data_"
    # TODO FIX  the mod list MUST MEET two requirements: near due AND requires a change. COMBINE SOMEHOW.
    mod_tlt_list = [Rules.apply_rule_near_due(t) for tlt in tlt_obj_list
                    for t in tlt['t_list']
                    if Rules.near_due_rule(t)]  # modified_tlt_objs_list
    return mod_tlt_list


def set_due_list(tlt_obj_list):
    tltdl = tlt_obj_list
    mod_list = [x for l in tltdl
                for tl in l
                for x in tl
                if isinstance(x, list)]
    return mod_list


 #### MAIN PREDICATE FUNCTIONS


# noinspection PyClassHasNoInit
class Rules():
    @staticmethod
    def apply_rule_near_due(task_rsrc_list):
        """
        assure all tasks that are near_due have
            (1) 'status'='needsAction' and (2) no 'completed' key.
        assure all tasks that are NOT near_due have
            (1) 'status'='complete'
        and don't modify any tasks that don't need to be.

        @type task_rsrc_list: dict
        @ptask_rsrc_list_rsrc that HAVE PASSED near_due rule().

        @return task_rsrc:  modified tasks
        """
        #local

        ret = [Rules.update_this_(task_rsrc) for tl, lot in task_rsrc_list for task_rsrc in lot
               if Rules.need_to_modify_this_(task_rsrc)]

        return ret

    @staticmethod
    def need_to_modify_this_(task_rsrc):
        """
        modify tasks that are near_due
            but don't have
            (1) 'status'='needsAction' and (2) no 'completed' key.
        modify tasks tasks that are NOT near_due
            but don't have
            (1) 'status'='complete'

        """
        # locals
        task_is_near_due = Rules.near_due_rule(task_rsrc)
        task_is_visible = (task_rsrc['status'] == 'needsAction') and 'completed' not in task_rsrc
        task_is_not_visible = (task_rsrc['status'] == 'completed')
        need_to_modify_this = False
        #PREDICATE
        if task_is_near_due:
            if task_is_not_visible:
                need_to_modify_this = True
        else:  # task is NOT near_due
            if task_is_visible:
                need_to_modify_this = True
        return need_to_modify_this

    @staticmethod
    def update_this_(task_rsrc):
        """

        """
        # local
        n = task_rsrc
        is_completed = True if n['status'] == 'completed' else False

        if is_completed:  #
            n['status'] = 'needsAction'
            n.pop('completed')
            ret = task_rsrc
        else:  # it is not completed:  # i.e. has needAction already
            n['status'] = 'completed'
            ret = task_rsrc
        return ret

    @staticmethod
    def near_due_rule(t_obj, tst_now=None):
        """now dt is near enough to due dt.
        sets default before and after days to be near
        @param: t_obj
        @type t_obj: dict
        @param tst_now : datetime  for testing
        due: datetime
        now: datetime
        @rtype: bool
        @return True if near enough to due date.
        """
        #locals
        before_near = 2  # now <= due -> days before due
        after_near = 2   # refact to class attribute
        ret = False
        # PREDICATE
        if 'due' in t_obj:  # otherwise no rule
            due = h.dt_from_(t_obj['due'])
            now = datetime.now() if tst_now is None else tst_now

            if now >= due:  # delta is days AFTER due
                ret = (now - due) < timedelta(after_near)   # days to go ALWAYS IS POSITIVE
            else:           # now <= due delta is days before due
                ret = (due - now) < timedelta(before_near)   # days to go ALWAYS IS POSITIVE
        return ret


if __name__ == '__main__':
    tlts_list = update_shelve(True)
    pass

