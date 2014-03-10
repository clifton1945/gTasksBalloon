"""server.py
NOTE: 140205 mostly changed this to be a module.

coding: utf-8
Command-line skeleton application for Tasks API.
Usage:-
  $ python seerver.py

You can also get help on all the command-line flags the program understands
by running:

  $ python server.py --help

"""
# TODO move server to src/ and figure out how to get server.dat to work.


import argparse
import httplib2
import os
# import pprint

from apiclient import discovery
from oauth2client import file
from oauth2client import client
from oauth2client import tools

# Parser for command-line arguments.
parser = argparse.ArgumentParser(
    description=__doc__,
    formatter_class=argparse.RawDescriptionHelpFormatter,
    parents=[tools.argparser])


""" # application, including client_id and client_secret. You can see the Client ID
# and Client secret on the APIs page in the Cloud Console:
# <https://cloud.google.com/console#/project/556428330551/apiui>
"""
CLIENT_SECRETS = os.path.join(os.path.dirname(__file__), 'src/client_secrets.json')


"""# Set up a Flow object to be used for authentication.
# Add one or more of the following scopes. PLEASE ONLY ADD THE SCOPES YOU
# NEED. For more information on using scopes please see
# <https://developers.google.com/+/best-practices>.
"""
FLOW = client.flow_from_clientsecrets(CLIENT_SECRETS,
                                      scope=['https://www.googleapis.com/auth/tasks',
                                      'https://www.googleapis.com/auth/tasks.readonly', ],
                                      message=tools.message_if_missing(CLIENT_SECRETS))


def get_service(argv=None):
    """as module returns a service object for server methods.
    as main I'll run this from windows tasks.

    @param argv:
    @return: Resource
    """
    # Parse the command-line flags.
    if argv:
        flags = parser.parse_args(argv[1:])

    # If the credentials don't exist or are invalid run through the native client
    # flow. The Storage object will ensure that if successful the good
    # credentials will get written back to the file.
    storage = file.Storage('server.dat')
    credentials = storage.get()
    if credentials is None or credentials.invalid:
        credentials = tools.run_flow(FLOW, storage, flags=None)

    # Create an httplib2.Http object to handle our HTTP requests and authorize it
    # with our good Credentials.
    http = httplib2.Http()
    http = credentials.authorize(http)
    # Construct the service_ object for the interacting with the Tasks API.
    service_ = discovery.build('tasks', 'v1', http=http)
    try:
        assert isinstance(service_, discovery.Resource)
    except client.AccessTokenRefreshError:
        print ("The credentials have been revoked or expired, please re-run"
               "the application to re-authorize")
    return service_



