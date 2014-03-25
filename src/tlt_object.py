

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
     update_data() is the main PREDICATE of th project. Each tlt_object is subjected to a series of Rules.
        If the rule dictates, the object is modifed, and returned to a modified_tlt_objs list.

     @param tlt_obj_list: list
     @return is_modified: bool
    """
    # ADD rules for TRIALS, IDEAS, GOALS, etc.
    tlt_mod_list = [tlt_obj for tlt_obj in tlt_obj_list
                    if Rules.apply_rule_near_due(tlt_obj)]
    return tlt_mod_list


def update_server(tlt_obj_list):
    # locals
    t_rsp_list = []
    for tlt_obj in tlt_obj_list:
        for task_obj in tlt_obj['t_list']:
            #try
            # noinspection PyPep8
            rsp = GBL_SERVICE.tasks().update(
                tasklist=tlt_obj['tl_rsrc']['id'],
                task=task_obj['id'],
                body=task_obj
                ).execute()
            t_rsp_list.append(rsp)
        task_obj['t_list'] = t_rsp_list
    return tlt_obj_list


# noinspection PyClassHasNoInit
class Rules():
    @staticmethod
    def apply_rule_near_due(tlt_obj):
        """
         apply_rule_ need_to_modify_this_( to each t_obj).
         If the tlt is modified / updated
         return True so that it will be included in a 'modified tlt obj list'

         @param tlt_obj: dict
         @return: is_modified
         @rtype: bool
        """
        #local
        is_modified = False
        # noinspection PyUnusedLocal
        modified_tasks_list = mt_l = []
        # PREDICATE
        assert 't_list' in tlt_obj  # always
        if len(tlt_obj['t_list']) > 0:
            mt_l = [t_obj for t_obj in tlt_obj['t_list']
                    if Rules.need_to_modify_this_(t_obj)]
        if len(mt_l) > 0 :
            is_modified = True
        tlt_obj['t_list'] = mt_l
        return is_modified

    @staticmethod
    def need_to_modify_this_(t_obj):
        """
        apply_rule: Rules.near_due_rule(to each t_obj task_rsrc).
        If the t_obj is modified / updated
        return True so that it will be included in a 'modified t_obj list'

        @type t_obj: dict
        @param t_obj: -> a tasks api resource dict
        @return: is_modified
        @rtype: bool

        modify tasks that are near_due
            but don't have
            (1) 'status'='needsAction' and (2) no 'completed' key.
        modify tasks that are NOT near_due
            but don't have
            (1) 'status'='complete'
        """

        need_to_modify_this = False
        if 'due' in t_obj:
            # locals
            task_is_near_due = Rules.near_due_rule(t_obj)
            task_is_visible = (t_obj['status'] == 'needsAction') and 'completed' not in t_obj
            task_is_not_visible = not task_is_visible
            #PREDICATE
            if task_is_near_due:
                if task_is_not_visible:
                    t_obj['status'] = 'needsAction'
                    t_obj.pop('completed')
                    need_to_modify_this = True
            else:  # task is NOT near_due
                if task_is_visible:
                    t_obj['status'] = 'completed'
                    need_to_modify_this = True

        return need_to_modify_this

    @staticmethod
    def update_this_(t_obj):
        """
        modify the task resource obj IF
        """
        # local
        is_completed = True if t_obj['status'] == 'completed' else False

        if is_completed:  #
            t_obj['status'] = 'needsAction'
            t_obj.pop('completed')
            ret = t_obj
        else:  # it is not completed:  # i.e. has needAction already
            t_obj['status'] = 'completed'
            ret = t_obj
        return ret

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
