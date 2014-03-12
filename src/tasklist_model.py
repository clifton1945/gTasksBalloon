# 'tasklist_model' in 'gTasksBalloon'
# 3/12/14
#
# version 4.5 GIW  tasklist_style meaning logic is a function of the tasklist
# Model:
#   logic and rules operations for updating tasks.
#       operations are now a function of the tasklist.
#   interface to Data. Any data use goes thru Model.
# from urllib2 import HTTPError

from datetime import datetime
import task_helpers as h
import server

### GLOBAL
GBL_SERVICE = server.get_service()


 ### MAIN PREDICATE ###
def update_server():
    tasklist_rsrcs_list = get_server_tasklist_items()
    tl_rx_l = get_server_tl_task_items_in_(tasklist_rsrcs_list)  # tasklist dict now xtended: lotasks' key.
    tl_mod_l = update_tl_tasks_in_(tl_rx_l)
    tl_rx_l = update_server_from_(tl_mod_l)

    # for a while I'll print some of this stuff.
    template = "  server->{}:tasklists/ {}:tasks\n" \
               "modified->{}:tasklists/ {}:tasks\n"
    print template.format(len(tl_rx_l),
                          sum([len(tlt['lotasks']) for tlt in tl_rx_l]),
                          len(tl_mod_l),
                          sum([len(tlt['lotasks']) for tlt in tl_mod_l])
                            )
    return tl_rx_l


 #### MAIN PREDICATE FUNCITONS


def get_server_tasklist_items():
    """
    gets a list of tasklist responses
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
    enhances each tasklist rsrc w/ {'lotasks':  list of task rsrcs['items']}.
    response ->       {
          "kind": "tasks#tasks",
          "etag": string,
          "nextPageToken": string,
          "items": [
            tasks Resource
            ]
        }
    The list maybe empty: NO tasks.

    @type: list
    @params: tls_list
    @rtype: list
    @return: a list of enhanced tasklist_rsrc.
    """
    for tl in tls_list:
        response = GBL_SERVICE.tasks().list(tasklist=tl['id']).execute()
        if 'items' in response:
            # add key/value to tasklist rsrc dict
            tl['lotasks'] = response['items']
    return tls_list


def update_tl_tasks_in_(tls_list):
    # return any updated tasks.
    lomods = []
    for tl in tls_list:
        for t in tl['lotasks']:
            if t['title'][:5] == 'TRIAL':  # TODO STUB filter on this name
                lomods.append(t)
                tl['lotasks'] = lomods

    return tls_list


def update_server_from_(modfd_tl_list):
    """
    update server for each MODIFIED task_rsrc.

    @type modfd_tl_list:  list
    @param modfd_tl_list: list of tasks that have been modified e.g. made visible
    @rtype: list
    @return modfd_tl_list: list of tasks that have been modified e.g. made visible
    NOTE: extended k/v are not presented to GBL_SERVICE...execute()
    """
    returned_tl_list = []
    for tl_xdict in modfd_tl_list:
        # only present api standard resources.
        if 'lotasks' in tl_xdict:
            ret_task_list = []
            for t_rsrc in tl_xdict['lotasks']:
                ret_t_rsrc = update_server_tasks_with_(tl_xdict, t_rsrc)
                ret_task_list.append(ret_t_rsrc)
                   #  now rebuild tl_xdict
            tl_xdict['lotasks'] = ret_task_list
            returned_tl_list.append(tl_xdict)
        # the implied else just returns an empty returned_tl_list.
    return returned_tl_list


def update_server_tasks_with_(tl_rsrc, task_rsrc):
    """

    @param tl_rsrc: dict
    @type tl_rsrc: dict
    @param task_rsrc: dict
    @type task_rsrc: dict

    @rtype: dict
    server returns a task rsrc -> {
      "kind": "tasks#task",
      "id": string,
      "etag": etag,
      "title": string,
      "updated": datetime,
      "selfLink": string,
      "parent": string,
      "position": string,
      "notes": string,
      "status": string,
      "due": datetime,
      "completed": datetime,
      "deleted": boolean,
      "hidden": boolean,
      "links": [
        {
          "type": string,
          "description": string,
          "link": string
        }
      ]
    }
    """
    try:
        new_task_rsrc = GBL_SERVICE.tasks().update(
            tasklist=tl_rsrc['id'],
            task=task_rsrc['id'],
            body=task_rsrc
        ).execute()  # MAIN predicate. only present api standard resources
        return new_task_rsrc

    except Exception as ex:
        print 'UPDATE FAILED: tlTitle:{} tTitle:{}\n...task:{}'\
            .format(tl_rsrc['title'], task_rsrc['title'], task_rsrc)
        template = "An exception of type {0} occured. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print message
        return {}


############## DEPRECATED ###########


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
        tl_xt = apply_rule_near_due(tl_xt)
        # tl_xt = update_tl_facets(tl_xt)
    else:  # update all the rest of the tasklists.
        tl_xt = apply_rule_near_due(tl_xt)
    return tl_xt


def apply_rule_near_due(tl_rsrc, now_dt=None):
    """ applies the rule; adds a new key {'modified': True | False}
     may or may not modify tl_rsrc 'status' and 'completed'.
    @type tl_rsrc: dict
    @param tl_rsrc: i.e. tl_rsrc['task']
    @type now_dt: datetime.datetime
    @param now_dt: datetime
    @return tl_rsrc: tsk_rsrc with a new key: 'modified'.
    """
    tl_rsrc['modified'] = False  # ADDED attribute. REMOVED in update_tls_from()
    t = tl_rsrc['task']
    if 'due' in t:
        due_dt = h.dt_from_(t['due'])
        now_dt = datetime.now() if not now_dt else now_dt  # added for testing
        tl_rsrc['modified'] = False  # default - so there is always a modified attr.
        is_completed = t['status'] == 'completed'
        # MAIN PREDICATE
        if near_due_rule(due_dt, now_dt):
            if is_completed:  #
                tl_rsrc['modified'] = True
                t['status'] = 'needsAction'
                t.pop('completed')
        else:  # not near enough, assure status is completed
            if not is_completed:
                tl_rsrc['modified'] = True
                t['status'] = 'completed'
    return tl_rsrc


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
    update_server()  # FILL Shelve with current state of ALL TASKS.
    # get_and_shelve_all_ttls()  # this is used for testing.