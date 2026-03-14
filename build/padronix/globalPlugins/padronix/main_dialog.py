# -*- coding: utf-8 -*-
# Padronix - NVDA Add-on for Academic Paper Formatting
# Copyright (C) 2026 Melhym Pereira Quemel
# Email: mpquemel@gmail.com

"""Interface principal do Padronix"""

import wx
import os
import sys
import addonHandler
addonHandler.initTranslation()

# Adicionar lib ao path para importar dependências
lib_path = os.path.join(os.path.dirname(__file__), "..", "lib")
if lib_path not in sys.path:
    sys.path.insert(0, lib_path)

from .padronix_settings import PadronixSettingsPanel
from .workflow_manager import WorkflowManager

class PadronixDialog(wx.Dialog):
    """Janela principal do Padronix"""
    
    def __init__(self, parent):
        super(PadronixDialog, self).__init__(
            parent,
            title=_("Padronix - Estruturador de Artigos Acadêmicos"),
            size=(600, 500)
        )
        
        self.workflow_manager = WorkflowManager(self)
        self.txt_content = ""
        self.json_content = ""
        
        # Painel principal
        panel = wx.Panel(self)
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        
        # Título
        title = wx.StaticText(panel, label=_("Padronix v2026.1.0"))
        title.SetFont(wx.Font(16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        main_sizer.Add(title, 0, wx.ALL | wx.CENTER, 10)
        
        # Botão carregar TXT
        self.btn_load_txt = wx.Button(panel, label=_("Carregar &TXT"))
        self.btn_load_txt.Bind(wx.EVT_BUTTON, self.on_load_txt)
        main_sizer.Add(self.btn_load_txt, 0, wx.ALL | wx.EXPAND, 5)
        
        # Botão importar JSON
        self.btn_import_json = wx.Button(panel, label=_("Importar &JSON"))
        self.btn_import_json.Bind(wx.EVT_BUTTON, self.on_import_json)
        main_sizer.Add(self.btn_import_json, 0, wx.ALL | wx.EXPAND, 5)
        
        # Painel de configurações
        self.settings_panel = PadronixSettingsPanel(panel)
        main_sizer.Add(self.settings_panel, 1, wx.ALL | wx.EXPAND, 10)
        
        # Botão gerar DOCX
        self.btn_generate = wx.Button(panel, label=_("&Gerar DOCX"))
        self.btn_generate.Bind(wx.EVT_BUTTON, self.on_generate)
        self.btn_generate.Enable(False)
        main_sizer.Add(self.btn_generate, 0, wx.ALL | wx.EXPAND, 5)
        
        # Botão fechar
        self.btn_close = wx.Button(panel, label=_("&Fechar"))
        self.btn_close.Bind(wx.EVT_BUTTON, lambda e: self.Close())
        main_sizer.Add(self.btn_close, 0, wx.ALL | wx.EXPAND, 5)
        
        panel.SetSizer(main_sizer)
        
        # Anunciar abertura
        ui.message(_("Padronix aberto"))
    
    def on_load_txt(self, event):
        """Carregar arquivo TXT"""
        ui.message(_("Abrindo seletor de arquivo TXT..."))
        
        with wx.FileDialog(
            self,
            _("Selecionar arquivo TXT"),
            wildcard="Arquivos TXT (*.txt)|*.txt|Todos os arquivos (*.*)|*.*",
            style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST
        ) as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return
            
            filepath = fileDialog.GetPath()
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    self.txt_content = f.read()
                
                ui.message(_("TXT carregado: {} caracteres").format(len(self.txt_content)))
                self.btn_generate.Enable(True)
                
            except Exception as e:
                ui.message(_("Erro ao carregar TXT: {}").format(str(e)))
                tones.beep(150, 300)
    
    def on_import_json(self, event):
        """Importar JSON estruturado"""
        ui.message(_("Abrindo seletor de arquivo JSON..."))
        
        with wx.FileDialog(
            self,
            _("Selecionar arquivo JSON"),
            wildcard="Arquivos JSON (*.json)|*.json|Todos os arquivos (*.*)|*.*",
            style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST
        ) as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return
            
            filepath = fileDialog.GetPath()
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    self.json_content = f.read()
                
                ui.message(_("JSON carregado"))
                self.btn_generate.Enable(True)
                
            except Exception as e:
                ui.message(_("Erro ao carregar JSON: {}").format(str(e)))
                tones.beep(150, 300)
    
    def on_generate(self, event):
        """Gerar documento DOCX"""
        if not self.txt_content and not self.json_content:
            ui.message(_("Erro: Nenhum conteúdo carregado"))
            tones.beep(150, 300)
            return
        
        ui.message(_("Iniciando processamento..."))
        
        # Obter configurações
        provider = self.settings_panel.get_provider()
        model = self.settings_panel.get_model()
        api_key = self.settings_panel.get_api_key()
        standard = self.settings_panel.get_standard()
        
        # Iniciar workflow
        self.workflow_manager.process(
            txt_content=self.txt_content,
            json_content=self.json_content,
            provider=provider,
            model=model,
            api_key=api_key,
            standard=standard
        )
