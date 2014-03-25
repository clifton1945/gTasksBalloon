# 'task_helpers' in 'tasks-cmd-line-sample'
#   '3/6/14'/'12:13 PM'

from datetime import datetime
import shelve

 ### GLOBAL DEFAULT ####################
DB_FILE_NAME = 'C:/GitHub/gTasksBalloon/myTaskDB'
DB_ROOT_NAME = 'MyTasks'
FILTER_TRIALS = 'TRIALS'
FILTER_FACETS = 'FACETS'

################ HELPER FUNCTIONS #################


###########  Tasklist Task [tlt] Testing #############
def is_valid_tlt_(tlt_obj, do_print=False, test_name=None):
    do_print = do_print and True
    my_name = "is_valid_tlt_"
    full_name = "  " + my_name if test_name is None else test_name + "." + my_name

    ret = isinstance(tlt_obj, dict)\
        and isinstance(tlt_obj['tl_rsrc'], dict)\
        and isinstance(tlt_obj['t_list'], list)

    if do_print:
        print_tlt_(tlt_obj, full_name)
    return ret


def is_valid_tlt_list_(tlt_obj_list, do_print=False, test_name=None):
    do_print = do_print and True
    my_name = "is_valid_tlt_list_"
    full_name = ("   ." + my_name) if test_name is None else (test_name + "." + my_name)
    if do_print:
        print_summary_ttl_list_(tlt_obj_list, "\n" + full_name)
    return isinstance(tlt_obj_list, list)  # expect a tlt_obj_list ")


    ############ Tasklist Printing ##################


def print_summary_ttl_list_(tlt_list, test_name=None):
    # noinspection PyProtectedMember
    print "\n{}->\n  " \
        "tlt list has {} tlt_obj.". \
        format(test_name, len(tlt_list))
    [print_tlt_(tlt, "...") for tlt in tlt_list]


def print_short_ttl_list_(tlt_list, test_name=None):
    # noinspection PyProtectedMember
    print "\n{}->\ntlt list has {} tlt_obj.". \
        format(test_name, len(tlt_list))

    # [print_tlt_(tlt, "...") for tlt in tlt_list]
    for tlt in tlt_list:
        # print_tlt_(tlt, "...")
        print_t_list_(tlt)


def print_tlt_(tlt_obj, test_name=None):
    # noinspection PyProtectedMember
    print "{}    " \
        "one tlt_obj has tl_rsrc[title]:{}, " \
        "and a task list of {} task rsrcs.". \
        format(test_name, tlt_obj['tl_rsrc']['title'], len(tlt_obj['t_list']))


def print_summary_t_list_(t_list, test_name=None):
    # noinspection PyProtectedMember
    print "{}->\n  " \
        "t list has {} t_obj.". \
        format(test_name, len(t_list))


def print_t_list_(tlt_obj, test_name=None):
    # noinspection PyProtectedMember
    if 'items' in tlt_obj['t_list']:
        _t_list = tlt_obj['t_list']
        l = len(_t_list)
        print "{}->\n  " \
            "t_obj list is {} long.". \
            format(test_name, l)
        print_t_objs_in_t_list_in_(tlt_obj)


def print_t_objs_in_t_list_in_(tlt_obj, test_name=None):
    """
    prints abbreviated summary of all task
    :type tlt_obj: dict
    """
    template = "-> task[{status}]:'{title}' "

    print "\n" + test_name
    for t_rsrc in tlt_obj['t_list']:
        print template.format(**t_rsrc)
    
    
###############   Data ############################
def shelve_to_db(tlt_rsrcs_list, db_file_name=DB_FILE_NAME, db_root_name=DB_ROOT_NAME):
    """ shelves A LIST tlt dicts.

    @type tlt_rsrcs_list: list
    @param: tlt_rsrcs_list: list
    @param db_file_name: <str> w/ default DB_FILE_NAME
    @param db_root_name: <str> w/ default DB_ROOT_NAME
    @return: tlt_rsrcs_list  as received!!
    """
    db = shelve.open(db_file_name)
    db[db_root_name] = tlt_rsrcs_list
    db.close()
    return tlt_rsrcs_list


def unshelve_from_db(db_file_name=DB_FILE_NAME, db_root_name=DB_ROOT_NAME):
    """ unshelve and return a dict of every item.

    @param db_file_name: str w/ default
    @param db_root_name: str w/ default
    @rtype: list
    @return tlt_rsrcs_list: list
    """
    db = shelve.open(db_file_name)
    tlt_rsrcs_list = db[db_root_name]
    db.close()
    return tlt_rsrcs_list


def dt_from_(rfc_str):
    """
    pseudo RFC3339 rfc_str: iso + 'Z' to datetime.
    strip Z off back of rfc_str
    @param rfc_str:
    @return: datetime or None
    """
    # if rfc_str is datetime.isoformat()
    try:
        ret = datetime.strptime(rfc_str[:-1], "%Y-%m-%dT%H:%M:%S.%f")
    except ValueError:
        print ("function:dt_from_(rfc_str) problem.\n  " +
               "[%s] not valid RFC3999 format." % rfc_str)
        ret = None
    return ret


def rfc_from_(dt):
    """ datetime to pseudo RFC3339: iso + 'Z'.
    @param dt: datetime
    @return: pseudo RFC3339
    """
    return dt.isoformat("T") + "Z"



