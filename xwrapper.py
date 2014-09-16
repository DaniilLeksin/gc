__author__ = 'Daniil Leksin'
import sys, time, math, os, os.path

import wx

_ = wx.GetTranslation
import wx.propgrid as wxpg


class MemoDialog(wx.Dialog):
    """\
    Dialog for multi-line text editing.
    """

    def __init__(self, parent=None, title="", text="", pos=None, size=(500, 500)):
        wx.Dialog.__init__(self, parent, -1, title, style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER)

        topsizer = wx.BoxSizer(wx.VERTICAL)

        tc = wx.TextCtrl(self, 11, text, style=wx.TE_MULTILINE)
        self.tc = tc
        topsizer.Add(tc, 1, wx.EXPAND | wx.ALL, 8)

        rowsizer = wx.BoxSizer(wx.HORIZONTAL)
        rowsizer.Add(wx.Button(self, wx.ID_OK, 'Ok'), 0, wx.ALIGN_RIGHT | wx.ALIGN_CENTRE_VERTICAL, 8)
        rowsizer.Add((0, 0), 1, wx.ALIGN_RIGHT | wx.ALIGN_CENTRE_VERTICAL, 8)
        rowsizer.Add(wx.Button(self, wx.ID_CANCEL, 'Cancel'), 0, wx.ALIGN_RIGHT | wx.ALIGN_CENTRE_VERTICAL, 8)
        topsizer.Add(rowsizer, 0, wx.EXPAND | wx.ALL, 8)

        self.SetSizer(topsizer)
        topsizer.Layout()

        self.SetSize(size)
        if not pos:
            self.CenterOnScreen()
        else:
            self.Move(pos)


class ValueObject:
    def __init__(self):
        pass


class MyFrame1(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=wx.EmptyString, pos=wx.DefaultPosition,
                          size=wx.Size(500, 300), style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)

        self.SetSizeHintsSz(wx.DefaultSize, wx.DefaultSize)

        self.pan = TestPanel(self)
        self.Centre(wx.BOTH)

    def __del__(self):
        pass


# ###########################################################################
#
# MAIN PROPERTY GRID TEST PANEL
#
############################################################################


