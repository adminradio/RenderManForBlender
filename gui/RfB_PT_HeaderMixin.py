from . import icons
from .. import rt


class _RManPanelHeader():
    iid = icons.iconid('renderman')

    def draw_header(self, context):
        if rt.reg.prefs().draw_panel_icon:
            self.layout.label(text="", icon_value=self.iid)
        else:
            pass
