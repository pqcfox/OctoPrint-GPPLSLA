# coding=utf-8
from __future__ import absolute_import

import base64
import cairo
import re
import rsvg
from cStringIO import StringIO
from PIL import Image
from Tkinter import *

import octoprint.plugin

class GPPLSLAPlugin(octoprint.plugin.SettingsPlugin,
                    octoprint.plugin.TemplatePlugin):
    def get_settings_defaults(self):		
        return dict(scale_factor=8)

    def get_template_configs(self):
        return [dict(type="settings", custom_bindings=False)]

    def sending_g420(self, comm_instance, phase, cmd, cmd_type, gcode, *args, **kwargs):
        if gcode:
            if gcode == "M654":
                self._logger.info("Handling M654: {}".format(cmd))
                payload = re.search(r"\sE(\S+)", cmd).group(1)
            if gcode == "G420":  # stop laughing
                self._logger.info("Handling G420: {}".format(cmd))
                time = float(re.search(r"\sP(\S+)", cmd).group(1))
                display_payload(payload, time)

    @staticmethod
    def render_svg(payload, size, root):
        image = cairo.ImageSurface(cairo.FORMAT_ARGB32, *size)
        context = cairo.Context(image)
        handle = rsvg.Handle(None, base64.b64decode(payload))
        handle.render_cairo(context)
        return Image.open(StringIO(img.get_data()))

    @staticmethod
    def display_image(payload, pause):
        root = Tk()
        width = root.winfo_screenwidth()
        height = root.winfo_screenheight()
        size = (width, height)
        image = render_svg(payload, size, root)
        panel = Label(root, image=image)
        panel.pack(side="bottom", fill="both", expand="yes")
        root.overrideredirect(1)
        root.geometry("{}x{}+0+0".format(*size))
        root.focus_set()
        root.after(pause * 1000, lambda: root.destroy())
        root.mainloop()
        

__plugin_name__ = "GPPL SLA"

def __plugin_load__():
    plugin = GPPLSLA()

    global __plugin_implementation__
    __plugin_implementation__ = plugin

    global __plugin_hooks__
    __plugin_hooks__ = {"octoprint.comm.protocol.gcode.sending": plugin.sending_g420}
