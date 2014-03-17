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
        print_tlt_list_(tlt_obj_list, "\n" + full_name)

    ret = isinstance(tlt_obj_list, list)  # expect a tlt_obj_list ")

    l = len(tlt_obj_list)
    if l > 0:
        ret = ret and is_valid_tlt_(tlt_obj_list[0], do_print, full_name)
    if l > 1:
        ret = ret and is_valid_tlt_(tlt_obj_list[1], do_print, full_name)
        ret = ret and tlt_obj_list[1] != tlt_obj_list[0]

    return ret


def print_tlt_list_(tlt_list, test_name=None):
    # noinspection PyProtectedMember
    print "{}->\n  " \
        "tlt list has {} tlt objects.". \
        format(test_name, len(tlt_list))


def print_t_list_(tlt_list, test_name=None):
    # noinspection PyProtectedMember
    print "{}->\n  " \
        "t list has {} t objects.". \
        format(test_name, len(tlt_list))


def print_tlt_(tlt_obj, test_name=None):
    # noinspection PyProtectedMember
    print "{}->\n    " \
        "one tlt object has tl_rsrc[title]:{}, and a task list of {} task rsrcs.". \
        format(test_name, tlt_obj['tl_rsrc']['title'], len(tlt_obj['t_list']))


###############   Data ############################
def shelve_to_db(tlt_rsrcs_list, db_file_name=DB_FILE_NAME, db_root_name=DB_ROOT_NAME):
    """ shelves a dict of all tasks.

    @type tlt_rsrcs_list: list
    @param: tlt_rsrcs_list: list
    @param db_file_name: <str> w/ default DB_FILE_NAME
    @param db_root_name: <str> w/ default DB_ROOT_NAME
    @return: tlt_rsrcs_list  unchanged
    """
    db = shelve.open(db_file_name)
    db[db_root_name] = tlt_rsrcs_list
    db.close()
    return tlt_rsrcs_list


def depr_shelve_to_db(ttl_rsrcs_dict, db_file_name=DB_FILE_NAME, db_root_name=DB_ROOT_NAME):
    """ shelves a dict of all tasks.

    @type ttl_rsrcs_dict: dict
    @param: ttl_rsrcs_dict: <dict
    @param db_file_name: <str> w/ default DB_FILE_NAME
    @param db_root_name: <str> w/ default DB_ROOT_NAME
    @return: ttl_rsrcs_dict  unchanged
    """
    db = shelve.open(db_file_name)
    db[db_root_name] = ttl_rsrcs_dict
    db.close()
    return ttl_rsrcs_dict


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



