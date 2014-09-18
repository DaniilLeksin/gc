__author__ = 'Daniil Leksin'
# -*- coding: utf-8 -*-

import sys
import json
import pprint

from googleapiclient.errors import HttpError
from oauth2client.client import AccessTokenRefreshError

from c_gawrapper.c_api import GoogleAnalyticApi


def main(argv):

    # TODO: check the valid input data
    # TODO: handle IOError
    # TODO: handle KeyError
    try:
        # Load the credentials
        # json format is got from: https://developers.google.com/analytics/solutions/articles/hello-analytics-api
        credentials = json.loads(open(argv[1], 'rb').read())
        client_id = credentials["installed"]["client_id"]
        client_secret = credentials["installed"]["client_secret"]
        # Load other properties
        properties = json.loads(open(argv[2], 'rb').read())
        start_date = properties['start-date']
        end_date = properties['end-date']
        dimensions = properties['dimensions']
        metrics = properties['metrics']
        filters = properties['filters']

        # Make instance of the google api class
        api = GoogleAnalyticApi(client_id, client_secret)
        # Go go go
        res = api.callAPI(start_date, end_date, metrics=metrics, dimensions=dimensions, filters=filters)
        pprint.pprint(res)

    except TypeError as error:
        print ('There was an error in constructing your query : %s' % error)
    except HttpError as error:
        print ('Arg, there was an API error : %s : %s' % (error.resp.status, error._get_reason()))
    except AccessTokenRefreshError:
        print ('The credentials have been revoked or expired, please re-run the application to re-authorize')


if __name__ == "__main__":
    main(sys.argv)

