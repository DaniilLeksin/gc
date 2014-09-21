"""
.. module:: api 4 Google analytics
    .. platform: Unix, Windows
    .. synopsis: Module to be the master in Google Analytics API (:

.. moduleauthor:: <itdoesn'tmetterat.com>
"""

__author__ = 'Daniil Leksin'
# -*- coding: utf-8 -*-

import httplib2
from googleapiclient.discovery import build
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.file import Storage
from oauth2client.tools import run

TOKEN_FILE_NAME = 'analytics.dat'


class GoogleAnalyticApi(object):
    """GoogleAnalyticApi is a class providing the actions to control and manage the Google Reports

    This class is called from console & UI as the instance.

    .. note::
        In this class we use hard coded parameters:
            * TOKEN_FILE_NAME = 'analytics.dat' - file to store tokens
            * redirect_uri='http://localhost:8080/oauth2' - Determines where the response is sent.
            * scope='https://www.googleapis.com/auth/analytics.readonly' - Identifies the Google API access that your
            application is requesting.

    """
    def __init__(self, client_id, client_secret, redirect_uri='http://localhost:8080/oauth2',
                 user_agent='analytics-api-v3-awesomeness'):
        """Init functions fot the class GoogleAnalyticApi.

        Args:
            client_id (str): Identifies the client that is making the request.
            client_secret (str): Identifies the client secret to get access to app

        Kwargs:
            redirect_uri (str): Determines where the response is sent.
            user_agent (str): Can be used by web analytics to identify OS, Browser etc ...
        """

        # Forming OAuth flow to have access to the installed app
        flow = OAuth2WebServerFlow(
            client_id=client_id,            # Client identifier
            client_secret=client_secret,    # Client secret key
            scope='https://www.googleapis.com/auth/analytics.readonly',
            redirect_uri=redirect_uri,      # Response URI
            user_agent=user_agent
        )

        # Create storage for token
        storage = Storage(TOKEN_FILE_NAME)
        self.credentials = storage.get()

        # Check if everything is ok with client secrets
        if not self.credentials or self.credentials.invalid:
            self.credentials = run(flow, storage)

        self.service = self._initialize_service()     # The service object built by the Google API Python client library
        self.profile_id = self.get_first_profile_id()   # The first profile ID

    def _initialize_service(self):
        """
        Create An Analytics Service Object

        ..Note:: we need to use that authorization and apply it to an http object. The http object will be used
        to create an Analytics service object.
        Returns:
            Analytic service object
        """
        http = self.credentials.authorize(httplib2.Http())
        return build('analytics', 'v3', http=http)

    def get_first_profile_id(self):
        """Traverses Management API to return the first profile id.

        .. Note::This first queries the Accounts collection to get the first account ID.
        This ID is used to query the Webproperties collection to retrieve the first
        webproperty ID. And both account and webproperty IDs are used to query the
        Profile collection to get the first profile id.

        Returns:
        A string with the first profile ID.
        None if a user does not have any accounts, webproperties, or profiles.
        """

        # Get a list of all Google Analytics accounts for this user
        accounts = self.service.management().accounts().list().execute()

        if accounts.get('items'):
            # Get the first Google Analytics account
            firstAccountId = accounts.get('items')[0].get('id')

            # Get a list of all the Web Properties for the first account
            webproperties = self.service.management().webproperties().list(accountId=firstAccountId).execute()

            if webproperties.get('items'):
                # Get the first Web Property ID
                firstWebpropertyId = webproperties.get('items')[0].get('id')

                # Get a list of all Views (Profiles) for the first Web Property of the first Account
                profiles = self.service.management().profiles().list(
                    accountId=firstAccountId,
                    webPropertyId=firstWebpropertyId).execute()

                if profiles.get('items'):
                    # return the first View (Profile) ID
                    return profiles.get('items')[0].get('id')

        return None

    def callAPI(self, date_from, date_to, metrics='ga:sessions', dimensions=None, sort=None, filters=None,
                segment=None, sampling_level=None, start_index=None, max_results=None, output=None, fields=None):
        """Executes and returns data from the Core Reporting API.
          This queries the API for the top 25 organic search terms by visits.

        Args:
            date_from (str) - start date for fetching Analytics data.
            date_to (str) - end date for fetching Analytics data.
        Kwargs:
            metrics='ga:sessions' (str) - a list of comma-separated metrics

            ..note:: One metric is a must

            dimensions=None (str) - a list of comma-separated dimensions
            sort=None (str) - a list of comma-separated dimensions and metrics indicating the sorting order and
            sorting direction for the returned data.
            filters=None (str) - dimension or metric filters that restrict the data returned for your request.
            segment=None (str) - segments the data returned for your request.
            sampling_level=None (str) - the desired sampling level. (DEFAULT /FASTER /HIGHER_PRECISION )
            start_index=None (int) - the first row of data to retrieve, starting at 1.
            Use this parameter as a pagination mechanism along with the max-results parameter.
            max_results=None (int) - the maximum number of rows to include in the response.
            output=None (str) - the desired output type for the Analytics data returned in the response (json/dataTable)
            fields=None (str) - selector specifying a subset of fields to include in the response

        Returns:
            The response returned from the Core Reporting API.
        """

        if self.profile_id is None:
            return None

        # Fill the parameters in dict
        params = {
            "ids": 'ga:' + self.profile_id,
            "start_date": date_from,
            "end_date": date_to,
            "metrics": metrics,
        }

        dimensions is not None and params.update({"dimensions": dimensions})
        sort is not None and params.update({"sort": sort})
        filters is not None and params.update({"filters": filters})
        segment is not None and params.update({"segment": segment})
        sampling_level is not None and params.update({"samplingLevel": sampling_level})
        start_index is not None and params.update({"start-index": start_index})
        max_results is not None and params.update({"max-results": max_results})
        output is not None and params.update({"output": output})
        fields is not None and params.update({"fields": fields})

        return self.service.data().ga().get(**params).execute()
