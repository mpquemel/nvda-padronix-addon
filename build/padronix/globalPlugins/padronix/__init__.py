# -*- coding: utf-8 -*-
# Padronix - NVDA Add-on for Academic Paper Formatting
# Copyright (C) 2026 Melhym Pereira Quemel
# Email: mpquemel@gmail.com
# GitHub: https://github.com/mpquemel/padronix
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""Padronix NVDA Add-on
Estrutura e formata artigos acadêmicos automaticamente usando IA.
"""

import globalPluginHandler
import scriptHandler
import ui
import tones
import wx
from .main_dialog import PadronixDialog
import addonHandler
addonHandler.initTranslation()

class GlobalPlugin(globalPluginHandler.GlobalPlugin):
    """Plugin principal do Padronix"""
    
    scriptCategory = "Padronix"
    
    def __init__(self):
        super(GlobalPlugin, self).__init__()
        self._dialog = None
    
    def script_openPadronix(self, gesture):
        """Abre a interface principal do Padronix"""
        if self._dialog is None or not self._dialog.IsShown():
            self._dialog = PadronixDialog(None)
            self._dialog.Show()
        else:
            self._dialog.Raise()
            self._dialog.Iconize(False)
            self._dialog.SetFocus()
    
    # Atalho: NVDA+Ctrl+Shift+F
    __gestures = {
        "kb(NVDA):control+shift+f": "openPadronix",
    }
