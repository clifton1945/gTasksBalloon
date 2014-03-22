

# 'tlt_object.py' in 'gTasksBalloon'
# GIW  WORKING update_data() for apply rule near due
# stable 3 tests
#   version 4.9.7 GIWr
#   '3/21/14'
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
    selves new server data -> list of tlt objects.
    @return: tlt_obj_list
    @rtype: list
    """
    my_name = "f.update_shelve"

    tlt_obj_list = h.shelve_to_db(serve_data())  # PREDICATE

    assert h.is_valid_tlt_list_(tlt_obj_list, do_print, my_name)  # expect valis list of tlt objects.
    return tlt_obj_list


def update_data_(tlt_obj_list):
    """
     modifies each tlt with update_rules which are a function of (tasklist_ type).
     returns a list of just the modified tlts.
     @param tlt_obj_list: list
     @return: modified tlt_mod_list
    """
    # ADD rules for TRIALS, IDEAS, GOALS, etc.
    # my_name = "f.update_data_"
    tlt_mod_list = [Rules.apply_rule_near_due(tlt_obj)
                    for tlt_obj in tlt_obj_list
                    if Rules.need_to_modify_this_(tlt_obj)]
    return tlt_mod_list


def update_server(tlt_obj_list):
    # locals
    list_of_rsps = []
    for tlt_obj in tlt_obj_list:
        for task_obj in tlt_obj['t_list']:
            #try
            # noinspection PyPep8
            rsp = GBL_SERVICE.tasks().update(
                tasklist=tlt_obj['tl_rsrc']['id'],
                task=task_obj['id'],
                body=task_obj
                ).execute()
            list_of_rsps.append(rsp)

    #rebuild tlt_obj_list now tlt_rsp_list
    tl_list = [tlt_obj['tl_rsrc'] for tlt_obj in tlt_obj_list]
    tlt_rsp_list = [{'tl_rsrc': tl_rsrc, 't_list': list_of_rsps}
                    for tl_rsrc, t_list in zip(tl_list, list_of_rsps)]
    return tlt_rsp_list


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
        @return: modified_tasks_list
        @rtype:  list
        """
        #local

        modified_tasks_list = [Rules.update_this_(task_rsrc)
                               for task_rsrc in task_rsrc_list
                               if Rules.need_to_modify_this_(task_rsrc)]

        return modified_tasks_list

    @staticmethod
    def update_this_(task_rsrc):
        """

        """
        # local
        n = task_rsrc
        is_completed = True if task_rsrc['status'] == 'completed' else False

        if is_completed:  #
            n['status'] = 'needsAction'
            n.pop('completed')
            ret = task_rsrc
        else:  # it is not completed:  # i.e. has needAction already
            n['status'] = 'completed'
            ret = task_rsrc
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
        need_to_modify_this = False
        if 'due' in task_rsrc:
            # locals
            task_is_near_due = Rules.near_due_rule(task_rsrc)
            task_is_visible = (task_rsrc['status'] == 'needsAction') and 'completed' not in task_rsrc
            task_is_not_visible = (task_rsrc['status'] == 'completed')
            #PREDICATE
            if task_is_near_due:
                if task_is_not_visible:
                    need_to_modify_this = True
            else:  # task is NOT near_due
                if task_is_visible:
                    need_to_modify_this = True

        return need_to_modify_this

    @staticmethod
    def near_due_rule(t_obj, tst_now=None):
        """now dt is near enough to due dt.
        sets default before and after days to be near
        @param: t_obj
        @type t_obj: dict
        @param tst_now: datetime  for testing
        due: datetime
        now: datetime
        @rtype: bool
        @return True if near enough to due date.
        """
        #locals
        after_near = 2.01   # refact to class attribute
        before_near = 2.01  # now <= due -> days before due
        ret = False
        # PREDICATE
        if 'due' in t_obj:  # otherwise no rule
            due = h.dt_from_(t_obj['due'])
            now = datetime.now() if tst_now is None else tst_now

            if now >= due:  # delta is days AFTER due
                ret = (now - due) < timedelta(after_near)   # days to go ALWAYS IS POSITIVE
            else:           # now <= due delta is days before due
                ret = (due - now) <= timedelta(before_near)   # days to go ALWAYS IS POSITIVE
        return ret


if __name__ == '__main__':
    tlts_list = update_shelve(True)
    pass
