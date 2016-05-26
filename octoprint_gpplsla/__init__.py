# coding=utf-8
from __future__ import absolute_import

import re
from Tkinter import *

import octoprint.plugin

class GPPLSLAPlugin(octoprint.plugin.EventHandlerPlugin,
                    octoprint.plugin.SettingsPlugin, 
                    octoprint.plugin.StartupPlugin,
                    octoprint.plugin.TemplatePlugin):
    def on_after_startup(self):
        self._logger.info("Hello World! image_archive = {}".format(self._settings.get(["image_archive"])))

    def get_settings_defaults(self):
        return dict(image_archive="images.tar.gz")

    def get_template_configs(self):
        return [dict(type="settings", custom_bindings=False)]

    def sending_g420(self, comm_instance, phase, cmd, cmd_type, gcode, *args, **kwargs):
        if gcode and gcode == "G420":  # stop laughing
            self._logger.info("Sending G420: {}".format(cmd))
            image_name = re.search(r"P(\S+)", cmd).group(1)
            image_path = self.get_image_path(image_name)
            pause = int(re.search(r"P(\d+)", cmd).group(1))
            self.display_image(image_path, pause)
            
    @staticmethod
    def get_image_path(image_name):
        pass
            
    @staticmethod
    def render_svg():
        pass

    @staticmethod
    def display_image(image_path, pause):
        root = Tk()
        width = root.winfo_screenwidth()
        height = root.winfo_screenheight()
        root.overrideredirect(1)
        root.geometry("{}x{}+0+0".format(width, height))
        root.focus_set()
        root.after(pause * 1000, lambda: root.destroy())
        root.mainloop()
        

__plugin_name__ = "GPPL SLA"

def __plugin_load__():
    plugin = GPPLSLAPlugin()

    global __plugin_implementation__
    __plugin_implementation__ = plugin

    global __plugin_hooks__
    __plugin_hooks__ = {"octoprint.comm.protocol.gcode.sending": plugin.sending_g420}
