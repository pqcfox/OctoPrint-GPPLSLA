# coding=utf-8
from __future__ import absolute_import

import re
import tarfile
from Tkinter import *

import octoprint.plugin

payload = None

def sending_g420(self, comm_instance, phase, cmd, cmd_type, gcode, *args, **kwargs):
    if gcode:
        if gcode == "M654":
            self._logger.info("Handling M654: {}".format(cmd))
        if gcode == "G420":  # stop laughing
            self._logger.info("Handling G420: {}".format(cmd))
            self.display_image(self.render_svg(self.decode_svg(payload)))

@staticmethod
def decode_svg(text):
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
__plugin_hooks__ = {"octoprint.comm.protocol.gcode.sending": plugin.sending_g420}
