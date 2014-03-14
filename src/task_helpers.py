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
def shelve_to_db(ttl_rsrcs_dict, db_file_name=DB_FILE_NAME, db_root_name=DB_ROOT_NAME):
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
    @rtype: dict
    @return ttl_rsrcs_dict: dict
    """
    db = shelve.open(db_file_name)
    ttl_rsrcs_dict = db[db_root_name]
    db.close()
    return ttl_rsrcs_dict


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



