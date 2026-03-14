# -*- coding: utf-8 -*-
"""
Padronix - Orquestração e Feedback
Copyright (C) 2026 Melhym Pereira Quemel <mpquemel@gmail.com>

Gerencia fluxo de trabalho, feedback auditivo e progresso.
"""

from __future__ import annotations

import asyncio
import wx
from typing import Optional, Dict, Any
from dataclasses import dataclass
from pathlib import Path
import addonHandler

addonHandler.initTranslation()

import config
import tones
import speech
import logHandler

from .ai_client import AIClient, AIResponse
from .docx_renderer import DocxRenderer


@dataclass
class ProcessingResult:
    """Resultado do processamento."""
    success: bool
    output_path: Optional[str] = None
    error_message: Optional[str] = None


class WorkflowManager:
    """
    Orquestra workflow completo de processamento.
    
    Responsabilidades:
    - Coordenar IA + Renderização
    - Fornecer feedback auditivo contínuo
    - Gerenciar exceções sem crashar NVDA
    """
    
    def __init__(self, dialog: Any) -> None:
        """
        Inicializa gerenciador de workflow.
        
        Args:
            dialog: Referência ao diálogo principal para callbacks
        """
        self.dialog = dialog
        self._is_processing: bool = False
        self._progress_timer: Optional[wx.Timer] = None
    
    def process(self, txt_content: str, json_content: str) -> None:
        """
        Inicia processamento assíncrono.
        
        Args:
            txt_content: Conteúdo TXT (se houver)
            json_content: Conteúdo JSON (se houver)
        """
        if self._is_processing:
            speech.speakMessage(_("Processamento já em andamento"))
            return
        
        self._is_processing = True
        
        # Iniciar feedback visual/sonoro
        self._start_progress_feedback()
        
        # Criar tarefa assíncrona
        asyncio.create_task(self._process_async(txt_content, json_content))
    
    async def _process_async(self, txt_content: str, json_content: str) -> None:
        """
        Processamento assíncrono principal.
        
        Executa em background sem bloquear NVDA.
        """
        try:
            # Obter configurações
            provider = config.conf["padronix"].get("provider", "google")
            model = config.conf["padronix"].get("model", "gemini-pro")
            api_key = config.conf["padronix"].get("api_key", "")
            standard = config.conf["padronix"].get("standard", "abnt")
            
            result = await self._execute_workflow(
                txt_content=txt_content,
                json_content=json_content,
                provider=provider,
                model=model,
                api_key=api_key,
                standard=standard
            )
            
            # Callback de conclusão
            if result.success:
                msg = _("Documento Padronix gerado em: {}").format(result.output_path)
            else:
                msg = _("Erro: {}").format(result.error_message)
            
            wx.CallAfter(self._on_complete, result.success, msg)
            
        except Exception as e:
            logHandler.log.error(f"Padronix: Erro inesperado no workflow: {e}")
            wx.CallAfter(self._on_complete, False, _("Erro interno. Verifique o log do NVDA."))
        
        finally:
            self._is_processing = False
            wx.CallAfter(self._stop_progress_feedback)
    
    async def _execute_workflow(
        self,
        txt_content: str,
        json_content: str,
        provider: str,
        model: str,
        api_key: str,
        standard: str
    ) -> ProcessingResult:
        """
        Executa workflow completo: IA -> JSON -> DOCX.
        
        Args:
            txt_content: Texto bruto do artigo
            json_content: JSON pré-estruturado
            provider: Provedor de IA
            model: Modelo específico
            api_key: Chave API
            standard: Padrão acadêmico
            
        Returns:
            ProcessingResult com caminho do arquivo ou erro
        """
        # === ETAPA 1: Estruturar com IA (se necessário) ===
        structured_data: Dict[str, Any]
        
        if json_content:
            # Usar JSON pré-estruturado
            import json
            structured_data = json.loads(json_content)
            
        elif txt_content:
            # Chamar IA para estruturar
            wx.CallAfter(speech.speakMessage, _("Estruturando artigo com IA..."))
            
            client = AIClient(provider, model, api_key)
            response: AIResponse = await client.structure_article(txt_content)
            
            if not response.success:
                return ProcessingResult(
                    success=False,
                    error_message=response.error
                )
            
            structured_data = response.data or {}
            
        else:
            return ProcessingResult(
                success=False,
                error_message=_("Nenhum conteúdo fornecido")
            )
        
        # === ETAPA 2: Renderizar DOCX ===
        wx.CallAfter(speech.speakMessage, _("Renderizando documento DOCX..."))
        
        try:
            renderer = DocxRenderer(standard)
            output_path = renderer.render(structured_data)
            
            return ProcessingResult(
                success=True,
                output_path=output_path
            )
            
        except Exception as e:
            logHandler.log.error(f"Padronix: Erro ao renderizar DOCX: {e}")
            return ProcessingResult(
                success=False,
                error_message=_("Erro ao gerar documento: {}").format(str(e))
            )
    
    def _start_progress_feedback(self) -> None:
        """Inicia feedback de progresso (beeps suaves)."""
        self._progress_count = 0
        self._progress_timer = wx.Timer(self.dialog)
        self.dialog.Bind(wx.EVT_TIMER, self._on_progress_tick, self._progress_timer)
        self._progress_timer.Start(3000)  # Beep a cada 3 segundos
    
    def _on_progress_tick(self, event: wx.TimerEvent) -> None:
        """Toca beep suave indicando atividade."""
        # Beep estéreo suave (880 Hz, 50ms)
        tones.beep(880, 50)
        self._progress_count += 1
    
    def _stop_progress_feedback(self) -> None:
        """Para feedback de progresso."""
        if self._progress_timer and self._progress_timer.IsRunning():
            self._progress_timer.Stop()
            self._progress_timer = None
    
    def _on_complete(self, success: bool, message: str) -> None:
        """Callback de conclusão."""
        if hasattr(self.dialog, 'on_processing_complete'):
            self.dialog.on_processing_complete(success, message)
