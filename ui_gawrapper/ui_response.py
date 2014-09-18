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

###########################################################################
## Class main
###########################################################################


class Response(wx.Panel):
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
        self.property_grid.AddPage("Response")

        # Create response format group of properties - Client Parameters
        property_grid.Append(grid.PropertyCategory("Response"))

        # Embedding grid panel to the main sizer
        sz_main.Add(self.property_grid, 1, wx.EXPAND)
        panel.SetSizer(sz_main)
        sz_main.SetSizeHints(panel)

        # Fit the sizer
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(panel, 1, wx.EXPAND)
        self.SetSizer(sizer)
        self.SetAutoLayout(True)

    def add(self, response):
        try:
            if response.has_key("kind"): self.property_grid.Append(grid.StringProperty("kind", value=response["kind"]))
            if response.has_key("id"): self.property_grid.Append(grid.StringProperty("id", value=response["id"]))
            if response.has_key("selfLink"):self.property_grid.Append(grid.StringProperty("selfLink", value=response["selfLink"]))
            if response.has_key("containsSampledData"):self.property_grid.Append(grid.StringProperty("containsSampledData", value=str(response["containsSampledData"])))
            self.property_grid.Append(grid.PropertyCategory("query"))
            if response['query'].has_key("start-date"):self.property_grid.Append(grid.StringProperty("start-date", value=response["query"]["start-date"]))
            if response['query'].has_key("end-date"):self.property_grid.Append(grid.StringProperty("end-date", value=response["query"]["end-date"]))
            if response['query'].has_key("ids"):self.property_grid.Append(grid.StringProperty("ids", value=response["query"]["ids"]))
            if response['query'].has_key("dimensions"):self.property_grid.Append(grid.StringProperty("dimensions", value=response["query"]["dimensions"]))
            if response['query'].has_key("metrics"):self.property_grid.Append(grid.StringProperty("metrics", value=",".join(response["query"]["metrics"])))
            if response['query'].has_key("samplingLevel"):self.property_grid.Append(grid.StringProperty("samplingLevel", value=response["query"]["samplingLevel"]))
            if response['query'].has_key("sort"):self.property_grid.Append(grid.StringProperty("sort", value=",".join(response["query"]["sort"])))
            if response['query'].has_key("filters"):self.property_grid.Append(grid.StringProperty("filters", value=response["query"]["filters"]))
            if response['query'].has_key("segment"):self.property_grid.Append(grid.StringProperty("segment", value=response["query"]["segment"]))
            if response['query'].has_key("start-index"):self.property_grid.Append(grid.StringProperty("start-index", value=str(response["query"]["start-index"])))
            if response['query'].has_key("max-results"):self.property_grid.Append(grid.StringProperty("max-results", value=str(response["query"]["max-results"])))
            self.property_grid.Append(grid.PropertyCategory("response fields"))
            if response.has_key("itemsPerPage"):self.property_grid.Append(grid.StringProperty("itemsPerPage", value=str(response["itemsPerPage"])))
            if response.has_key("totalResults"):self.property_grid.Append(grid.StringProperty("totalResults", value=str(response["totalResults"])))
            if response.has_key("previousLink"):self.property_grid.Append(grid.StringProperty("previousLink", value=str(response["previousLink"])))
            if response.has_key("nextLink"):self.property_grid.Append(grid.StringProperty("nextLink", value=str(response["nextLink"])))
            if response.has_key("profileId"):self.property_grid.Append(grid.StringProperty("profileId", value=response["profileId"]))
            if response.has_key("accountId"):self.property_grid.Append(grid.StringProperty("accountId", value=response["accountId"]))
            if response.has_key("webPropertyId"):self.property_grid.Append(grid.StringProperty("webPropertyId", value=response["webPropertyId"]))
            if response.has_key("internalWebPropertyId"):self.property_grid.Append(grid.StringProperty("internalWebPropertyId", value=response["internalWebPropertyId"]))
            if response.has_key("profileName"):self.property_grid.Append(grid.StringProperty("profileName", value=response["profileName"]))
            if response.has_key("tableId"):self.property_grid.Append(grid.StringProperty("tableId", value=response["tableId"]))
            for index, header in enumerate(response["columnHeaders"]):
                self.property_grid.Append(grid.PropertyCategory("columnHeaders_%s" % index))
                self.property_grid.Append(grid.StringProperty(name="columnHeaders_%s_name" % index, label="columnHeaders", value=header["name"]))
                self.property_grid.Append(grid.StringProperty(name="columnHeaders_%s_columnType" % index, label="columnType", value=header["columnType"]))
                self.property_grid.Append(grid.StringProperty(name="columnHeaders_%s_dataType" % index, label="dataType", value=header["dataType"]))
            if response.has_key("dataTable"):
                # handle if used json table
                self.property_grid.Append(grid.PropertyCategory("dataTable"))
                for index, column in enumerate(response["dataTable"]["cols"]):
                    self.property_grid.Append(grid.PropertyCategory("column_%s" % index))
                    if header.has_key("id"):self.property_grid.Append(grid.StringProperty(name="column_%s_id" % index, label="id", value=header["id"]))
                    if header.has_key("label"):self.property_grid.Append(grid.StringProperty(name="column_%s_label" % index, label="label", value=header["label"]))
                    if header.has_key("type"):self.property_grid.Append(grid.StringProperty(name="column_%s_type" % index, label="type", value=header["type"]))
                for index, row in enumerate(response["dataTable"]["rows"]):
                    self.property_grid.Append(grid.PropertyCategory("row_%s" % index))
                    for index_c, c in enumerate(row):
                        self.property_grid.Append(grid.PropertyCategory("c_%s" % index_c))
                        if c.has_key("v"):self.property_grid.Append(grid.StringProperty("c_%s_v" % index_c, value=c["v"]))
            if response.has_key("sampleSize"):self.property_grid.Append(grid.StringProperty("sampleSize", value=response["sampleSize"]))
            if response.has_key("sampleSpace"):self.property_grid.Append(grid.StringProperty("sampleSpace", value=response["sampleSpace"]))
            self.property_grid.Append(grid.PropertyCategory("totalsForAllResults"))
            # Make it better
            if type(response["totalsForAllResults"]) is not dict:
                for index, result in enumerate(response["totalsForAllResults"]):
                    self.property_grid.Append(grid.PropertyCategory("result_%s" % index))
                    for metric in response["totalsForAllResults"].keys():
                        self.property_grid.Append(grid.StringProperty(name="%s_%s" % (metric, index), label=metric, value=response["totalsForAllResults"][result]))
            else:
                for index, result in enumerate(response["totalsForAllResults"]):
                    self.property_grid.Append(grid.StringProperty(name="%s_%s" % (result, index), label=result, value=response["totalsForAllResults"][result]))
        except KeyError as error:
            print str(error)
