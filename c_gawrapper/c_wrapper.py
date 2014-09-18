__author__ = 'Daniil Leksin'
# -*- coding: utf-8 -*-

from googleapiclient.errors import HttpError
from oauth2client.client import AccessTokenRefreshError
from c_warning import show_warning

from c_gawrapper.c_api import GoogleAnalyticApi


def check_the_data(info_obj=None):
    return True


def make_report(credentials, params, all_metrics):
    try:
        client_id = credentials["installed"]["client_id"]
        client_secret = credentials["installed"]["client_secret"]

        # Load other properties except Dimensions and Metrics
        start_date = params['start-date']
        end_date = params['end-date']
        filters = params['filters']

        # Load Metrics
        dimensions = ''
        metrics = 'ga:sessions,'
        for p_property in all_metrics['/']:
            if all_metrics["/"][p_property]["value"]:
                if all_metrics["/"][p_property]["view"] in ["Metrics"]:
                    metrics += '%s,' % p_property
                else:
                    dimensions += '%s,' % p_property
        # Make instance of the google api class
        api = GoogleAnalyticApi(client_id, client_secret)

        # To delete
        if len(dimensions) > 0:
            if dimensions[-1] == ',': dimensions = dimensions[: -1]
        if metrics[-1] == ',': metrics = metrics[: -1]
        # Go go go
        res = api.callAPI(start_date, end_date, metrics=metrics, dimensions=dimensions, filters=filters)
        return res

    except TypeError as error:
        show_warning('There was an error in constructing your query : %s' % error)
        print ('There was an error in constructing your query : %s' % error)
    except HttpError as error:
        show_warning('Arg, there was an API error : %s : %s' % (error.resp.status, error._get_reason()))
        print ('Arg, there was an API error : %s : %s' % (error.resp.status, error._get_reason()))
    except AccessTokenRefreshError:
        show_warning('The credentials have been revoked or expired, please re-run the application to re-authorize')
        print ('The credentials have been revoked or expired, please re-run the application to re-authorize')
