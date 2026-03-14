# -*- coding: utf-8 -*-
"""
Padronix - Interface Principal de Operação
Copyright (C) 2026 Melhym Pereira Quemel <mpquemel@gmail.com>

Diálogo principal acionado pelo atalho NVDA+Ctrl+Shift+F.
"""

from __future__ import annotations

import wx
import os
from pathlib import Path
from typing import Optional, Callable
import addonHandler

addonHandler.initTranslation()

from .workflow_manager import WorkflowManager
import speech
import tones


class PadronixDialog(wx.Dialog):
    """
    Janela principal de operações do Padronix.
    
    Features:
    - Botões grandes com atalhos Alt
    - Feedback auditivo imediato
    - Desabilitação temporária para evitar duplo clique
    - Gerenciamento de ciclo de vida adequado
    """
    
    def __init__(self, parent: wx.Window) -> None:
        """
        Inicializa diálogo principal.
        
        Args:
            parent: Janela pai (geralmente gui.mainFrame)
        """
        super(PadronixDialog, self).__init__(
            parent,
            title=_("Padronix - Estruturador de Artigos Acadêmicos"),
            size=wx.Size(550, 450),
            style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER
        )
        
        self.workflow_manager = WorkflowManager(self)
        self.txt_content: str = ""
        self.json_content: str = ""
        
        self._create_ui()
        self._bind_events()
        
        # Centralizar na tela
        self.Centre(wx.BOTH)
        
        # Anunciar abertura
        speech.speakMessage(_("Padronix aberto"))
        
        # Tocar tom de confirmação
        tones.beep(880, 100)  # A5 - som agradável
    
    def _create_ui(self) -> None:
        """Cria interface do diálogo."""
        panel = wx.Panel(self)
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        
        # Título
        title = wx.StaticText(panel, label=_("Padronix v2026.1.0"))
        title_font = wx.Font(16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        title.SetFont(title_font)
        main_sizer.Add(title, 0, wx.ALL | wx.CENTER, 15)
        
        # Subtítulo
        subtitle = wx.StaticText(
            panel,
            label=_("Estruture artigos acadêmicos com IA e formate em DOCX")
        )
        main_sizer.Add(subtitle, 0, wx.ALL | wx.CENTER, 5)
        
        # Separador
        main_sizer.Add(wx.StaticLine(panel), 0, wx.ALL | wx.EXPAND, 10)
        
        # === BOTÃO: Carregar TXT ===
        self.btn_load_txt = wx.Button(
            panel,
            label=_("&Carregar TXT do Artigo")
        )
        self.btn_load_txt.SetMinSize(wx.Size(400, 40))
        main_sizer.Add(self.btn_load_txt, 0, wx.ALL | wx.CENTER, 10)
        
        # Status do TXT
        self.lbl_txt_status = wx.StaticText(panel, label=_("Nenhum arquivo TXT carregado"))
        self.lbl_txt_status.SetForegroundColour(wx.Colour(128, 128, 128))
        main_sizer.Add(self.lbl_txt_status, 0, wx.ALL | wx.CENTER, 5)
        
        # === BOTÃO: Importar JSON ===
        self.btn_import_json = wx.Button(
            panel,
            label=_("&Importar JSON Estruturado")
        )
        self.btn_import_json.SetMinSize(wx.Size(400, 40))
        main_sizer.Add(self.btn_import_json, 0, wx.ALL | wx.CENTER, 10)
        
        # Status do JSON
        self.lbl_json_status = wx.StaticText(panel, label=_("Nenhum JSON importado"))
        self.lbl_json_status.SetForegroundColour(wx.Colour(128, 128, 128))
        main_sizer.Add(self.lbl_json_status, 0, wx.ALL | wx.CENTER, 5)
        
        # Separador
        main_sizer.Add(wx.StaticLine(panel), 0, wx.ALL | wx.EXPAND, 10)
        
        # === BOTÃO: Gerar DOCX ===
        self.btn_generate = wx.Button(
            panel,
            label=_("&Gerar Documento DOCX")
        )
        self.btn_generate.SetMinSize(wx.Size(400, 50))
        self.btn_generate.SetFont(wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        self.btn_generate.Enable(False)  # Desabilitado até carregar conteúdo
        main_sizer.Add(self.btn_generate, 0, wx.ALL | wx.CENTER, 10)
        
        # Separador
        main_sizer.Add(wx.StaticLine(panel), 0, wx.ALL | wx.EXPAND, 10)
        
        # === BOTÃO: Fechar ===
        self.btn_close = wx.Button(panel, label=_("&Fechar"))
        self.btn_close.SetMinSize(wx.Size(150, 35))
        main_sizer.Add(self.btn_close, 0, wx.ALL | wx.CENTER, 10)
        
        # Espaçador
        main_sizer.AddStretchSpacer()
        
        panel.SetSizer(main_sizer)
        self.Layout()
    
    def _bind_events(self) -> None:
        """Vincula eventos aos botões."""
        self.btn_load_txt.Bind(wx.EVT_BUTTON, self._on_load_txt)
        self.btn_import_json.Bind(wx.EVT_BUTTON, self._on_import_json)
        self.btn_generate.Bind(wx.EVT_BUTTON, self._on_generate)
        self.btn_close.Bind(wx.EVT_BUTTON, self._on_close)
        
        # Fechar com ESC
        self.Bind(wx.EVT_CHAR_HOOK, self._on_key_esc)
    
    def _on_key_esc(self, event: wx.KeyEvent) -> None:
        """Fecha diálogo com ESC."""
        if event.GetKeyCode() == wx.WXK_ESCAPE:
            self.Close()
        else:
            event.Skip()
    
    def _on_load_txt(self, event: wx.Event) -> None:
        """
        Callback para carregar arquivo TXT.
        
        Abre diálogo de arquivo, lê conteúdo e atualiza status.
        """
        # Feedback imediato
        speech.speakMessage(_("Abrindo seletor de arquivo TXT..."))
        self.btn_load_txt.Enable(False)
        
        wx.CallAfter(self._show_txt_dialog)
    
    def _show_txt_dialog(self) -> None:
        """Mostra diálogo de seleção de TXT."""
        try:
            with wx.FileDialog(
                self,
                _("Selecionar arquivo TXT"),
                wildcard="Arquivos TXT (*.txt)|*.txt|Todos os arquivos (*.*)|*.*",
                style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST
            ) as fileDialog:
                
                if fileDialog.ShowModal() == wx.ID_CANCEL:
                    self.btn_load_txt.Enable(True)
                    return
                
                filepath = fileDialog.GetPath()
                
                # Ler arquivo
                with open(filepath, 'r', encoding='utf-8') as f:
                    self.txt_content = f.read()
                
                # Atualizar UI
                char_count = len(self.txt_content)
                self.lbl_txt_status.SetLabel(
                    _("TXT carregado: {} caracteres").format(char_count)
                )
                self.lbl_txt_status.SetForegroundColour(wx.Colour(0, 128, 0))  # Verde
                
                # Habilitar botão de geração
                self._update_generate_button()
                
                # Feedback auditivo
                speech.speakMessage(
                    _("TXT carregado: {} caracteres. Pressione Alt+G para gerar DOCX.").format(char_count)
                )
                tones.beep(660, 100)  # E5 - som de sucesso
                
        except Exception as e:
            speech.speakMessage(_("Erro ao carregar TXT: {}").format(str(e)))
            tones.beep(220, 300)  # A3 - som de erro
            
        finally:
            self.btn_load_txt.Enable(True)
    
    def _on_import_json(self, event: wx.Event) -> None:
        """
        Callback para importar JSON estruturado.
        
        Permite pular etapa da IA usando JSON pré-estruturado.
        """
        speech.speakMessage(_("Abrindo seletor de arquivo JSON..."))
        self.btn_import_json.Enable(False)
        
        wx.CallAfter(self._show_json_dialog)
    
    def _show_json_dialog(self) -> None:
        """Mostra diálogo de seleção de JSON."""
        try:
            with wx.FileDialog(
                self,
                _("Selecionar JSON estruturado"),
                wildcard="Arquivos JSON (*.json)|*.json",
                style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST
            ) as fileDialog:
                
                if fileDialog.ShowModal() == wx.ID_CANCEL:
                    self.btn_import_json.Enable(True)
                    return
                
                filepath = fileDialog.GetPath()
                
                # Ler arquivo
                with open(filepath, 'r', encoding='utf-8') as f:
                    self.json_content = f.read()
                
                # Validar JSON
                import json
                json.loads(self.json_content)  # Validação
                
                # Atualizar UI
                self.lbl_json_status.SetLabel(_("JSON importado com sucesso"))
                self.lbl_json_status.SetForegroundColour(wx.Colour(0, 128, 0))
                
                # Habilitar botão de geração
                self._update_generate_button()
                
                # Feedback
                speech.speakMessage(_("JSON estruturado importado. Pronto para gerar DOCX."))
                tones.beep(660, 100)
                
        except json.JSONDecodeError:
            speech.speakMessage(_("Erro: Arquivo JSON inválido"))
            tones.beep(220, 300)
            
        except Exception as e:
            speech.speakMessage(_("Erro ao importar JSON: {}").format(str(e)))
            tones.beep(220, 300)
            
        finally:
            self.btn_import_json.Enable(True)
    
    def _on_generate(self, event: wx.Event) -> None:
        """
        Callback para iniciar geração do DOCX.
        
        Inicia workflow de processamento assíncrono.
        """
        if not self.txt_content and not self.json_content:
            speech.speakMessage(_("Erro: Nenhum conteúdo carregado"))
            tones.beep(220, 300)
            return
        
        # Desabilitar botão temporariamente
        self.btn_generate.Enable(False)
        self.btn_generate.SetLabel(_("Processando..."))
        
        speech.speakMessage(_("Iniciando processamento. Isso pode levar alguns segundos..."))
        
        # Iniciar workflow
        wx.CallAfter(self._start_processing)
    
    def _start_processing(self) -> None:
        """Inicia processamento no workflow manager."""
        try:
            self.workflow_manager.process(
                txt_content=self.txt_content,
                json_content=self.json_content
            )
        except Exception as e:
            speech.speakMessage(_("Erro ao iniciar processamento: {}").format(str(e)))
            self.btn_generate.Enable(True)
            self.btn_generate.SetLabel(_("&Gerar Documento DOCX"))
            tones.beep(220, 300)
    
    def _update_generate_button(self) -> None:
        """Atualiza estado do botão de geração."""
        has_content = bool(self.txt_content or self.json_content)
        self.btn_generate.Enable(has_content)
        
        if has_content:
            self.btn_generate.SetDefault()  # Torna botão padrão (Enter)
    
    def _on_close(self, event: wx.Event) -> None:
        """Fecha diálogo."""
        speech.speakMessage(_("Fechando Padronix"))
        self.Close()
    
    def on_processing_complete(self, success: bool, message: str) -> None:
        """
        Callback chamado quando processamento termina.
        
        Args:
            success: True se processamento teve sucesso
            message: Mensagem de resultado
        """
        wx.CallAfter(self._update_ui_after_processing, success, message)
    
    def _update_ui_after_processing(self, success: bool, message: str) -> None:
        """Atualiza UI após processamento."""
        self.btn_generate.Enable(True)
        self.btn_generate.SetLabel(_("&Gerar Documento DOCX"))
        
        if success:
            # Som de sucesso (acorde)
            tones.beep(523, 100)  # C5
            wx.CallLater(50, lambda: tones.beep(659, 100))  # E5
            wx.CallLater(100, lambda: tones.beep(784, 200))  # G5
        else:
            tones.beep(220, 300)
        
        speech.speakMessage(message)
