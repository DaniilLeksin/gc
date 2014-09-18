__author__ = 'Daniil Leksin'
# -*- coding: utf-8 -*-


def on_change_value(event, dict_credentials, dict_params, dict_api_properties):
    """

    :param event:
    :param dict_credentials:
    :param dict_api_properties:
    :return:
    """
    current_property = event.GetProperty().GetName()
    new_property_value = event.GetProperty().GetValue()
    current_category = event.GetProperty().GetParent().GetName()
    # Change the value of the property
    if current_category in ["01 - Client Parameters"]:
        dict_credentials["installed"][current_property] = new_property_value
    elif current_category in ["02 - Required Parameters"]:
        if current_property in ["start-date", "end-date"]:
            # piano - remake
            new_property_value = new_property_value.FormatDate().replace('/', '-')
        dict_params[current_property] = new_property_value
    else:
        dict_api_properties["/"][current_property]["value"] = new_property_value
    return dict_credentials, dict_params, dict_api_properties


def on_select_property(event, dict_api_properties):
    current_property = event.GetProperty()
    if current_property:
        try:
            # TODO: normal handler of the event "PGEVT_SELECTED"
            #print('%s selected\n' % (event.GetProperty().GetName()))
            #html_path = dict_api_properties["/"][event.GetProperty().GetName()]["html"]
            #self.GetTopLevelParent().set_html_page("html/%s" % html_path)
            pass
        except KeyError as error:
            print "No key found: %s" % str(error)   # TODO: to log
    else:
        print('Nothing selected\n')  # TODO: to log