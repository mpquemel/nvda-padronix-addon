# -*- coding: utf-8 -*-
# Padronix - NVDA Add-on for Academic Paper Formatting
# Copyright (C) 2026 Melhym Pereira Quemel
# Email: mpquemel@gmail.com

"""Gerenciador de workflow do Padronix"""

import wx
import threading
import os
import json
import addonHandler
addonHandler.initTranslation()

from .ai_client import AIClient
from .docx_renderer import DocxRenderer

class WorkflowManager:
    """Gerencia o fluxo de processamento do artigo"""
    
    def __init__(self, dialog):
        self.dialog = dialog
        self.ai_client = None
        self.renderer = None
    
    def process(self, txt_content, json_content, provider, model, api_key, standard):
        """Processar artigo completo"""
        
        # Iniciar thread de processamento
        thread = threading.Thread(
            target=self._process_thread,
            args=(txt_content, json_content, provider, model, api_key, standard)
        )
        thread.daemon = True
        thread.start()
    
    def _process_thread(self, txt_content, json_content, provider, model, api_key, standard):
        """Thread de processamento (background)"""
        
        try:
            # Etapa 1: Estruturar com IA
            wx.CallAfter(
                self.dialog.ui_message,
                _("Estruturando artigo com IA...")
            )
            
            self.ai_client = AIClient(provider, model, api_key)
            
            if txt_content:
                structured = self.ai_client.structure_article(txt_content)
            elif json_content:
                structured = json.loads(json_content)
            else:
                raise ValueError(_("Nenhum conteúdo para processar"))
            
            # Etapa 2: Renderizar DOCX
            wx.CallAfter(
                self.dialog.ui_message,
                _("Renderizando documento DOCX...")
            )
            
            self.renderer = DocxRenderer(standard)
            output_path = self.renderer.render(structured)
            
            # Etapa 3: Finalizar
            wx.CallAfter(
                self.dialog.ui_message,
                _("Finalizando...")
            )
            
            # Sucesso!
            wx.CallAfter(
                self.dialog.ui_message,
                _("Documento Padronix gerado em: {}").format(output_path)
            )
            
            # Som de sucesso (acorde)
            wx.CallAfter(self.play_success_sound)
            
        except Exception as e:
            wx.CallAfter(
                self.dialog.ui_message,
                _("Erro de processamento: {}").format(str(e))
            )
            wx.CallAfter(self.play_error_sound)
    
    def play_success_sound(self):
        """Tocar som de sucesso"""
        import winsound
        # Acorde de piano simples
        winsound.Beep(523, 100)  # C5
        winsound.Beep(659, 100)  # E5
        winsound.Beep(784, 200)  # G5
    
    def play_error_sound(self):
        """Tocar som de erro"""
        import winsound
        winsound.Beep(150, 300)
