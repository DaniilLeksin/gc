__author__ = 'Daniil Leksin'
# -*- coding: utf-8 -*-

# ##########################################################################
##
##
##
##
###########################################################################

import wx

_ = wx.GetTranslation
import wx.propgrid as grid
from c_vacabular import *

###########################################################################
## Class main
###########################################################################


class Properties(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, wx.ID_ANY)

        self.panel = panel = wx.Panel(self, wx.ID_ANY)
        sz_main = wx.BoxSizer(wx.VERTICAL)
        self.property_grid = property_grid = \
            grid.PropertyGridManager(panel, style=grid.PG_SPLITTER_AUTO_CENTER)
        # Set column width
        self.property_grid.SetColumnProportion(1, 2)

        # Add properties
        # Create property page
        property_grid.AddPage("Properties")
        # Create dict for storing credentials
        self.dict_credentials = dict_credentials

        # Create first required group of properties - Client Parameters
        property_grid.Append(grid.PropertyCategory("01 - Client Parameters"))
        # Client ID: get from the api credentials
        property_grid.Append(grid.StringProperty("Client ID", value=wx.EmptyString))
        # Client secret: get from the api credentials. Keep it in secret (:
        property_grid.Append(grid.StringProperty("Client secret", value=wx.EmptyString))

        # Category of the required parameters except Metrics and ids
        # Metric are in individual category
        property_grid.Append(grid.PropertyCategory("02 - Required Parameters"))
        # Start date for fetching Analytics data
        property_grid.Append(grid.DateProperty("start-date", value=wx.DateTime_Now()))
        # End date for fetching Analytics data
        property_grid.Append(grid.DateProperty("end-date", value=wx.DateTime_Now()))

        # Not required property category
        property_grid.Append(grid.PropertyCategory("03 - Not Required Parameters"))
        # A list of comma-separated dimensions and metrics indicating the sorting order and
        # sorting direction for the returned data
        property_grid.Append(grid.StringProperty("sort", value=wx.EmptyString))
        # Dimension or metric filters that restrict the data returned for your request
        property_grid.Append(grid.StringProperty("filters", value=wx.EmptyString))
        # Segments the data returned for your request
        property_grid.Append(grid.StringProperty("segment", value=wx.EmptyString))
        # The desired sampling level. Allowed Values:
        #       DEFAULT — Returns response with a sample size that balances speed and accuracy.
        #       FASTER — Returns a fast response with a smaller sample size.
        #       HIGHER_PRECISION — Returns a more accurate response using a large sample size,
        #                           but this may result in the response being slower.
        property_grid.Append(grid.EnumProperty("samplingLevel", "samplingLevel",
                                               ['DEFAULT', 'FASTER', 'HIGHER_PRECISION'], [10, 11, 12], 0))
        # The first row of data to retrieve
        property_grid.Append(grid.StringProperty("start-index", value=wx.EmptyString))
        # The maximum number of rows to include in the response
        property_grid.Append(grid.StringProperty("max-results", value=wx.EmptyString))
        # Format of the outputs
        property_grid.Append(grid.EnumProperty("output", "output",
                                               ['json', 'dataTable'], [10, 11], 0))
        # Specifies which fields to return in a partial response.
        property_grid.Append(grid.StringProperty("fields", value=wx.EmptyString))
        # Returns the response in a human-readable format
        property_grid.Append(grid.BoolProperty("prettyPrint", value=True))
        property_grid.SetPropertyAttribute("prettyPrint", "UseCheckbox", True)
        # To enforce per-user quotas from a server-side application even in cases when the user's IP address is unknown.
        property_grid.Append(grid.StringProperty("quotaUser", value=wx.EmptyString))

        # Create big vac of metrics for work
        self.dict_api_properties = {"/": {}}

        # Create user dimensions and metrics category
        property_grid.Append(grid.PropertyCategory("04 - User"))
        # Create vac of the user dimensions and metrics
        # Vac format: ga:metrics/dimension: {
        #       "type": type_of_property,
        #       "view": dim/met,
        #       "html": path_to_html_info_page,
        #       "value": True/False}
        # Create properties for user metrics
        self._create_property(user_metrics)
        self.dict_api_properties["/"].update(user_metrics)

        # Create property category for session dimensions & metrics
        property_grid.Append(grid.PropertyCategory("05 - Session"))
        # Vac format: ga:metrics/dimension
        # Create properties for session metrics
        self._create_property(session_metrics)
        self.dict_api_properties["/"].update(session_metrics)

        # Create property category for Traffic Sources dimensions & metrics
        property_grid.Append(grid.PropertyCategory("06 - Traffic Sources"))
        # Create vac for Traffic sources
        # Create properties for Traffic sources metrics
        self._create_property(traffic_source_metrics)
        self.dict_api_properties["/"].update(traffic_source_metrics)

        # Create property category for Adwords dimensions & metrics
        property_grid.Append(grid.PropertyCategory("07 - Adwords"))
        # Create vac for Traffic sources
        self._create_property(adwords_metrics)
        self.dict_api_properties["/"].update(adwords_metrics)

        # Create property category for Goal Conversion dimensions & metrics
        property_grid.Append(grid.PropertyCategory("08 - Goal Conversion"))
        # Create vac for Goal Conversion
        self._create_property(goal_conversions_metrics)
        self.dict_api_properties["/"].update(goal_conversions_metrics)

        # Create property category for Platform & device dimensions & metrics
        property_grid.Append(grid.PropertyCategory("09 - Platform & device"))
        # Create vac for Platform & device
        self._create_property(platform_device_metrics)
        self.dict_api_properties["/"].update(platform_device_metrics)

        # Create property category for Geo Network dimensions & metrics
        property_grid.Append(grid.PropertyCategory("10 - Geo Network"))
        # Create vac for Geo Network
        self._create_property(geo_network_metrics)
        self.dict_api_properties["/"].update(geo_network_metrics)

        # Create property category for System dimensions & metrics
        property_grid.Append(grid.PropertyCategory("11 - System"))
        # Create vac for System
        self._create_property(system_metrics)
        self.dict_api_properties["/"].update(system_metrics)

        # Create property category for Social activities dimensions & metrics
        property_grid.Append(grid.PropertyCategory("12 - Social activities"))
        # Create vac for Social activities
        self._create_property(social_activities_metrics)
        self.dict_api_properties["/"].update(social_interaction_metrics)

       # Create property category for Page Tracking dimensions & metrics
        property_grid.Append(grid.PropertyCategory("13 - Page tracking"))
        # Create vac for Page Tracking
        self._create_property(page_tracking_metrics)
        self.dict_api_properties["/"].update(page_tracking_metrics)

        # Create property category for Content grouping dimensions & metrics
        property_grid.Append(grid.PropertyCategory("14 - Content grouping"))
        # Create vac for Content grouping
        self._create_property(content_grouping_metrics)
        self.dict_api_properties["/"].update(content_grouping_metrics)

        # Create property category for Internal search dimensions & metrics
        property_grid.Append(grid.PropertyCategory("15 - Internal search"))
        # Create vac for Internal search
        self._create_property(internal_search_metrics)
        self.dict_api_properties["/"].update(internal_search_metrics)

        # Create property category for Site speed dimensions & metrics
        property_grid.Append(grid.PropertyCategory("16 - Site speed"))
        # Create vac for Site speed
        self._create_property(site_speed_metrics)
        self.dict_api_properties["/"].update(site_speed_metrics)

        # Create property category for App tracking dimensions & metrics
        property_grid.Append(grid.PropertyCategory("17 - App tracking"))
        # Create vac for App tracking
        self._create_property(app_tracking_metrics)
        self.dict_api_properties["/"].update(app_tracking_metrics)

        # Create property category for Event tracking dimensions & metrics
        property_grid.Append(grid.PropertyCategory("18 - Event tracking"))
        # Create vac for Event tracking
        self._create_property(event_tracking_metrics)
        self.dict_api_properties["/"].update(event_tracking_metrics)

        # Create property category for Ecommerce dimensions & metrics
        property_grid.Append(grid.PropertyCategory("19 - Ecommerce"))
        # Create vac for Ecommerce
        self._create_property(ecommerce_metrics)
        self.dict_api_properties["/"].update(ecommerce_metrics)

        # Create property category for Social interaction dimensions & metrics
        property_grid.Append(grid.PropertyCategory("20 - Social interaction"))
        # Create vac for Social interaction
        self._create_property(social_interaction_metrics)
        self.dict_api_properties["/"].update(social_interaction_metrics)

        # Create property category for User timing dimensions & metrics
        property_grid.Append(grid.PropertyCategory("21 - User timing"))
        # Create vac for User timing
        self._create_property(user_timing_metrics)
        self.dict_api_properties["/"].update(user_timing_metrics)

        # Create property category for Exceptions dimensions & metrics
        property_grid.Append(grid.PropertyCategory("22 - Exceptions"))
        # Create vac for Exceptions
        self._create_property(exception_metrics)
        self.dict_api_properties["/"].update(exception_metrics)

        # Create property category for Content experiments dimensions & metrics
        property_grid.Append(grid.PropertyCategory("23 - Content experiments"))
        # Create vac for Content experiments
        self._create_property(content_experiments_metrics)
        self.dict_api_properties["/"].update(content_experiments_metrics)

        # Create property category for Custom variables dimensions & metrics
        property_grid.Append(grid.PropertyCategory("24 - Custom variables"))
        # Create vac for Custom variables
        self._create_property(custom_variables_columns_metrics)
        self.dict_api_properties["/"].update(custom_variables_columns_metrics)

        # Create property category for Time dimensions & metrics
        property_grid.Append(grid.PropertyCategory("25 - Time"))
        # Create vac for Time
        self._create_property(time_metrics)
        self.dict_api_properties["/"].update(time_metrics)

        # Create property category for Double click manager dimensions & metrics
        property_grid.Append(grid.PropertyCategory("25 - DoubleClick campaign manager"))
        # Create vac for Double click manager
        self._create_property(double_click_campaign_manager_metrics)
        self.dict_api_properties["/"].update(double_click_campaign_manager_metrics)

        # Create property category for Audience dimensions & metrics
        property_grid.Append(grid.PropertyCategory("26 - Audience"))
        # Create vac for Audience
        self._create_property(audience_metrics)
        self.dict_api_properties["/"].update(audience_metrics)

        # Create property category for Adsense dimensions & metrics
        property_grid.Append(grid.PropertyCategory("27 - Adsense"))
        # Create vac for Adsense
        self._create_property(adsense_metrics)
        self.dict_api_properties["/"].update(adsense_metrics)

        # Create property category for Channel grouping dimensions & metrics
        property_grid.Append(grid.PropertyCategory("28 - Channel grouping"))
        # Create vac for Channel grouping
        self._create_property(channel_grouping_metrics)
        self.dict_api_properties["/"].update(channel_grouping_metrics)

        # Create property category for Related products dimensions & metrics
        property_grid.Append(grid.PropertyCategory("29 - Related products"))
        # Create vac for Related products
        self._create_property(related_products_metrics)
        self.dict_api_properties["/"].update(related_products_metrics)

        # Embedding grid panel to the main sizer
        sz_main.Add(property_grid, 1, wx.EXPAND)
        panel.SetSizer(sz_main)
        sz_main.SetSizeHints(panel)

        # Fit the sizer
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(panel, 1, wx.EXPAND)
        self.SetSizer(sizer)
        self.SetAutoLayout(True)

        # Little piano in the bushes, to expand only useful/most popular property categories
        # Collapse all categories
        property_grid.CollapseAll()
        # expand categories that are needed
        property_grid.Expand("01 - Client Parameters")
        property_grid.Expand("02 - Required Parameters")

        # Binders, to connect events and handlers
        property_grid.Bind(grid.EVT_PG_CHANGED, self.on_property_grid_changed)
        property_grid.Bind(grid.EVT_PG_SELECTED, self.on_property_grid_select)

    def _create_property(self, metrics):
        """
        Put data to the grid
        :param metrics: vac of properties
        :return:
        """
        for ga_property in metrics:
            self.property_grid.Append(grid.BoolProperty(ga_property, value=False))
            self.property_grid.SetPropertyAttribute(ga_property, "UseCheckbox", True)
            if metrics[ga_property]["view"] == "Metrics":
                # TODO: create the background colour separation between dimensions and metrics
                pass
            else:
                # TODO: create the background colour separation between dimensions and metrics
                pass

    def on_property_grid_select(self, event):
        """
        hook the event on select any property in the grid
        :param event:
        """
        current_property = event.GetProperty()
        if current_property:
            try:
                print('%s selected\n' % (event.GetProperty().GetName()))
                html_path = self.dict_api_properties["/"][event.GetProperty().GetName()]["html"]
                self.GetTopLevelParent().set_html_page("html/%s" % html_path)
            except KeyError as error:
                print "No key found: %s" % str(error)   # TODO: to log
        else:
            print('Nothing selected\n')  # TODO: to log

    def on_property_grid_changed(self, event):
        """
        hook the event on making changes in any property in the grid
        :param event:
        """
        current_property = event.GetProperty().GetName()
        new_property_state = event.GetProperty().GetValue()
        # Change the value of the property
        self.dict_api_properties["/"][current_property]["value"] = new_property_state
        # TODO: change status bar
        # self.GetTopLevelParent().sb_status.SetValue("changed:%s" % event.GetProperty().GetName(), 0)
        # self.GetTopLevelParent().sb_status.refresh()
