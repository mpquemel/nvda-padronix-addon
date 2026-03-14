# -*- coding: utf-8 -*-
"""
Padronix - NVDA Add-on for Academic Paper Formatting
Copyright (C) 2026 Melhym Pereira Quemel <mpquemel@gmail.com>
GitHub: https://github.com/mpquemel/padronix

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

"""
Módulo Bootstrap & Injeção Multi-Arquitetura
Responsável por carregar bibliotecas externas (32/64-bit) e inicializar o plugin.
"""

from __future__ import annotations

import sys
import os
import struct
from pathlib import Path
from typing import TYPE_CHECKING, Optional, Self

import globalPluginHandler
import scriptHandler
import config
import gui
from gui import SettingsPanel, guiHelper
import ui
import addonHandler

addonHandler.initTranslation()

# ============================================================================
# INJEÇÃO MULTI-ARQUITETURA
# ============================================================================

def _inject_lib_path() -> None:
    """
    Injeta bibliotecas externas no sys.path conforme arquitetura (32/64-bit).
    
    Estrutura esperada:
    - lib/shared/     (bibliotecas puras Python)
    - lib/x86/        (binários 32-bit)
    - lib/x64/        (binários 64-bit)
    """
    plugin_dir: Path = Path(__file__).parent
    lib_base: Path = plugin_dir / "lib"
    
    # Bibliotecas compartilhadas (requests, urllib3, python-docx)
    shared_path: Path = lib_base / "shared"
    if shared_path.exists() and str(shared_path) not in sys.path:
        sys.path.insert(0, str(shared_path))
    
    # Detectar arquitetura (32-bit vs 64-bit)
    is_64bit: bool = struct.calcsize("P") * 8 == 64
    arch_folder: str = "x64" if is_64bit else "x86"
    
    # Injetar bibliotecas específicas da arquitetura (lxml, etc.)
    arch_path: Path = lib_base / arch_folder
    if arch_path.exists() and str(arch_path) not in sys.path:
        sys.path.insert(0, str(arch_path))
    
    # Log para debugging (visível em NVDA+F1)
    import logHandler
    logHandler.log.info(f"Padronix: Bibliotecas carregadas para arquitetura {arch_folder}")

# Injetar bibliotecas antes de qualquer import externo
_inject_lib_path()

# ============================================================================
# IMPORTS COM VALIDAÇÃO
# ============================================================================

try:
    from .padronix_settings import PadronixSettingsPanel
    from .main_dialog import PadronixDialog
    SETTINGS_AVAILABLE: bool = True
except ImportError as e:
    SETTINGS_AVAILABLE = False
    import logHandler
    logHandler.log.error(f"Padronix: Falha ao importar módulos: {e}")

# ============================================================================
# CONFIGURAÇÃO NATIVA DO NVDA
# ============================================================================

# Registra seção de configuração do Padronix no NVDA
if "padronix" not in config.conf:
    config.conf["padronix"] = {}

# Valores padrão
_PADRONIX_DEFAULTS: dict = {
    "provider": "google",
    "model": "gemini-pro",
    "api_key": "",
    "standard": "abnt",
    "last_txt_path": "",
    "last_json_path": "",
}

# Aplicar defaults
for key, value in _PADRONIX_DEFAULTS.items():
    if key not in config.conf["padronix"]:
        config.conf["padronix"][key] = value

# ============================================================================
# GLOBAL PLUGIN
# ============================================================================

class GlobalPlugin(globalPluginHandler.GlobalPlugin):
    """
    Plugin principal do Padronix.
    
    Responsabilidades:
    - Registrar atalho de teclado (NVDA+Ctrl+Shift+F)
    - Gerenciar ciclo de vida do diálogo
    - Cleanup adequado no terminate()
    """
    
    scriptCategory: str = "Padronix"
    _dialog: Optional[PadronixDialog] = None
    
    def __init__(self) -> None:
        """Inicialização do plugin."""
        # Rota A: super().__init__() moderno (Python 3)
        super().__init__()
        
        if not SETTINGS_AVAILABLE:
            import logHandler
            # Rota A: except específico
            logHandler.log.error("Padronix: Módulos não disponíveis. Plugin desativado.")
            return
        
        # Registrar painel de configurações no NVDA
        self._register_settings_panel()
    
    def _register_settings_panel(self) -> None:
        """Registra painel de configurações no menu do NVDA."""
        try:
            # Rota A: PadronixSettingsPanel agora herda SettingsPanel corretamente
            # A classe PadronixSettingsPanel foi reestruturada para herdar SettingsPanel
            # Removida delegação através de PadronixSettingsCategory wrapper
            
            # Registrar categoria
            gui.settingsDialogs.NVDASettingsDialog.categoryClasses.append(
                PadronixSettingsPanel
            )
            
        except (ImportError, AttributeError, RuntimeError, KeyError) as e:
            import logHandler
            # Rota A: except específico
            logHandler.log.error(f"Padronix: Erro ao registrar painel: {e}")
    
    @scriptHandler.script(
        description=_("Abre a interface principal do Padronix"),
        gesture="kb:NVDA+control+shift+f"
    )
    def script_openPadronix(self, gesture: scriptHandler.InputGesture) -> None:
        """
        Abre a interface principal do Padronix.
        
        Args:
            gesture: Gesture de teclado que acionou o script.
        """
        if not SETTINGS_AVAILABLE:
            ui.message(_("Erro: Padronix não pôde ser carregado. Verifique o log do NVDA."))
            return
        
        try:
            if self._dialog is None or not self._dialog.IsShown():
                self._dialog = PadronixDialog(gui.mainFrame)
                self._dialog.Show()
                self._dialog.Raise()
            else:
                self._dialog.Raise()
                self._dialog.Iconize(False)
                self._dialog.SetFocus()
                
        except (ImportError, AttributeError, RuntimeError, KeyError) as e:
            import logHandler
            # Rota A: except específico
            logHandler.log.error(f"Padronix: Erro ao abrir diálogo: {e}")
            ui.message(_("Erro ao abrir Padronix. Verifique o log do NVDA."))
    
    def terminate(self) -> None:
        """
        Cleanup ao desativar o plugin.
        
        Remove atalhos, destrói janelas e libera recursos.
        """
        # Rota A: super().__init__() moderno (Python 3)
        super().__init__()
        
        # Destruir diálogo se existir
        if self._dialog is not None:
            try:
                if self._dialog.IsShown():
                    self._dialog.Close()
                self._dialog.Destroy()
                self._dialog = None
            except (ImportError, AttributeError, RuntimeError, KeyError) as e:
                import logHandler
                # Rota A: except específico
                logHandler.log.error(f"Padronix: Erro ao destruir diálogo: {e}")
        
        # Log de encerramento
        import logHandler
        logHandler.log.info("Padronix: Plugin encerrado com sucesso.")