class TestPanel(wx.Panel):
    def __init__(self, parent, log=None):
        wx.Panel.__init__(self, parent, wx.ID_ANY)
        #self.log = log

        self.panel = panel = wx.Panel(self, wx.ID_ANY)
        topsizer = wx.BoxSizer(wx.VERTICAL)

        # Difference between using PropertyGridManager vs PropertyGrid is that
        # the manager supports multiple pages and a description box.
        self.pg = pg = wxpg.PropertyGridManager(panel, style=wxpg.PG_SPLITTER_AUTO_CENTER | wxpg.PG_AUTO_SORT |
                                                             wxpg.PG_TOOLBAR)

        # Show help as tooltips
        #pg.SetExtraStyle(wxpg.PG_EX_HELP_AS_TOOLTIPS)

        pg.Bind(wxpg.EVT_PG_CHANGED, self.OnPropGridChange)
        pg.Bind(wxpg.EVT_PG_PAGE_CHANGED, self.OnPropGridPageChange)
        pg.Bind(wxpg.EVT_PG_SELECTED, self.OnPropGridSelect)
        pg.Bind(wxpg.EVT_PG_RIGHT_CLICK, self.OnPropGridRightClick)

        #
        # Let's use some simple custom editor
        #
        # NOTE: Editor must be registered *before* adding a property that
        # uses it.
        # if not getattr(sys, '_PropGridEditorsRegistered', False):
        #     pg.RegisterEditor(TrivialPropertyEditor)
        #     pg.RegisterEditor(SampleMultiButtonEditor)
        #     pg.RegisterEditor(LargeImageEditor)
        #     # ensure we only do it once
        #     sys._PropGridEditorsRegistered = True

        #
        # Add properties
        #

        pg.AddPage("Properties")
        pg.Append(wxpg.PropertyCategory("01 - API properties"))
        pg.Append(wxpg.StringProperty("Client ID", value=wx.EmptyString))  # TODO: make masked ctrl
        pg.Append(wxpg.StringProperty("Client secret", value=wx.EmptyString))  # TODO: make masked ctrl
        pg.Append(wxpg.DateProperty("Date from", value=wx.DateTime_Now()))
        pg.Append(wxpg.DateProperty("Date to", value=wx.DateTime_Now()))
        pg.Append(wxpg.StringProperty("Sort", value=wx.EmptyString))
        pg.Append(wxpg.StringProperty("Filters", value=wx.EmptyString))

        pg.Append(wxpg.PropertyCategory("02 - User Dimensions & Metrics"))
        pg.Append(wxpg.BoolProperty("ga:userDefinedValue", value=False))
        pg.SetPropertyAttribute("ga:userDefinedValue", "UseCheckbox", True)
        pg.Append(wxpg.BoolProperty("ga:daysSinceLastSession", value=False))
        pg.SetPropertyAttribute("ga:daysSinceLastSession", "UseCheckbox", True)
        pg.Append(wxpg.BoolProperty("ga:sessionCount", value=False))
        pg.SetPropertyAttribute("ga:sessionCount", "UseCheckbox", True)
        pg.Append(wxpg.BoolProperty("ga:userType", value=False))
        pg.SetPropertyAttribute("ga:userType", "UseCheckbox", True)
        pg.Append(wxpg.BoolProperty("ga:percentNewSessions", value=False))
        pg.SetPropertyAttribute("ga:percentNewSessions", "UseCheckbox", True)
        pg.Append(wxpg.BoolProperty("ga:newUsers", value=False))
        pg.SetPropertyAttribute("ga:newUsers", "UseCheckbox", True)
        pg.Append(wxpg.BoolProperty("ga:users", value=False))
        pg.SetPropertyAttribute("ga:users", "UseCheckbox", True)

        pg.Append(wxpg.PropertyCategory("03 - Session Dimensions & Metrics"))
        pg.Append(wxpg.BoolProperty("ga:sessionDurationBucket", value=False))
        pg.SetPropertyAttribute("ga:sessionDurationBucket", "UseCheckbox", True)
        pg.Append(wxpg.BoolProperty("ga:sessions", value=False))
        pg.SetPropertyAttribute("ga:sessions", "UseCheckbox", True)
        pg.Append(wxpg.BoolProperty("ga:bounces", value=False))
        pg.SetPropertyAttribute("ga:bounces", "UseCheckbox", True)
        pg.Append(wxpg.BoolProperty("ga:bounceRate", value=False))
        pg.SetPropertyAttribute("ga:bounceRate", "UseCheckbox", True)
        pg.Append(wxpg.BoolProperty("ga:sessionDuration", value=False))
        pg.SetPropertyAttribute("ga:sessionDuration", "UseCheckbox", True)
        pg.Append(wxpg.BoolProperty("ga:avgSessionDuration", value=False))
        pg.SetPropertyAttribute("ga:avgSessionDuration", "UseCheckbox", True)
        pg.Append(wxpg.BoolProperty("ga:hits", value=False))
        pg.SetPropertyAttribute("ga:hits", "UseCheckbox", True)

        pg.Append(wxpg.PropertyCategory("04 - Traffic Sources Dimensions & Metrics"))
        pg.Append(wxpg.BoolProperty("ga:referralPath", value=False))
        pg.SetPropertyAttribute("ga:referralPath", "UseCheckbox", True)
        pg.Append(wxpg.BoolProperty("ga:fullReferrer", value=False))
        pg.SetPropertyAttribute("ga:fullReferrer", "UseCheckbox", True)
        pg.Append(wxpg.BoolProperty("ga:campaign", value=False))
        pg.SetPropertyAttribute("ga:campaign", "UseCheckbox", True)
        pg.Append(wxpg.BoolProperty("ga:source", value=False))
        pg.SetPropertyAttribute("ga:source", "UseCheckbox", True)
        pg.Append(wxpg.BoolProperty("ga:medium", value=False))
        pg.SetPropertyAttribute("ga:medium", "UseCheckbox", True)
        pg.Append(wxpg.BoolProperty("ga:sourceMedium", value=False))
        pg.SetPropertyAttribute("ga:sourceMedium", "UseCheckbox", True)
        pg.Append(wxpg.BoolProperty("ga:keyword", value=False))
        pg.SetPropertyAttribute("ga:keyword", "UseCheckbox", True)
        pg.Append(wxpg.BoolProperty("ga:adContent", value=False))
        pg.SetPropertyAttribute("ga:adContent", "UseCheckbox", True)
        pg.Append(wxpg.BoolProperty("ga:socialNetwork", value=False))
        pg.SetPropertyAttribute("ga:socialNetwork", "UseCheckbox", True)
        pg.Append(wxpg.BoolProperty("ga:hasSocialSourceReferral", value=False))
        pg.SetPropertyAttribute("ga:hasSocialSourceReferral", "UseCheckbox", True)
        pg.Append(wxpg.BoolProperty("ga:campaignCode", value=False))
        pg.SetPropertyAttribute("ga:campaignCode", "UseCheckbox", True)
        pg.Append(wxpg.BoolProperty("ga:organicSearches", value=False))
        pg.SetPropertyAttribute("ga:organicSearches", "UseCheckbox", True)

        pg.Append(wxpg.PropertyCategory("05 - Adwords Dimensions & Metrics"))
        pg.Append(wxpg.BoolProperty("ga:adGroup", value=False))
        pg.SetPropertyAttribute("ga:adGroup", "UseCheckbox", True)
        pg.Append(wxpg.BoolProperty("ga:adSlot", value=False))
        pg.SetPropertyAttribute("ga:adSlot", "UseCheckbox", True)
        pg.Append(wxpg.BoolProperty("ga:adSlotPosition", value=False))
        pg.SetPropertyAttribute("ga:adSlotPosition", "UseCheckbox", True)
        pg.Append(wxpg.BoolProperty("ga:adDistributionNetwork", value=False))
        pg.SetPropertyAttribute("ga:adDistributionNetwork", "UseCheckbox", True)
        pg.Append(wxpg.BoolProperty("ga:adMatchType", value=False))
        pg.SetPropertyAttribute("ga:adMatchType", "UseCheckbox", True)
        pg.Append(wxpg.BoolProperty("ga:adKeywordMatchType", value=False))
        pg.SetPropertyAttribute("ga:adKeywordMatchType", "UseCheckbox", True)
        pg.Append(wxpg.BoolProperty("ga:adMatchedQuery", value=False))
        pg.SetPropertyAttribute("ga:adMatchedQuery", "UseCheckbox", True)
        pg.Append(wxpg.BoolProperty("ga:adPlacementDomain", value=False))
        pg.SetPropertyAttribute("ga:adPlacementDomain", "UseCheckbox", True)
        pg.Append(wxpg.BoolProperty("ga:adPlacementUrl", value=False))
        pg.SetPropertyAttribute("ga:adPlacementUrl", "UseCheckbox", True)
        pg.Append(wxpg.BoolProperty("ga:adFormat", value=False))
        pg.SetPropertyAttribute("ga:adFormat", "UseCheckbox", True)
        pg.Append(wxpg.BoolProperty("ga:adTargetingType", value=False))
        pg.SetPropertyAttribute("ga:adTargetingType", "UseCheckbox", True)
        pg.Append(wxpg.BoolProperty("ga:adTargetingOption", value=False))
        pg.SetPropertyAttribute("ga:adTargetingOption", "UseCheckbox", True)
        pg.Append(wxpg.BoolProperty("ga:adDisplayUrl", value=False))
        pg.SetPropertyAttribute("ga:adDisplayUrl", "UseCheckbox", True)
        pg.Append(wxpg.BoolProperty("ga:adDestinationUrl", value=False))
        pg.SetPropertyAttribute("ga:adDestinationUrl", "UseCheckbox", True)
        pg.Append(wxpg.BoolProperty("ga:adwordsCustomerID", value=False))
        pg.SetPropertyAttribute("ga:adwordsCustomerID", "UseCheckbox", True)
        pg.Append(wxpg.BoolProperty("ga:adwordsCampaignID", value=False))
        pg.SetPropertyAttribute("ga:adwordsCampaignID", "UseCheckbox", True)
        pg.Append(wxpg.BoolProperty("ga:adwordsAdGroupID", value=False))
        pg.SetPropertyAttribute("ga:adwordsAdGroupID", "UseCheckbox", True)
        pg.Append(wxpg.BoolProperty("ga:adwordsCreativeID", value=False))
        pg.SetPropertyAttribute("ga:adwordsCreativeID", "UseCheckbox", True)
        pg.Append(wxpg.BoolProperty("ga:adwordsCriteriaID", value=False))
        pg.SetPropertyAttribute("ga:adwordsCriteriaID", "UseCheckbox", True)
        pg.Append(wxpg.BoolProperty("ga:isTrueViewVideoAd", value=False))
        pg.SetPropertyAttribute("ga:isTrueViewVideoAd", "UseCheckbox", True)
        pg.Append(wxpg.BoolProperty("ga:impressions", value=False))
        pg.SetPropertyAttribute("ga:impressions", "UseCheckbox", True)
        pg.Append(wxpg.BoolProperty("ga:adClicks", value=False))
        pg.SetPropertyAttribute("ga:adClicks", "UseCheckbox", True)
        pg.Append(wxpg.BoolProperty("ga:adCost", value=False))
        pg.SetPropertyAttribute("ga:adCost", "UseCheckbox", True)
        pg.Append(wxpg.BoolProperty("ga:CPM", value=False))
        pg.SetPropertyAttribute("ga:CPM", "UseCheckbox", True)
        pg.Append(wxpg.BoolProperty("ga:CPC", value=False))
        pg.SetPropertyAttribute("ga:CPC", "UseCheckbox", True)
        pg.Append(wxpg.BoolProperty("ga:CTR", value=False))
        pg.SetPropertyAttribute("ga:CTR", "UseCheckbox", True)
        pg.Append(wxpg.BoolProperty("ga:costPerTransaction", value=False))
        pg.SetPropertyAttribute("ga:costPerTransaction", "UseCheckbox", True)
        pg.Append(wxpg.BoolProperty("ga:costPerGoalConversion", value=False))
        pg.SetPropertyAttribute("ga:costPerGoalConversion", "UseCheckbox", True)
        pg.Append(wxpg.BoolProperty("ga:costPerConversion", value=False))
        pg.SetPropertyAttribute("ga:costPerConversion", "UseCheckbox", True)
        pg.Append(wxpg.BoolProperty("ga:RPC", value=False))
        pg.SetPropertyAttribute("ga:RPC", "UseCheckbox", True)
        pg.Append(wxpg.BoolProperty("ga:ROI", value=False))
        pg.SetPropertyAttribute("ga:ROI", "UseCheckbox", True)
        pg.Append(wxpg.BoolProperty("ga:margin", value=False))
        pg.SetPropertyAttribute("ga:margin", "UseCheckbox", True)

        pg.Append(wxpg.PropertyCategory("06 - Goal Conversions Dimensions & Metrics"))
        pg.Append(wxpg.BoolProperty("ga:goalCompletionLocation", value=False))
        pg.SetPropertyAttribute("ga:goalCompletionLocation", "UseCheckbox", True)
        pg.Append(wxpg.BoolProperty("ga:goalPreviousStep1", value=False))
        pg.SetPropertyAttribute("ga:goalPreviousStep1", "UseCheckbox", True)
        pg.Append(wxpg.BoolProperty("ga:goalPreviousStep2", value=False))
        pg.SetPropertyAttribute("ga:goalPreviousStep2", "UseCheckbox", True)
        pg.Append(wxpg.BoolProperty("ga:goalPreviousStep3", value=False))
        pg.SetPropertyAttribute("ga:goalPreviousStep3", "UseCheckbox", True)
        pg.Append(wxpg.BoolProperty("ga:goalXXStarts", value=False))
        pg.SetPropertyAttribute("ga:goalXXStarts", "UseCheckbox", True)
        pg.Append(wxpg.BoolProperty("ga:goalStartsAll", value=False))
        pg.SetPropertyAttribute("ga:goalStartsAll", "UseCheckbox", True)
        pg.Append(wxpg.BoolProperty("ga:goalXXCompletions", value=False))
        pg.SetPropertyAttribute("ga:goalXXCompletions", "UseCheckbox", True)
        pg.Append(wxpg.BoolProperty("ga:goalCompletionsAll", value=False))
        pg.SetPropertyAttribute("ga:goalCompletionsAll", "UseCheckbox", True)
        pg.Append(wxpg.BoolProperty("ga:goalXXValue", value=False))
        pg.SetPropertyAttribute("ga:goalXXValue", "UseCheckbox", True)
        pg.Append(wxpg.BoolProperty("ga:goalValueAll", value=False))
        pg.SetPropertyAttribute("ga:goalValueAll", "UseCheckbox", True)
        pg.Append(wxpg.BoolProperty("ga:goalValuePerSession", value=False))
        pg.SetPropertyAttribute("ga:goalValuePerSession", "UseCheckbox", True)
        pg.Append(wxpg.BoolProperty("ga:goalXXConversionRate", value=False))
        pg.SetPropertyAttribute("ga:goalXXConversionRate", "UseCheckbox", True)
        pg.Append(wxpg.BoolProperty("ga:goalConversionRateAll", value=False))
        pg.SetPropertyAttribute("ga:goalConversionRateAll", "UseCheckbox", True)
        pg.Append(wxpg.BoolProperty("ga:goalXXAbandons", value=False))
        pg.SetPropertyAttribute("ga:goalXXAbandons", "UseCheckbox", True)
        pg.Append(wxpg.BoolProperty("ga:goalAbandonsAll", value=False))
        pg.SetPropertyAttribute("ga:goalAbandonsAll", "UseCheckbox", True)
        pg.Append(wxpg.BoolProperty("ga:goalXXAbandonRate", value=False))
        pg.SetPropertyAttribute("ga:goalXXAbandonRate", "UseCheckbox", True)
        pg.Append(wxpg.BoolProperty("ga:goalAbandonRateAll", value=False))
        pg.SetPropertyAttribute("ga:goalAbandonRateAll", "UseCheckbox", True)

        pg.Append(wxpg.PropertyCategory("07 - Platform or Device Dimensions & Metrics"))
        pg.Append(wxpg.BoolProperty("ga:browser", value=True))
        pg.SetPropertyAttribute("ga:browser", "UseCheckbox", True)
        pg.Append(wxpg.BoolProperty("ga:browserVersion", value=False))
        pg.SetPropertyAttribute("ga:browserVersion", "UseCheckbox", True)
        pg.Append(wxpg.BoolProperty("ga:operatingSystem", value=False))
        pg.SetPropertyAttribute("ga:operatingSystem", "UseCheckbox", True)
        pg.Append(wxpg.BoolProperty("ga:operatingSystemVersion", value=False))
        pg.SetPropertyAttribute("ga:operatingSystemVersion", "UseCheckbox", True)
        pg.Append(wxpg.BoolProperty("ga:mobileDeviceBranding", value=False))
        pg.SetPropertyAttribute("ga:mobileDeviceBranding", "UseCheckbox", True)
        pg.Append(wxpg.BoolProperty("ga:mobileDeviceModel", value=False))
        pg.SetPropertyAttribute("ga:mobileDeviceModel", "UseCheckbox", True)
        pg.Append(wxpg.BoolProperty("ga:mobileInputSelector", value=False))
        pg.SetPropertyAttribute("ga:mobileInputSelector", "UseCheckbox", True)
        pg.Append(wxpg.BoolProperty("ga:mobileDeviceInfo", value=False))
        pg.SetPropertyAttribute("ga:mobileDeviceInfo", "UseCheckbox", True)
        pg.Append(wxpg.BoolProperty("ga:mobileDeviceMarketingName", value=False))
        pg.SetPropertyAttribute("ga:mobileDeviceMarketingName", "UseCheckbox", True)
        pg.Append(wxpg.BoolProperty("ga:deviceCategory", value=False))
        pg.SetPropertyAttribute("ga:deviceCategory", "UseCheckbox", True)

        pg.Append(wxpg.PropertyCategory("08 - Geo Network Dimensions & Metrics"))
        pg.Append(wxpg.BoolProperty("ga:continent", value=False))
        pg.SetPropertyAttribute("ga:continent", "UseCheckbox", True)
        pg.Append(wxpg.BoolProperty("ga:subContinent", value=False))
        pg.SetPropertyAttribute("ga:subContinent", "UseCheckbox", True)
        pg.Append(wxpg.BoolProperty("ga:country", value=True))
        pg.SetPropertyAttribute("ga:country", "UseCheckbox", True)
        pg.Append(wxpg.BoolProperty("ga:region", value=False))
        pg.SetPropertyAttribute("ga:region", "UseCheckbox", True)
        pg.Append(wxpg.BoolProperty("ga:metro", value=False))
        pg.SetPropertyAttribute("ga:metro", "UseCheckbox", True)
        pg.Append(wxpg.BoolProperty("ga:city", value=False))
        pg.SetPropertyAttribute("ga:city", "UseCheckbox", True)
        pg.Append(wxpg.BoolProperty("ga:latitude", value=False))
        pg.SetPropertyAttribute("ga:latitude", "UseCheckbox", True)
        pg.Append(wxpg.BoolProperty("ga:longitude", value=False))
        pg.SetPropertyAttribute("ga:longitude", "UseCheckbox", True)
        pg.Append(wxpg.BoolProperty("ga:networkDomain", value=False))
        pg.SetPropertyAttribute("ga:networkDomain", "UseCheckbox", True)
        pg.Append(wxpg.BoolProperty("ga:networkLocation", value=False))
        pg.SetPropertyAttribute("ga:networkLocation", "UseCheckbox", True)

        pg.Append(wxpg.PropertyCategory("09 - System Dimensions & Metrics"))
        pg.Append(wxpg.BoolProperty("ga:flashVersion", value=False))
        pg.SetPropertyAttribute("ga:flashVersion", "UseCheckbox", True)
        pg.Append(wxpg.BoolProperty("ga:javaEnabled", value=False))
        pg.SetPropertyAttribute("ga:javaEnabled", "UseCheckbox", True)
        pg.Append(wxpg.BoolProperty("ga:language", value=False))
        pg.SetPropertyAttribute("ga:language", "UseCheckbox", True)
        pg.Append(wxpg.BoolProperty("ga:screenColors", value=False))
        pg.SetPropertyAttribute("ga:screenColors", "UseCheckbox", True)
        pg.Append(wxpg.BoolProperty("ga:sourcePropertyDisplayName", value=False))
        pg.SetPropertyAttribute("ga:sourcePropertyDisplayName", "UseCheckbox", True)
        pg.Append(wxpg.BoolProperty("ga:sourcePropertyTrackingId", value=False))
        pg.SetPropertyAttribute("ga:sourcePropertyTrackingId", "UseCheckbox", True)
        pg.Append(wxpg.BoolProperty("ga:screenResolution", value=False))
        pg.SetPropertyAttribute("ga:screenResolution", "UseCheckbox", True)

        pg.Append(wxpg.PropertyCategory("10 - Social Activities Dimensions & Metrics"))
        pg.Append(wxpg.BoolProperty("ga:socialActivityEndorsingUrl", value=False))
        pg.SetPropertyAttribute("ga:socialActivityEndorsingUrl", "UseCheckbox", True)
        pg.Append(wxpg.BoolProperty("ga:socialActivityDisplayName", value=False))
        pg.SetPropertyAttribute("ga:socialActivityDisplayName", "UseCheckbox", True)
        pg.Append(wxpg.BoolProperty("ga:socialActivityPost", value=False))
        pg.SetPropertyAttribute("ga:socialActivityPost", "UseCheckbox", True)
        pg.Append(wxpg.BoolProperty("ga:socialActivityTimestamp", value=False))
        pg.SetPropertyAttribute("ga:socialActivityTimestamp", "UseCheckbox", True)
        pg.Append(wxpg.BoolProperty("ga:socialActivityUserHandle", value=False))
        pg.SetPropertyAttribute("ga:socialActivityUserHandle", "UseCheckbox", True)
        pg.Append(wxpg.BoolProperty("ga:socialActivityUserPhotoUrl", value=False))
        pg.SetPropertyAttribute("ga:socialActivityUserPhotoUrl", "UseCheckbox", True)
        pg.Append(wxpg.BoolProperty("ga:socialActivityUserProfileUrl", value=False))
        pg.SetPropertyAttribute("ga:socialActivityUserProfileUrl", "UseCheckbox", True)
        pg.Append(wxpg.BoolProperty("ga:socialActivityContentUrl", value=False))
        pg.SetPropertyAttribute("ga:socialActivityContentUrl", "UseCheckbox", True)
        pg.Append(wxpg.BoolProperty("ga:socialActivityTagsSummary", value=False))
        pg.SetPropertyAttribute("ga:socialActivityTagsSummary", "UseCheckbox", True)
        pg.Append(wxpg.BoolProperty("ga:socialActivityAction", value=False))
        pg.SetPropertyAttribute("ga:socialActivityAction", "UseCheckbox", True)
        pg.Append(wxpg.BoolProperty("ga:socialActivityNetworkAction", value=False))
        pg.SetPropertyAttribute("ga:socialActivityNetworkAction", "UseCheckbox", True)
        pg.Append(wxpg.BoolProperty("ga:socialActivities", value=False))
        pg.SetPropertyAttribute("ga:socialActivities", "UseCheckbox", True)

        pg.Append(wxpg.PropertyCategory("11 - Page Tracking Dimensions & Metrics"))
        pg.Append(wxpg.BoolProperty("ga:hostname", value=False))
        pg.SetPropertyAttribute("ga:hostname", "UseCheckbox", True)
        pg.Append(wxpg.BoolProperty("ga:pagePath", value=False))
        pg.SetPropertyAttribute("ga:pagePath", "UseCheckbox", True)
        pg.Append(wxpg.BoolProperty("ga:pagePathLevel1", value=False))
        pg.SetPropertyAttribute("ga:pagePathLevel1", "UseCheckbox", True)
        pg.Append(wxpg.BoolProperty("ga:pagePathLevel2", value=False))
        pg.SetPropertyAttribute("ga:pagePathLevel2", "UseCheckbox", True)
        pg.Append(wxpg.BoolProperty("ga:pagePathLevel3", value=False))
        pg.SetPropertyAttribute("ga:pagePathLevel3", "UseCheckbox", True)
        pg.Append(wxpg.BoolProperty("ga:pagePathLevel4", value=False))
        pg.SetPropertyAttribute("ga:pagePathLevel4", "UseCheckbox", True)
        pg.Append(wxpg.BoolProperty("ga:pageTitle", value=False))
        pg.SetPropertyAttribute("ga:pageTitle", "UseCheckbox", True)
        pg.Append(wxpg.BoolProperty("ga:landingPagePath", value=False))
        pg.SetPropertyAttribute("ga:landingPagePath", "UseCheckbox", True)
        pg.Append(wxpg.BoolProperty("ga:secondPagePath", value=False))
        pg.SetPropertyAttribute("ga:secondPagePath", "UseCheckbox", True)
        pg.Append(wxpg.BoolProperty("ga:exitPagePath", value=False))
        pg.SetPropertyAttribute("ga:exitPagePath", "UseCheckbox", True)
        pg.Append(wxpg.BoolProperty("ga:previousPagePath", value=False))
        pg.SetPropertyAttribute("ga:previousPagePath", "UseCheckbox", True)
        pg.Append(wxpg.BoolProperty("ga:nextPagePath", value=False))
        pg.SetPropertyAttribute("ga:nextPagePath", "UseCheckbox", True)
        pg.Append(wxpg.BoolProperty("ga:pageDepth", value=False))
        pg.SetPropertyAttribute("ga:pageDepth", "UseCheckbox", True)
        pg.Append(wxpg.BoolProperty("ga:pageValue", value=False))
        pg.SetPropertyAttribute("ga:pageValue", "UseCheckbox", True)
        pg.Append(wxpg.BoolProperty("ga:entrances", value=False))
        pg.SetPropertyAttribute("ga:entrances", "UseCheckbox", True)
        pg.Append(wxpg.BoolProperty("ga:entranceRate", value=False))
        pg.SetPropertyAttribute("ga:entranceRate", "UseCheckbox", True)
        pg.Append(wxpg.BoolProperty("ga:pageviews", value=False))
        pg.SetPropertyAttribute("ga:pageviews", "UseCheckbox", True)
        pg.Append(wxpg.BoolProperty("ga:pageviewsPerSession", value=False))
        pg.SetPropertyAttribute("ga:pageviewsPerSession", "UseCheckbox", True)
        pg.Append(wxpg.BoolProperty("ga:uniquePageviews", value=False))
        pg.SetPropertyAttribute("ga:uniquePageviews", "UseCheckbox", True)
        pg.Append(wxpg.BoolProperty("ga:timeOnPage", value=False))
        pg.SetPropertyAttribute("ga:timeOnPage", "UseCheckbox", True)
        pg.Append(wxpg.BoolProperty("ga:avgTimeOnPage", value=False))
        pg.SetPropertyAttribute("ga:avgTimeOnPage", "UseCheckbox", True)
        pg.Append(wxpg.BoolProperty("ga:exits", value=False))
        pg.SetPropertyAttribute("ga:exits", "UseCheckbox", True)
        pg.Append(wxpg.BoolProperty("ga:exitRate", value=False))
        pg.SetPropertyAttribute("ga:exitRate", "UseCheckbox", True)

        pg.Append(wxpg.PropertyCategory("12 - SContent Grouping Dimensions & Metrics"))
        pg.Append(wxpg.BoolProperty("ga:landingContentGroupXX", value=False))
        pg.SetPropertyAttribute("ga:landingContentGroupXX", "UseCheckbox", True)
        pg.Append(wxpg.BoolProperty("ga:previousContentGroupXX", value=False))
        pg.SetPropertyAttribute("ga:previousContentGroupXX", "UseCheckbox", True)
        pg.Append(wxpg.BoolProperty("ga:contentGroupXX", value=False))
        pg.SetPropertyAttribute("ga:contentGroupXX", "UseCheckbox", True)
        pg.Append(wxpg.BoolProperty("ga:nextContentGroupXX", value=False))
        pg.SetPropertyAttribute("ga:nextContentGroupXX", "UseCheckbox", True)
        pg.Append(wxpg.BoolProperty("ga:contentGroupUniqueViewsXX", value=False))
        pg.SetPropertyAttribute("ga:contentGroupUniqueViewsXX", "UseCheckbox", True)

        pg.Append(wxpg.PropertyCategory("13 - Internal Search Dimensions & Metrics"))
        pg.Append(wxpg.BoolProperty("ga:searchUsed", value=False))
        pg.SetPropertyAttribute("ga:searchUsed", "UseCheckbox", True)
        pg.Append(wxpg.BoolProperty("ga:searchKeyword", value=False))
        pg.SetPropertyAttribute("ga:searchKeyword", "UseCheckbox", True)
        pg.Append(wxpg.BoolProperty("ga:searchKeywordRefinement", value=False))
        pg.SetPropertyAttribute("ga:searchKeywordRefinement", "UseCheckbox", True)
        pg.Append(wxpg.BoolProperty("ga:searchCategory", value=False))
        pg.SetPropertyAttribute("ga:searchCategory", "UseCheckbox", True)
        pg.Append(wxpg.BoolProperty("ga:searchStartPage", value=False))
        pg.SetPropertyAttribute("ga:searchStartPage", "UseCheckbox", True)
        pg.Append(wxpg.BoolProperty("ga:searchDestinationPage", value=False))
        pg.SetPropertyAttribute("ga:searchDestinationPage", "UseCheckbox", True)
        pg.Append(wxpg.BoolProperty("ga:searchResultViews", value=False))
        pg.SetPropertyAttribute("ga:searchResultViews", "UseCheckbox", True)
        pg.Append(wxpg.BoolProperty("ga:searchUniques", value=False))
        pg.SetPropertyAttribute("ga:searchUniques", "UseCheckbox", True)
        pg.Append(wxpg.BoolProperty("ga:avgSearchResultViews", value=False))
        pg.SetPropertyAttribute("ga:avgSearchResultViews", "UseCheckbox", True)
        pg.Append(wxpg.BoolProperty("ga:searchSessions", value=False))
        pg.SetPropertyAttribute("ga:searchSessions", "UseCheckbox", True)
        pg.Append(wxpg.BoolProperty("ga:percentSessionsWithSearch", value=False))
        pg.SetPropertyAttribute("ga:percentSessionsWithSearch", "UseCheckbox", True)
        pg.Append(wxpg.BoolProperty("ga:searchDepth", value=False))
        pg.SetPropertyAttribute("ga:searchDepth", "UseCheckbox", True)
        pg.Append(wxpg.BoolProperty("ga:avgSearchDepth", value=False))
        pg.SetPropertyAttribute("ga:avgSearchDepth", "UseCheckbox", True)
        pg.Append(wxpg.BoolProperty("ga:searchRefinements", value=False))
        pg.SetPropertyAttribute("ga:searchRefinements", "UseCheckbox", True)
        pg.Append(wxpg.BoolProperty("ga:percentSearchRefinements", value=False))
        pg.SetPropertyAttribute("ga:percentSearchRefinements", "UseCheckbox", True)
        pg.Append(wxpg.BoolProperty("ga:searchDuration", value=False))
        pg.SetPropertyAttribute("ga:searchDuration", "UseCheckbox", True)
        pg.Append(wxpg.BoolProperty("ga:avgSearchDuration", value=False))
        pg.SetPropertyAttribute("ga:avgSearchDuration", "UseCheckbox", True)
        pg.Append(wxpg.BoolProperty("ga:searchExits", value=False))
        pg.SetPropertyAttribute("ga:searchExits", "UseCheckbox", True)
        pg.Append(wxpg.BoolProperty("ga:searchExitRate", value=False))
        pg.SetPropertyAttribute("ga:searchExitRate", "UseCheckbox", True)
        pg.Append(wxpg.BoolProperty("ga:searchGoalConversionRateAll", value=False))
        pg.SetPropertyAttribute("ga:searchGoalConversionRateAll", "UseCheckbox", True)
        pg.Append(wxpg.BoolProperty("ga:goalValueAllPerSearch", value=False))
        pg.SetPropertyAttribute("ga:goalValueAllPerSearch", "UseCheckbox", True)

        pg.Append(wxpg.PropertyCategory("14 - Site Speed Dimensions & Metrics"))
        lst = ["ga:pageLoadTime", "ga:pageLoadSample", "ga:avgPageLoadTime", "ga:domainLookupTime",
               "ga:avgDomainLookupTime", "ga:pageDownloadTime", "ga:avgPageDownloadTime", "ga:redirectionTime",
               "ga:avgRedirectionTime", "ga:serverConnectionTime", "ga:avgServerConnectionTime",
               "ga:serverResponseTime", "ga:avgServerResponseTime", "ga:speedMetricsSample", "ga:domInteractiveTime",
               "ga:avgDomInteractiveTime", "ga:domContentLoadedTime", "ga:avgDomContentLoadedTime",
               "ga:domLatencyMetricsSample"]
        for name in lst:
            pg.Append(wxpg.BoolProperty(name, value=False))
            pg.SetPropertyAttribute(name, "UseCheckbox", True)

        pg.Append(wxpg.PropertyCategory("15 - App Tracking Dimensions & Metrics"))
        lst = ["ga:appInstallerId", "ga:appVersion", "ga:appName", "ga:appId", "ga:screenName", "ga:screenDepth",
               "ga:landingScreenName", "ga:exitScreenName", "ga:screenviews", "ga:uniqueScreenviews",
               "ga:screenviewsPerSession", "ga:timeOnScreen", "ga:avgScreenviewDuration"]
        for name in lst:
            pg.Append(wxpg.BoolProperty(name, value=False))
            pg.SetPropertyAttribute(name, "UseCheckbox", True)

        pg.Append(wxpg.PropertyCategory("16 - Event Tracking Dimensions & Metrics"))
        lst = ["ga:eventCategory", "ga:eventAction", "ga:eventLabel", "ga:totalEvents", "ga:uniqueEvents",
               "ga:eventValue", "ga:avgEventValue", "ga:sessionsWithEvent", "ga:eventsPerSessionWithEvent"]
        for name in lst:
            pg.Append(wxpg.BoolProperty(name, value=False))
            pg.SetPropertyAttribute(name, "UseCheckbox", True)

        pg.Append(wxpg.PropertyCategory("17 - Ecommerce Dimensions & Metrics"))
        lst = ["ga:transactionId", "ga:affiliation", "ga:sessionsToTransaction", "ga:daysToTransaction",
               "ga:productSku", "ga:productName", "ga:productCategory", "ga:currencyCode", "ga:checkoutOptions",
               "ga:internalPromotionCreative", "ga:internalPromotionId",
               "ga:internalPromotionName", "ga:internalPromotionPosition", "ga:orderCouponCode", "ga:productBrand",
               "ga:productCategoryHierarchy", "ga:productCategoryLevelXX", "ga:productCouponCode", "ga:productListName",
               "ga:productListPosition", "ga:productVariant", "ga:shoppingStage", "ga:transactions",
               "ga:transactionsPerSession", "ga:transactionRevenue", "ga:revenuePerTransaction",
               "ga:transactionRevenuePerSession", "ga:transactionShipping", "ga:transactionTax", "ga:totalValue",
               "ga:itemQuantity", "ga:uniquePurchases", "ga:revenuePerItem", "ga:itemRevenue", "ga:itemsPerPurchase",
               "ga:localTransactionRevenue", "ga:localTransactionShipping", "ga:localTransactionTax",
               "ga:localItemRevenue", "ga:buyToDetailRate", "ga:cartToDetailRate", "ga:internalPromotionCTR",
               "ga:internalPromotionClicks", "ga:internalPromotionViews", "ga:localProductRefundAmount",
               "ga:localRefundAmount", "ga:productAddsToCart", "ga:productCheckouts", "ga:productDetailViews",
               "ga:productListCTR", "ga:productListClicks", "ga:productListViews", "ga:productRefundAmount",
               "ga:productRefunds", "ga:productRemovesFromCart", "ga:productRevenuePerPurchase",
               "ga:quantityAddedToCart", "ga:quantityCheckedOut", "ga:quantityRefunded", "ga:quantityRemovedFromCart",
               "ga:refundAmount", "ga:totalRefunds"]
        for name in lst:
            pg.Append(wxpg.BoolProperty(name, value=False))
            pg.SetPropertyAttribute(name, "UseCheckbox", True)

        pg.Append(wxpg.PropertyCategory("18 - Social Interactions Dimensions & Metrics"))
        lst = ["ga:socialInteractionNetwork", "ga:socialInteractionAction", "ga:socialInteractionNetworkAction",
               "ga:socialInteractionTarget", "ga:socialEngagementType", "ga:socialInteractions",
               "ga:uniqueSocialInteractions", "ga:socialInteractionsPerSession"]
        for name in lst:
            pg.Append(wxpg.BoolProperty(name, value=False))
            pg.SetPropertyAttribute(name, "UseCheckbox", True)

        pg.Append(wxpg.PropertyCategory("19 - User Timings Dimensions & Metrics"))
        lst = ["ga:userTimingCategory", "ga:userTimingLabel", "ga:userTimingVariable", "ga:userTimingValue",
               "ga:userTimingSample", "ga:avgUserTimingValue"]
        for name in lst:
            pg.Append(wxpg.BoolProperty(name, value=False))
            pg.SetPropertyAttribute(name, "UseCheckbox", True)

        pg.Append(wxpg.PropertyCategory("20 - Exceptions Dimensions & Metrics"))
        lst = ["ga:exceptionDescription", "ga:exceptions", "ga:exceptionsPerScreenview", "ga:fatalExceptions",
               "ga:fatalExceptionsPerScreenview"]
        for name in lst:
            pg.Append(wxpg.BoolProperty(name, value=False))
            pg.SetPropertyAttribute(name, "UseCheckbox", True)

        pg.Append(wxpg.PropertyCategory("21 - Content Experiments Dimensions & Metrics"))
        lst = ["ga:experimentId", "ga:experimentVariant"]
        for name in lst:
            pg.Append(wxpg.BoolProperty(name, value=False))
            pg.SetPropertyAttribute(name, "UseCheckbox", True)

        pg.Append(wxpg.PropertyCategory("22 - Custom Variables or Columns Dimensions & Metrics"))
        lst = ["ga:dimensionXX", "ga:customVarNameXX", "ga:customVarValueXX", "ga:metricXX"]
        for name in lst:
            pg.Append(wxpg.BoolProperty(name, value=False))
            pg.SetPropertyAttribute(name, "UseCheckbox", True)

        pg.Append(wxpg.PropertyCategory("23 - Time Dimensions & Metrics"))
        lst = ["ga:date", "ga:year", "ga:month", "ga:week", "ga:day", "ga:hour", "ga:minute", "ga:nthMonth",
               "ga:nthWeek", "ga:nthDay", "ga:nthMinute", "ga:dayOfWeek", "ga:dayOfWeekName", "ga:dateHour",
               "ga:yearMonth", "ga:yearWeek", "ga:isoWeek", "ga:isoYear", "ga:isoYearIsoWeek", "ga:nthHour"]
        for name in lst:
            pg.Append(wxpg.BoolProperty(name, value=False))
            pg.SetPropertyAttribute(name, "UseCheckbox", True)

        pg.Append(wxpg.PropertyCategory("24 - DoubleClick Campaign Manager Dimensions & Metrics"))
        lst = ["ga:dcmClickAd", "ga:dcmClickAdId", "ga:dcmClickAdType", "ga:dcmClickAdTypeId", "ga:dcmClickAdvertiser",
               "ga:dcmClickAdvertiserId", "ga:dcmClickCampaign", "ga:dcmClickCampaignId", "ga:dcmClickCreativeId",
               "ga:dcmClickCreative", "ga:dcmClickRenderingId", "ga:dcmClickCreativeType", "ga:dcmClickCreativeTypeId",
               "ga:dcmClickCreativeVersion", "ga:dcmClickSite", "ga:dcmClickSiteId", "ga:dcmClickSitePlacement",
               "ga:dcmClickSitePlacementId", "ga:dcmClickSpotId", "ga:dcmFloodlightActivity",
               "ga:dcmFloodlightActivityAndGroup", "ga:dcmFloodlightActivityGroup", "ga:dcmFloodlightActivityGroupId",
               "ga:dcmFloodlightActivityId", "ga:dcmFloodlightAdvertiserId", "ga:dcmFloodlightSpotId",
               "ga:dcmLastEventAd", "ga:dcmLastEventAdId", "ga:dcmLastEventAdType", "ga:dcmLastEventAdTypeId",
               "ga:dcmLastEventAdvertiser", "ga:dcmLastEventAdvertiserId", "ga:dcmLastEventAttributionType",
               "ga:dcmLastEventCampaign", "ga:dcmLastEventCampaignId", "ga:dcmLastEventCreativeId",
               "ga:dcmLastEventCreative", "ga:dcmLastEventRenderingId", "ga:dcmLastEventCreativeType",
               "ga:dcmLastEventCreativeTypeId", "ga:dcmLastEventCreativeVersion", "ga:dcmLastEventSite",
               "ga:dcmLastEventSiteId", "ga:dcmLastEventSitePlacement", "ga:dcmLastEventSitePlacementId",
               "ga:dcmLastEventSpotId", "ga:dcmFloodlightQuantity", "ga:dcmFloodlightRevenue", "ga:dcmCPC", "ga:dcmCTR",
               "ga:dcmClicks", "ga:dcmCost", "ga:dcmImpressions", "ga:dcmMargin", "ga:dcmROI", "ga:dcmRPC"]
        for name in lst:
            pg.Append(wxpg.BoolProperty(name, value=False))
            pg.SetPropertyAttribute(name, "UseCheckbox", True)

        pg.Append(wxpg.PropertyCategory("25 - Audience Dimensions & Metrics"))
        lst = ["ga:userAgeBracket", "ga:userGender", "ga:interestOtherCategory", "ga:interestAffinityCategory",
               "ga:interestInMarketCategory"]
        for name in lst:
            pg.Append(wxpg.BoolProperty(name, value=False))
            pg.SetPropertyAttribute(name, "UseCheckbox", True)


        pg.Append(wxpg.PropertyCategory("26 - Adsense Dimensions & Metrics"))
        lst = ["ga:adsenseRevenue", "ga:adsenseAdUnitsViewed", "ga:adsenseAdsViewed", "ga:adsenseAdsClicks",
               "ga:adsensePageImpressions", "ga:adsenseCTR", "ga:adsenseECPM", "ga:adsenseExits"]
        for name in lst:
            pg.Append(wxpg.BoolProperty(name, value=False))
            pg.SetPropertyAttribute(name, "UseCheckbox", True)

        pg.Append(wxpg.PropertyCategory("27 - Channel Grouping Dimensions & Metrics"))
        lst = ["ga:channelGrouping"]
        for name in lst:
            pg.Append(wxpg.BoolProperty(name, value=False))
            pg.SetPropertyAttribute(name, "UseCheckbox", True)

        pg.Append(wxpg.PropertyCategory("28 - Related Products Dimensions & Metrics"))
        lst = ["ga:correlationModelId", "ga:queryProductId", "ga:queryProductName", "ga:queryProductVariation",
               "ga:relatedProductId", "ga:relatedProductName", "ga:relatedProductVariation", "ga:correlationScore",
               "ga:queryProductQuantity", "ga:relatedProductQuantity"]
        for name in lst:
            pg.Append(wxpg.BoolProperty(name, value=False))
            pg.SetPropertyAttribute(name, "UseCheckbox", True)




        # When page is added, it will become the target page for AutoFill
        # calls (and for other property insertion methods as well)
        #pg.AddPage( "Page 2 - Results of AutoFill will appear here" )

        topsizer.Add(pg, 1, wx.EXPAND)

        rowsizer = wx.BoxSizer(wx.HORIZONTAL)
        m_staticText1 = wx.StaticText(panel, wx.ID_ANY, u"MyLabel", wx.DefaultPosition, wx.DefaultSize, 0 )
        m_staticText1.Wrap(-1)
        rowsizer.Add(m_staticText1, 1)
        #Sizer2.Add(m_staticText1, 1, wx.ALL|wx.EXPAND, 5)
        but = wx.Button(panel, -1, "SetPropertyValues")
        but.Bind(wx.EVT_BUTTON, self.OnSetPropertyValues)
        rowsizer.Add(but, 1)
        but = wx.Button(panel, -1, "GetPropertyValues")
        but.Bind(wx.EVT_BUTTON, self.OnGetPropertyValues)
        rowsizer.Add(but, 1)
        topsizer.Add(rowsizer, 0, wx.EXPAND)
        rowsizer = wx.BoxSizer(wx.HORIZONTAL)
        but = wx.Button(panel, -1, "GetPropertyValues(as_strings=True)")
        but.Bind(wx.EVT_BUTTON, self.OnGetPropertyValues2)
        rowsizer.Add(but, 1)
        but = wx.Button(panel, -1, "AutoFill")
        but.Bind(wx.EVT_BUTTON, self.OnAutoFill)
        rowsizer.Add(but, 1)
        topsizer.Add(rowsizer, 0, wx.EXPAND)
        rowsizer = wx.BoxSizer(wx.HORIZONTAL)
        but = wx.Button(panel, -1, "Delete")
        but.Bind(wx.EVT_BUTTON, self.OnDeleteProperty)
        rowsizer.Add(but, 1)
        but = wx.Button(panel, -1, "Run Tests")
        but.Bind(wx.EVT_BUTTON, self.RunTests)
        rowsizer.Add(but, 1)
        topsizer.Add(rowsizer, 0, wx.EXPAND)

        panel.SetSizer(topsizer)
        topsizer.SetSizeHints(panel)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(panel, 1, wx.EXPAND)
        self.SetSizer(sizer)
        self.SetAutoLayout(True)

    def OnPropGridChange(self, event):
        p = event.GetProperty()
        if p:
            self.log.write('%s changed to "%s"\n' % (p.GetName(), p.GetValueAsString()))

    def OnPropGridSelect(self, event):
        p = event.GetProperty()
        if p:
            self.log.write('%s selected\n' % (event.GetProperty().GetName()))
        else:
            self.log.write('Nothing selected\n')

    def OnDeleteProperty(self, event):
        p = self.pg.GetSelectedProperty()
        if p:
            self.pg.DeleteProperty(p)
        else:
            wx.MessageBox("First select a property to delete")

    def OnReserved(self, event):
        pass

    def OnSetPropertyValues(self, event):
        try:
            d = self.pg.GetPropertyValues(inc_attributes=True)

            ss = []
            for k, v in d.iteritems():
                v = repr(v)
                if not v or v[0] != '<':
                    if k.startswith('@'):
                        ss.append('setattr(obj, "%s", %s)' % (k, v))
                    else:
                        ss.append('obj.%s = %s' % (k, v))

            dlg = MemoDialog(self,
                             "Enter Content for Object Used in SetPropertyValues",
                             '\n'.join(ss))  # default_object_content1

            if dlg.ShowModal() == wx.ID_OK:
                import datetime

                sandbox = {'obj': ValueObject(),
                           'wx': wx,
                           'datetime': datetime}
                exec dlg.tc.GetValue() in sandbox
                t_start = time.time()
                #print(sandbox['obj'].__dict__)
                self.pg.SetPropertyValues(sandbox['obj'])
                t_end = time.time()
                self.log.write('SetPropertyValues finished in %.0fms\n' %
                               ((t_end - t_start) * 1000.0))
        except:
            import traceback

            traceback.print_exc()

    def OnGetPropertyValues(self, event):
        try:
            t_start = time.time()
            d = self.pg.GetPropertyValues(inc_attributes=True)
            t_end = time.time()
            self.log.write('GetPropertyValues finished in %.0fms\n' %
                           ((t_end - t_start) * 1000.0))
            ss = ['%s: %s' % (k, repr(v)) for k, v in d.iteritems()]
            dlg = MemoDialog(self, "GetPropertyValues Result",
                             'Contents of resulting dictionary:\n\n' + '\n'.join(ss))
            dlg.ShowModal()
        except:
            import traceback

            traceback.print_exc()

    def OnGetPropertyValues2(self, event):
        try:
            t_start = time.time()
            d = self.pg.GetPropertyValues(as_strings=True)
            t_end = time.time()
            self.log.write('GetPropertyValues(as_strings=True) finished in %.0fms\n' %
                           ((t_end - t_start) * 1000.0))
            ss = ['%s: %s' % (k, repr(v)) for k, v in d.iteritems()]
            dlg = MemoDialog(self, "GetPropertyValues Result",
                             'Contents of resulting dictionary:\n\n' + '\n'.join(ss))
            dlg.ShowModal()
        except:
            import traceback

            traceback.print_exc()

    def OnAutoFill(self, event):
        try:
            dlg = MemoDialog(self, "Enter Content for Object Used for AutoFill", default_object_content1)
            if dlg.ShowModal() == wx.ID_OK:
                sandbox = {'object': ValueObject(), 'wx': wx}
                exec dlg.tc.GetValue() in sandbox
                t_start = time.time()
                self.pg.AutoFill(sandbox['object'])
                t_end = time.time()
                self.log.write('AutoFill finished in %.0fms\n' %
                               ((t_end - t_start) * 1000.0))
        except:
            import traceback

            traceback.print_exc()

    def OnPropGridRightClick(self, event):
        p = event.GetProperty()
        if p:
            self.log.write('%s right clicked\n' % (event.GetProperty().GetName()))
        else:
            self.log.write('Nothing right clicked\n')

    def OnPropGridPageChange(self, event):
        index = self.pg.GetSelectedPage()
        self.log.write('Page Changed to \'%s\'\n' % (self.pg.GetPageName(index)))

    def RunTests(self, event):
        pg = self.pg
        log = self.log

        # Validate client data
        log.write('Testing client data set/get')
        pg.SetPropertyClientData("Bool", 1234)
        if pg.GetPropertyClientData("Bool") != 1234:
            raise ValueError("Set/GetPropertyClientData() failed")

        # Test setting unicode string
        log.write('Testing setting an unicode string value')
        pg.GetPropertyByName("String").SetValue(u"Some Unicode Text")

        #
        # Test some code that *should* fail (but not crash)
        try:
            if wx.GetApp().GetAssertionMode() == wx.PYAPP_ASSERT_EXCEPTION:
                log.write('Testing exception handling compliancy')
                a_ = pg.GetPropertyValue("NotARealProperty")
                pg.EnableProperty("NotAtAllRealProperty", False)
                pg.SetPropertyHelpString("AgaintNotARealProperty",
                                         "Dummy Help String")
        except:
            pass

        # GetPyIterator
        log.write('GetPage(0).GetPyIterator()\n')
        it = pg.GetPage(0).GetPyIterator(wxpg.PG_ITERATE_ALL)
        for prop in it:
            log.write('Iterating \'%s\'\n' % (prop.GetName()))

        # VIterator
        log.write('GetPyVIterator()\n')
        it = pg.GetPyVIterator(wxpg.PG_ITERATE_ALL)
        for prop in it:
            log.write('Iterating \'%s\'\n' % (prop.GetName()))

        # Properties
        log.write('GetPage(0).Properties\n')
        it = pg.GetPage(0).Properties
        for prop in it:
            log.write('Iterating \'%s\'\n' % (prop.GetName()))

        # Items
        log.write('GetPage(0).Items\n')
        it = pg.GetPage(0).Items
        for prop in it:
            log.write('Iterating \'%s\'\n' % (prop.GetName()))

#---------------------------------------------------------------------------


if __name__ == '__main__':
    app = wx.PySimpleApp()
    win = MyFrame1(parent=None)
    win.Show()
    app.MainLoop()