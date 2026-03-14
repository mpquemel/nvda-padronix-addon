# -*- coding: utf-8 -*-
"""
Padronix - Cliente REST Universal
Copyright (C) 2026 Melhym Pereira Quemel <mpquemel@gmail.com>

Cliente assíncrono para múltiplos provedores de IA usando urllib (nativo).
"""

from __future__ import annotations

import json
import ssl
import asyncio
from dataclasses import dataclass
from typing import Dict, Any, Optional, List
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
import addonHandler

addonHandler.initTranslation()

import logHandler


@dataclass
class AIResponse:
    """Resposta padronizada do cliente de IA."""
    success: bool
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    raw_response: Optional[str] = None


class AIClient:
    """
    Cliente unificado para provedores de IA.
    
    Suporta: Google Gemini, OpenAI, OpenRouter, Ollama Local.
    Todas as chamadas são assíncronas (não bloqueiam NVDA).
    """
    
    # Endpoints por provedor
    ENDPOINTS: Dict[str, str] = {
        "google": "https://generativelanguage.googleapis.com/v1beta/models",
        "openai": "https://api.openai.com/v1/chat/completions",
        "openrouter": "https://openrouter.ai/api/v1/chat/completions",
        "ollama": "http://localhost:11434/api/generate",
    }
    
    # Timeout padrão (segundos)
    DEFAULT_TIMEOUT: int = 60
    
    def __init__(self, provider: str, model: str, api_key: str) -> None:
        """
        Inicializa cliente de IA.
        
        Args:
            provider: Nome do provedor (google, openai, openrouter, ollama)
            model: Modelo específico
            api_key: Chave API (ou "ollama-local" para Ollama)
        """
        self.provider = provider
        self.model = model
        self.api_key = api_key
        self.endpoint = self.ENDPOINTS.get(provider, "")
        
        if not self.endpoint:
            raise ValueError(f"Provedor desconhecido: {provider}")
    
    async def structure_article(self, txt_content: str) -> AIResponse:
        """
        Estrutura artigo acadêmico usando IA.
        
        Args:
            txt_content: Texto bruto do artigo
            
        Returns:
            AIResponse com dados estruturados ou erro
        """
        prompt = self._build_prompt(txt_content)
        
        try:
            # Executar chamada de rede em thread separada
            result = await asyncio.to_thread(
                self._call_api,
                prompt
            )
            return result
            
        except asyncio.TimeoutError:
            logHandler.log.warning("Padronix: Timeout na chamada de IA")
            return AIResponse(
                success=False,
                error=_("A IA demorou muito para responder. Tente novamente.")
            )
            
        except Exception as e:
            logHandler.log.error(f"Padronix: Erro na chamada de IA: {e}")
            return AIResponse(
                success=False,
                error=_("Erro ao comunicar com a IA: {}").format(str(e))
            )
    
    def _build_prompt(self, txt_content: str) -> str:
        """
        Constrói prompt de estruturação.
        
        Args:
            txt_content: Texto do artigo
            
        Returns:
            Prompt formatado
        """
        max_length = 15000  # Limitar para não exceder tokens
        truncated_content = txt_content[:max_length]
        
        return f"""Você é um assistente especializado em estruturação de artigos acadêmicos.

Analise o texto abaixo e extraia a estrutura completa no formato JSON exato:

{{
    "title": "Título do artigo em português",
    "abstract": "Resumo em português (200-250 palavras)",
    "abstract_en": "Abstract in English (200-250 words)",
    "keywords": ["palavra-chave1", "palavra-chave2", "palavra-chave3", "palavra-chave4", "palavra-chave5"],
    "keywords_en": ["keyword1", "keyword2", "keyword3", "keyword4", "keyword5"],
    "sections": [
        {{
            "heading": "1. Introdução",
            "level": 1,
            "content": "Texto completo da seção..."
        }},
        {{
            "heading": "2. Revisão da Literatura",
            "level": 1,
            "content": "Texto completo da seção..."
        }},
        {{
            "heading": "2.1 Subseção",
            "level": 2,
            "content": "Texto da subseção..."
        }}
    ],
    "references": [
        "SOBRENOME, Nome. Título do livro. Editora, Ano.",
        "SOBRENOME, Nome; SOBRENOME2, Nome2. Título do artigo. Nome da Revista, v. X, n. Y, p. Z, Ano."
    ]
}}

REGRAS IMPORTANTES:
1. O JSON deve ser VÁLIDO e completo
2. Preserve o máximo do conteúdo original
3. Divida em seções lógicas (Introdução, Metodologia, Resultados, Conclusão, etc.)
4. Formate as referências no padrão ABNT quando possível
5. Se o texto estiver em inglês, adapte os campos adequadamente

TEXTO PARA ANÁLISE:

{truncated_content}

Retorne APENAS o JSON válido, sem markdown, sem explicações adicionais."""
    
    def _call_api(self, prompt: str) -> AIResponse:
        """
        Executa chamada HTTP síncrona (executada em thread).
        
        Args:
            prompt: Prompt para a IA
            
        Returns:
            AIResponse com resultado
        """
        # Rotear para método específico do provedor
        if self.provider == "google":
            return self._call_google(prompt)
        elif self.provider == "openai":
            return self._call_openai(prompt)
        elif self.provider == "openrouter":
            return self._call_openrouter(prompt)
        elif self.provider == "ollama":
            return self._call_ollama(prompt)
        else:
            return AIResponse(success=False, error=_("Provedor não implementado"))
    
    def _call_google(self, prompt: str) -> AIResponse:
        """Chama Google Gemini API."""
        url = f"{self.endpoint}/{self.model}:generateContent?key={self.api_key}"
        
        payload = {
            "contents": [{
                "parts": [{"text": prompt}]
            }],
            "generationConfig": {
                "temperature": 0.2,
                "maxOutputTokens": 4096,
            }
        }
        
        headers = {
            "Content-Type": "application/json"
        }
        
        return self._make_request(url, payload, headers)
    
    def _call_openai(self, prompt: str) -> AIResponse:
        """Chama OpenAI API."""
        url = self.endpoint
        
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": "Você é um assistente que retorna apenas JSON válido."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.2,
            "max_tokens": 8192,
        }
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        
        return self._make_request(url, payload, headers)
    
    def _call_openrouter(self, prompt: str) -> AIResponse:
        """Chama OpenRouter API."""
        url = self.endpoint
        
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": "Retorne apenas JSON válido."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.2,
            "max_tokens": 8192,
        }
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
            "HTTP-Referer": "https://github.com/mpquemel/padronix",
            "X-Title": "Padronix NVDA Add-on"
        }
        
        return self._make_request(url, payload, headers)
    
    def _call_ollama(self, prompt: str) -> AIResponse:
        """Chama Ollama Local."""
        url = self.endpoint
        
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "format": "json",
            "options": {
                "temperature": 0.2,
            }
        }
        
        headers = {
            "Content-Type": "application/json"
        }
        
        # Ollama não requer autenticação local
        return self._make_request(url, payload, headers, timeout=120)
    
    def _make_request(
        self,
        url: str,
        payload: Dict[str, Any],
        headers: Dict[str, str],
        timeout: int = None
    ) -> AIResponse:
        """
        Executa requisição HTTP.
        
        Args:
            url: Endpoint
            payload: Corpo da requisição
            headers: Cabeçalhos HTTP
            timeout: Timeout em segundos
            
        Returns:
            AIResponse processado
        """
        if timeout is None:
            timeout = self.DEFAULT_TIMEOUT
        
        try:
            # Preparar requisição
            data = json.dumps(payload).encode('utf-8')
            request = Request(url, data=data, headers=headers, method='POST')
            
            # SSL context seguro
            ssl_context = ssl.create_default_context()
            
            # Executar com timeout
            response = urlopen(request, context=ssl_context, timeout=timeout)
            
            # Ler resposta
            response_data = response.read().decode('utf-8')
            response_json = json.loads(response_data)
            
            # Extrair texto da resposta
            text_response = self._extract_text_from_response(response_json)
            
            # Tentar parsear como JSON
            try:
                structured_data = self._parse_json_response(text_response)
                return AIResponse(success=True, data=structured_data, raw_response=text_response)
            except json.JSONDecodeError as e:
                logHandler.log.warning(f"Padronix: IA retornou JSON inválido: {e}")
                return AIResponse(
                    success=False,
                    error=_("A IA retornou um formato inválido. Tente outro modelo."),
                    raw_response=text_response
                )
            
        except HTTPError as e:
            error_body = e.read().decode('utf-8') if hasattr(e, 'read') else str(e)
            logHandler.log.error(f"Padronix: Erro HTTP {e.code}: {error_body}")
            return AIResponse(
                success=False,
                error=_("Erro na comunicação com a IA (HTTP {}). Verifique sua chave API.").format(e.code)
            )
            
        except URLError as e:
            logHandler.log.error(f"Padronix: Erro de conexão: {e}")
            if self.provider == "ollama":
                return AIResponse(
                    success=False,
                    error=_("Ollama está offline. Execute 'ollama serve' no terminal.")
                )
            return AIResponse(
                success=False,
                error=_("Erro de conexão. Verifique sua internet.")
            )
            
        except Exception as e:
            logHandler.log.error(f"Padronix: Erro inesperado: {e}")
            return AIResponse(success=False, error=str(e))
    
    def _extract_text_from_response(self, response: Dict[str, Any]) -> str:
        """
        Extrai texto da resposta do provedor.
        
        Args:
            response: Resposta JSON do provedor
            
        Returns:
            Texto extraído
        """
        try:
            if self.provider == "google":
                # Formato Gemini
                return response["candidates"][0]["content"]["parts"][0]["text"]
                
            elif self.provider in ["openai", "openrouter"]:
                # Formato OpenAI/OpenRouter
                return response["choices"][0]["message"]["content"]
                
            elif self.provider == "ollama":
                # Formato Ollama
                return response["response"]
                
        except (KeyError, IndexError) as e:
            logHandler.log.error(f"Padronix: Erro ao extrair texto: {e}")
            raise ValueError("Formato de resposta inesperado")
        
        return ""
    
    def _parse_json_response(self, text: str) -> Dict[str, Any]:
        """
        Parseia texto JSON, removendo markdown se necessário.
        
        Args:
            text: Texto possivelmente com markdown
            
        Returns:
            Dicionário parseado
        """
        # Remover blocos markdown
        clean_text = text.strip()
        
        if "```json" in clean_text:
            clean_text = clean_text.split("```json")[1].split("```")[0]
        elif "```" in clean_text:
            clean_text = clean_text.split("```")[1].split("```")[0] if "```" in clean_text else clean_text
        
        clean_text = clean_text.strip()
        
        return json.loads(clean_text)
