# 'tasklist_model' in 'tasks-cmd-line-sample'
#   '3/10/14'
#
# version 4.1 GIW  tasklist_style meaning logic is a function of the tasklist
# Model:
#   logic and rules operations for updating tasks.
#       operations are now a function of the tasklist.
#   interface to Data. Any data use goes thru Model.
# from urllib2 import HTTPError
######################
#  naming for ~ as  t: task, tl: tasklist, ttl: tasklist_task, f: facet
#  for example using t as ~:
#   ~_r:          t_rsrc          task api resource
#   ~_r_l:        t_rsrc_lst      task api resource items
#   ~_rx:         t_rsrc_xt       task api resource extended
#   ~_rx_l:       t_rsrc_xt_lst   task api resource extended items

from datetime import datetime
import task_helpers as h
import server

### GLOBAL
GBL_SERVICE = server.get_service()


 ### MAIN PREDICATE ###
def update_server():
    tasklist_rsrcs_list = tl_r_l = get_server_tasklist_items()
    tl_r_l = get_server_tl_task_items_in_(tl_r_l)
    tl_r_l = update_tl_tasks_in_(tl_r_l)
    tl_r_l = update_server_tl_task_in_(tl_r_l)
    tl_r_l = update_server_tasklists_in_(tl_r_l)
    return tl_r_l


 #### MAIN PREDICATE FUNCITONS


def get_server_tasklist_items():
    """
    gets a tasklist_list_response
        {
          "kind": "tasks#taskLists",
          "etag": string,
          "nextPageToken": string,
          "items": [
            tasklists Resource
          ]
        }

    The list maybe empty: NO tasklists.

    @rtype: list
    @return: a list of each tasklist_rsrc.
    """
    tasklist_list_response = GBL_SERVICE.tasklists().list().execute()  # predicate

    tasklist_rsrcs_list = [tl_r for tl_r in tasklist_list_response['items']]
    return tasklist_rsrcs_list


def get_server_tl_task_items_in_(tls_list):
    """

    gets a list of tasks- response - for each tasklist.
       {
          "kind": "tasks#tasks",
          "etag": string,
          "nextPageToken": string,
          "items": [
            tasks Resource
            ]
        }

    """
    def tasks_list_request(tl_id):
        return GBL_SERVICE.tasklists().list(tl_id).execute
    x = [tasks_list_request(tl['id']) for tl in tls_list]
    tasks_list_responses = x
    return tls_list


def update_tl_tasks_in_(tls_list):
    # for each task resource in each tasklist, return an updated task.
    # REFACT GIW: STUB
    return tls_list


def update_server_tl_task_in_(tls_list):
    # update server from the modified tasklist_list.
    #
    # REFACT STUB GIW
    return tls_list


def update_server_tasklists_in_(tls_list):
    # update server from the modified tasklist_list.
    #
    # REFACT STUB GIW
    return tls_list


############## DEPRECATED ###########
def update_ttls_from_(ttl_rsrc_dict):
    # update each tasklist in it's own scope.
    #i.e. justthe tasks in that tasklist.
    # ttl_r_d could be empty.
    if ttl_rsrc_dict:
        return ttl_rsrc_dict

    # locals
    ttl_xt = ttl_rsrc_dict.copy()
    tl = ttl_xt['tasklist']

    # PREDICATE: triage tasks for updating
    if tl['title'] == h.FILTER_FACETS:
        ttl_xt = apply_rule_near_due(ttl_xt)  # TODO REFRACT TEST STUB
        # ttl_xt = update_tl_facets(ttl_xt)
    else:  # update all the rest of the tasklists.
        ttl_xt = apply_rule_near_due(ttl_xt)
    return ttl_xt


def apply_rule_near_due(ttl_rsrc, now_dt=None):
    """ applies the rule; adds a new key {'modified': True | False}
     may or may not modify ttl_rsrc 'status' and 'completed'.
    @type ttl_rsrc: dict
    @param ttl_rsrc: i.e. ttl_rsrc['task']
    @type now_dt: datetime.datetime
    @param now_dt: datetime
    @return ttl_rsrc: tsk_rsrc with a new key: 'modified'.
    """
    ttl_rsrc['modified'] = False  # ADDED attribute. REMOVED in update_ttls_from()
    t = ttl_rsrc['task']
    if 'due' in t:
        due_dt = h.dt_from_(t['due'])
        now_dt = datetime.now() if not now_dt else now_dt  # added for testing
        ttl_rsrc['modified'] = False  # default - so there is always a modified attr.
        is_completed = t['status'] == 'completed'
        # MAIN PREDICATE
        if near_due_rule(due_dt, now_dt):
            if is_completed:  #
                ttl_rsrc['modified'] = True
                t['status'] = 'needsAction'
                t.pop('completed')
        else:  # not near enough, assure status is completed
            if not is_completed:
                ttl_rsrc['modified'] = True
                t['status'] = 'completed'
    return ttl_rsrc


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