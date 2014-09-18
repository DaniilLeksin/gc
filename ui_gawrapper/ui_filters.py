import wx

_ = wx.GetTranslation
import wx.propgrid as grid


class FiltersAdds(grid.PyTextCtrlEditor):
    def __init__(self):
        grid.PyTextCtrlEditor.__init__(self)

    def CreateControls(self, property_grid, property, pos, sz):
        # Create and populate buttons-subwindow
        buttons = grid.PGMultiButton(property_grid, sz)

        buttons.AddButton("...")
        buttons.AddButton("x")

        # Create the 'primary' editor control (textctrl in this case)
        wnd = self.CallSuperMethod("CreateControls",
                                   property_grid,
                                   property,
                                   pos,
                                   buttons.GetPrimarySize())

        # Finally, move buttons-subwindow to correct position and make sure
        # returned wxPGWindowList contains our custom button list.
        buttons.Finalize(property_grid, pos)

        # We must maintain a reference to any editor objects we created
        # ourselves. Otherwise they might be freed prematurely. Also,
        # we need it in OnEvent() below, because in Python we cannot "cast"
        # result of wxPropertyGrid.GetEditorControlSecondary() into
        # PGMultiButton instance.
        self.button = buttons
        return wnd, buttons

    def OnEvent(self, property_grid, prop, ctrl, event):
        if event.GetEventType() == wx.wxEVT_COMMAND_BUTTON_CLICKED:
            buttons = self.button
            evtId = event.GetId()

            if evtId == buttons.GetButtonId(0):
                # TODO: show box to find the filter
                return False  # Return false since value did not change
            if evtId == buttons.GetButtonId(1):
                # TODO: clear property value
                return False  # Return false since value did not change

        return self.CallSuperMethod("OnEvent", property_grid, prop, ctrl, event)
