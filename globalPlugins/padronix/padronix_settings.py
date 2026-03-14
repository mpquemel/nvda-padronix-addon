# -*- coding: utf-8 -*-
"""
Padronix - Motor de Configurações
Copyright (C) 2026 Melhym Pereira Quemel <mpquemel@gmail.com>

Módulo responsável pela integração com config.conf do NVDA.
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Optional, List, Dict, Any, Callable, TYPE_CHECKING

import wx
import config
import gui
from gui import guiHelper
from gui.settingsDialogs import SettingsPanel
import addonHandler

addonHandler.initTranslation()

# Tipos
ProviderType = str
ModelType = str
StandardType = str

class PadronixSettingsPanel(SettingsPanel):
    """
    Painel de configurações do Padronix integrado ao NVDA.
    
    Segue o padrão SettingsPanel do NVDA 2026 para máxima compatibilidade.
    
    Rota A: Agora herda SettingsPanel diretamente, removendo delegação through
    PadronixSettingsCategory wrapper.
    """
    
    # Configuração do NVDA SettingsPanel
    title: str = "Padronix"
    
    # Configurações dos provedores
    PROVIDERS: List[tuple[str, str]] = [
        ("google", _("Google Gemini")),
        ("openai", _("OpenAI")),
        ("openrouter", _("OpenRouter")),
        ("ollama", _("Ollama Local (100% offline)")),
    ]
    
    # Modelos padrão por provedor
    DEFAULT_MODELS: Dict[str, List[str]] = {
        "google": ["gemini-pro", "gemini-1.5-pro", "gemini-1.5-flash"],
        "openai": ["gpt-4-turbo", "gpt-4", "gpt-3.5-turbo"],
        "openrouter": [
            "anthropic/claude-3-sonnet",
            "meta-llama/llama-3-70b-instruct",
            "google/gemini-pro-1.5",
            "mistralai/mistral-large"
        ],
        "ollama": ["llama3", "mistral", "codellama", "gemma:7b"],
    }
    
    # Padrões acadêmicos
    STANDARDS: List[tuple[str, str]] = [
        ("abnt", _("ABNT (Brasil)")),
        ("apa", _("APA (EUA/Psicologia)")),
        ("ieee", _("IEEE (Engenharia)")),
        ("chicago", _("Chicago (Humanidades)")),
        ("harvard", _("Harvard (Economia)")),
        ("mla", _("MLA (Literatura)")),
        ("vancouver", _("Vancouver (Medicina)")),
    ]
    
    def __init__(self, parent: wx.Window) -> None:
        """
        Inicializa o painel de configurações.
        
        Args:
            parent: Janela pai (wx.Panel ou wx.Window)
        """
        # Rota A: Chama super().__init__() corretamente para SettingsPanel
        super().__init__(parent)
        self._create_ui()
        self._load_settings()
    
    def makeSettings(self, settingsSizer: wx.BoxSizer) -> None:
        """
        Constroi UI do painel.
        
        Método obrigatório de SettingsPanel do NVDA 2026.
        """
        helper = guiHelper.BoxSizerHelper(self, sizer=settingsSizer)
        
        # === SEÇÃO: Provedor de IA ===
        helper.addItem(wx.StaticText(self, label=_("Provedor de IA:")))
        self.provider_combo = wx.ComboBox(
            self,
            choices=[p[1] for p in self.PROVIDERS],
            style=wx.CB_READONLY
        )
        self.provider_combo.Bind(wx.EVT_COMBOBOX, self._on_provider_change)
        helper.addItem(self.provider_combo)
        
        # === SEÇÃO: Chave API ===
        helper.addItem(wx.StaticText(self, label=_("Chave API:")))
        self.api_key_text = wx.TextCtrl(
            self,
            style=wx.TE_PASSWORD,
            size=wx.Size(400, -1)
        )
        helper.addItem(self.api_key_text)
        
        # Nota sobre Ollama
        self.ollama_note = wx.StaticText(
            self,
            label=_("Nota: Para Ollama local, deixe a chave em branco ou use 'ollama-local'")
        )
        self.ollama_note.SetForegroundColour(wx.Colour(128, 128, 128))
        helper.addItem(self.ollama_note)
        
        # === BOTÃO: Atualizar Modelos ===
        self.btn_update_models = wx.Button(
            self,
            label=_("&Atualizar Lista de Modelos")
        )
        self.btn_update_models.Bind(wx.EVT_BUTTON, self._on_update_models)
        helper.addItem(self.btn_update_models)
        
        # === SEÇÃO: Modelo ===
        helper.addItem(wx.StaticText(self, label=_("Modelo:")))
        self.model_combo = wx.ComboBox(
            self,
            style=wx.CB_READONLY,
            size=wx.Size(400, -1)
        )
        helper.addItem(self.model_combo)
        
        # === SEÇÃO: Padrão Acadêmico ===
        helper.addItem(wx.StaticText(self, label=_("Padrão Acadêmico:")))
        self.standard_combo = wx.ComboBox(
            self,
            choices=[s[1] for s in self.STANDARDS],
            style=wx.CB_READONLY
        )
        helper.addItem(self.standard_combo)
        
        # === BOTÃO: Gerenciar Padrões ===
        self.btn_manage_standards = wx.Button(
            self,
            label=_("Gerenciar &Padrões")
        )
        self.btn_manage_standards.Bind(wx.EVT_BUTTON, self._on_manage_standards)
        helper.addItem(self.btn_manage_standards)
        
        # Espaçador final
        helper.addItem(wx.StaticText(self, label=""))
    
    def onSave(self) -> None:
        """
        Salva configurações no config.conf.
        
        Método obrigatório de SettingsPanel do NVDA 2026.
        Chamado quando usuário clica em OK.
        """
        self.save_settings()
    
    def onDiscard(self) -> None:
        """
        Descarta mudanças.
        
        Método obrigatório de SettingsPanel do NVDA 2026.
        """
        # Recarregar configurações originais
        self._load_settings()
    
    def _create_ui(self) -> None:
        """Cria interface do painel usando guiHelper."""
        # O UI já é criado em makeSettings(), este método é mantido para compatibilidade
        pass
    
    def _on_provider_change(self, event: wx.Event) -> None:
        """
        Callback quando o provedor muda.
        
        Atualiza lista de modelos padrão para o novo provedor.
        """
        provider = self.get_provider()
        models = self.DEFAULT_MODELS.get(provider, [])
        
        self.model_combo.Clear()
        self.model_combo.AppendItems(models)
        
        if models:
            self.model_combo.SetSelection(0)
        
        # Feedback auditivo
        import speech
        # Rota A: F-string convertida para .format()
        speech.speakMessage(
            _("Provedor {} selecionado. {} modelos disponíveis.").format(provider, len(models))
        )
    
    def _on_update_models(self, event: wx.Event) -> None:
        """
        Callback para atualizar lista de modelos via API.
        
        Executa chamada assíncrona para obter modelos disponíveis.
        """
        provider = self.get_provider()
        api_key = self.get_api_key()
        
        # Feedback imediato
        import speech
        # Rota A: F-string convertida para .format()
        speech.speakMessage(_("Atualizando modelos do {}...").format(provider))
        
        # Desabilitar botão temporariamente
        self.btn_update_models.Enable(False)
        
        # Usar CallLater para não bloquear UI
        wx.CallLater(100, self._fetch_models_async, provider, api_key)
    
    def _fetch_models_async(self, provider: str, api_key: str) -> None:
        """
        Busca modelos disponíveis de forma assíncrona.
        
        Args:
            provider: Nome do provedor
            api_key: Chave API
        """
        try:
            # TODO: Implementar chamada real à API
            # Por enquanto, usa modelos padrão
            models = self.DEFAULT_MODELS.get(provider, [])
            
            # Atualizar UI na thread principal
            wx.CallAfter(self._update_models_list, models)
            
        except (ImportError, AttributeError, RuntimeError, KeyError) as e:
            import logHandler
            # Rota A: except específico
            logHandler.log.error(f"Padronix: Erro ao buscar modelos: {e}")
            wx.CallAfter(self._show_error, str(e))
        
        finally:
            wx.CallAfter(self.btn_update_models.Enable, True)
    
    def _update_models_list(self, models: List[str]) -> None:
        """Atualiza lista de modelos na UI."""
        self.model_combo.Clear()
        self.model_combo.AppendItems(models)
        
        if models:
            self.model_combo.SetSelection(0)
            import speech
            # Rota A: F-string convertida para .format()
            speech.speakMessage(_("{} modelos atualizados").format(len(models)))
    
    def _show_error(self, message: str) -> None:
        """Mostra erro ao usuário."""
        import speech
        # Rota A: F-string convertida para .format()
        speech.speakMessage(_("Erro: {}").format(message))
    
    def _on_manage_standards(self, event: wx.Event) -> None:
        """Abre gerenciador de padrões acadêmicos."""
        # TODO: Implementar gerenciador de padrões
        import speech
        speech.speakMessage(_("Gerenciador de padrões será implementado em versão futura"))
    
    def _load_settings(self) -> None:
        """Carrega configurações do config.conf do NVDA."""
        try:
            # Provedor
            provider = config.conf["padronix"].get("provider", "google")
            for i, (key, _) in enumerate(self.PROVIDERS):
                if key == provider:
                    self.provider_combo.SetSelection(i)
                    break
            
            # API Key
            api_key = config.conf["padronix"].get("api_key", "")
            self.api_key_text.SetValue(api_key)
            
            # Modelo
            model = config.conf["padronix"].get("model", "")
            self._update_models_list(self.DEFAULT_MODELS.get(provider, []))
            if model:
                idx = self.model_combo.FindString(model)
                if idx != wx.NOT_FOUND:
                    self.model_combo.SetSelection(idx)
            elif self.model_combo.GetCount() > 0:
                self.model_combo.SetSelection(0)
            
            # Padrão
            standard = config.conf["padronix"].get("standard", "abnt")
            for i, (key, _) in enumerate(self.STANDARDS):
                if key == standard:
                    self.standard_combo.SetSelection(i)
                    break
                    
        except (ImportError, AttributeError, RuntimeError, KeyError) as e:
            import logHandler
            # Rota A: except específico
            logHandler.log.error(f"Padronix: Erro ao carregar configurações: {e}")
    
    def save_settings(self) -> None:
        """
        Salva configurações no config.conf do NVDA.
        
        Chamado automaticamente pelo NVDA quando usuário clica OK.
        """
        try:
            config.conf["padronix"]["provider"] = self.get_provider()
            config.conf["padronix"]["api_key"] = self.get_api_key()
            config.conf["padronix"]["model"] = self.get_model()
            config.conf["padronix"]["standard"] = self.get_standard()
            
            import logHandler
            logHandler.log.info("Padronix: Configurações salvas com sucesso")
            
        except (ImportError, AttributeError, RuntimeError, KeyError) as e:
            import logHandler
            # Rota A: except específico
            logHandler.log.error(f"Padronix: Erro ao salvar configurações: {e}")
    
    # === GETTERS ===
    
    def get_provider(self) -> ProviderType:
        """Retorna provedor selecionado."""
        selection = self.provider_combo.GetSelection()
        if selection >= 0:
            return self.PROVIDERS[selection][0]
        return "google"
    
    def get_api_key(self) -> str:
        """Retorna chave API."""
        return self.api_key_text.GetValue().strip()
    
    def get_model(self) -> ModelType:
        """Retorna modelo selecionado."""
        return self.model_combo.GetValue()
    
    def get_standard(self) -> StandardType:
        """Retorna padrão acadêmico selecionado."""
        selection = self.standard_combo.GetSelection()
        if selection >= 0:
            return self.STANDARDS[selection][0]
        return "abnt"
