# -*- coding: utf-8 -*-
# Padronix - NVDA Add-on for Academic Paper Formatting
# Copyright (C) 2026 Melhym Pereira Quemel
# Email: mpquemel@gmail.com

"""Painel de configurações do Padronix"""

import wx
import json
import os
import addonHandler
addonHandler.initTranslation()

class PadronixSettingsPanel(wx.Panel):
    """Painel de configurações"""
    
    PROVIDERS = [
        ("google", "Google Gemini"),
        ("openai", "OpenAI"),
        ("openrouter", "OpenRouter"),
        ("ollama", "Ollama Local")
    ]
    
    STANDARDS = [
        ("abnt", "ABNT (Brasil)"),
        ("apa", "APA (EUA)"),
        ("ieee", "IEEE (Engenharia)"),
        ("chicago", "Chicago (Humanidades)"),
        ("harvard", "Harvard (Economia)"),
        ("mla", "MLA (Literatura)"),
        ("vancouver", "Vancouver (Medicina)")
    ]
    
    def __init__(self, parent):
        super(PadronixSettingsPanel, self).__init__(parent)
        
        sizer = wx.BoxSizer(wx.VERTICAL)
        
        # Provedor de IA
        sizer.Add(wx.StaticText(self, label=_("Provedor de &IA:")), 0, wx.ALL, 5)
        self.provider_combo = wx.ComboBox(
            self,
            choices=[p[1] for p in self.PROVIDERS],
            style=wx.CB_READONLY
        )
        self.provider_combo.SetSelection(0)
        sizer.Add(self.provider_combo, 0, wx.ALL | wx.EXPAND, 5)
        
        # Chave API
        sizer.Add(wx.StaticText(self, label=_("Chave &API:")), 0, wx.ALL, 5)
        self.api_key_text = wx.TextCtrl(self, style=wx.TE_PASSWORD)
        sizer.Add(self.api_key_text, 0, wx.ALL | wx.EXPAND, 5)
        
        # Botão atualizar modelos
        self.btn_update_models = wx.Button(self, label=_("&Atualizar Lista de Modelos"))
        self.btn_update_models.Bind(wx.EVT_BUTTON, self.on_update_models)
        sizer.Add(self.btn_update_models, 0, wx.ALL, 5)
        
        # Modelo
        sizer.Add(wx.StaticText(self, label=_("&Modelo:")), 0, wx.ALL, 5)
        self.model_combo = wx.ComboBox(self, style=wx.CB_READONLY)
        sizer.Add(self.model_combo, 0, wx.ALL | wx.EXPAND, 5)
        
        # Padrão acadêmico
        sizer.Add(wx.StaticText(self, label=_("Padrão &Acadêmico:")), 0, wx.ALL, 5)
        self.standard_combo = wx.ComboBox(
            self,
            choices=[s[1] for s in self.STANDARDS],
            style=wx.CB_READONLY
        )
        self.standard_combo.SetSelection(0)
        sizer.Add(self.standard_combo, 0, wx.ALL | wx.EXPAND, 5)
        
        # Botão gerenciar padrões
        self.btn_manage_standards = wx.Button(self, label=_("Gerenciar &Padrões"))
        self.btn_manage_standards.Bind(wx.EVT_BUTTON, self.on_manage_standards)
        sizer.Add(self.btn_manage_standards, 0, wx.ALL, 5)
        
        self.SetSizer(sizer)
        
        # Carregar configurações salvas
        self.load_settings()
    
    def on_update_models(self, event):
        """Atualizar lista de modelos do provedor"""
        provider = self.get_provider()
        api_key = self.get_api_key()
        
        # TODO: Implementar chamada à API para listar modelos
        wx.MessageBox(_("Lista de modelos atualizada para {}").format(provider), _("Informação"))
    
    def on_manage_standards(self, event):
        """Gerenciar padrões acadêmicos"""
        # TODO: Abrir gerenciador de padrões
        wx.MessageBox(_("Gerenciador de padrões será aberto"), _("Informação"))
    
    def load_settings(self):
        """Carregar configurações salvas"""
        config_dir = os.path.join(os.path.dirname(__file__), "..", "..", "config")
        config_file = os.path.join(config_dir, "settings.json")
        
        if os.path.exists(config_file):
            try:
                with open(config_file, 'r', encoding='utf-8') as f:
                    settings = json.load(f)
                
                # Restaurar configurações
                if 'provider' in settings:
                    # TODO: Set provider combo
                    pass
                if 'api_key' in settings:
                    self.api_key_text.SetValue(settings['api_key'])
                if 'model' in settings:
                    # TODO: Set model combo
                    pass
                if 'standard' in settings:
                    # TODO: Set standard combo
                    pass
                    
            except Exception as e:
                pass  # Ignorar erros ao carregar
    
    def save_settings(self):
        """Salvar configurações"""
        config_dir = os.path.join(os.path.dirname(__file__), "..", "..", "config")
        os.makedirs(config_dir, exist_ok=True)
        
        config_file = os.path.join(config_dir, "settings.json")
        
        settings = {
            'provider': self.get_provider(),
            'api_key': self.get_api_key(),
            'model': self.get_model(),
            'standard': self.get_standard()
        }
        
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(settings, f, indent=2)
    
    def get_provider(self):
        """Obter provedor selecionado"""
        selection = self.provider_combo.GetSelection()
        return self.PROVIDERS[selection][0]
    
    def get_api_key(self):
        """Obter chave API"""
        return self.api_key_text.GetValue()
    
    def get_model(self):
        """Obter modelo selecionado"""
        return self.model_combo.GetValue()
    
    def get_standard(self):
        """Obter padrão acadêmico selecionado"""
        selection = self.standard_combo.GetSelection()
        return self.STANDARDS[selection][0]
