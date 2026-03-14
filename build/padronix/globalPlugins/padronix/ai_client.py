# -*- coding: utf-8 -*-
# Padronix - NVDA Add-on for Academic Paper Formatting
# Copyright (C) 2026 Melhym Pereira Quemel
# Email: mpquemel@gmail.com

"""Cliente de IA para múltiplos provedores"""

import json
import requests
import addonHandler
addonHandler.initTranslation()

class AIClient:
    """Cliente unificado para provedores de IA"""
    
    def __init__(self, provider, model, api_key):
        self.provider = provider
        self.model = model
        self.api_key = api_key
        
        self.endpoints = {
            'google': 'https://generativelanguage.googleapis.com/v1beta/models',
            'openai': 'https://api.openai.com/v1/chat/completions',
            'openrouter': 'https://openrouter.ai/api/v1/chat/completions',
            'ollama': 'http://localhost:11434/api/generate'
        }
    
    def structure_article(self, txt_content):
        """Estruturar artigo usando IA"""
        
        prompt = f"""
Você é um assistente especializado em estruturação de artigos acadêmicos.

Analise o texto abaixo e extraia a estrutura completa no formato JSON:

{{
    "title": "Título do artigo",
    "abstract": "Resumo em português",
    "abstract_en": "Abstract in English",
    "keywords": ["palavra1", "palavra2", "palavra3"],
    "keywords_en": ["keyword1", "keyword2", "keyword3"],
    "sections": [
        {{
            "heading": "1. Introdução",
            "level": 1,
            "content": "Texto da seção..."
        }}
    ],
    "references": [
        "Referência 1 formatada",
        "Referência 2 formatada"
    ]
}}

TEXTO PARA ANÁLISE:
{txt_content[:15000]}  # Limitar para não exceder tokens

Retorne APENAS o JSON válido, sem markdown ou explicações.
"""
        
        if self.provider == 'google':
            return self._call_google(prompt)
        elif self.provider == 'openai':
            return self._call_openai(prompt)
        elif self.provider == 'openrouter':
            return self._call_openrouter(prompt)
        elif self.provider == 'ollama':
            return self._call_ollama(prompt)
        else:
            raise ValueError(f"Provedor desconhecido: {self.provider}")
    
    def _call_google(self, prompt):
        """Chamar Google Gemini API"""
        url = f"{self.endpoints['google']}/{self.model}:generateContent?key={self.api_key}"
        
        payload = {
            "contents": [{
                "parts": [{"text": prompt}]
            }]
        }
        
        response = requests.post(url, json=payload, timeout=60)
        response.raise_for_status()
        
        result = response.json()
        text = result['candidates'][0]['content']['parts'][0]['text']
        
        # Extrair JSON do texto
        return self._extract_json(text)
    
    def _call_openai(self, prompt):
        """Chamar OpenAI API"""
        url = self.endpoints['openai']
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": "Você é um assistente que retorna apenas JSON válido."},
                {"role": "user", "content": prompt}
            ],
            "response_format": {"type": "json_object"}
        }
        
        response = requests.post(url, json=payload, headers=headers, timeout=60)
        response.raise_for_status()
        
        result = response.json()
        text = result['choices'][0]['message']['content']
        
        return json.loads(text)
    
    def _call_openrouter(self, prompt):
        """Chamar OpenRouter API"""
        url = self.endpoints['openrouter']
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://github.com/mpquemel/padronix"
        }
        
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": "Retorne apenas JSON válido."},
                {"role": "user", "content": prompt}
            ]
        }
        
        response = requests.post(url, json=payload, headers=headers, timeout=60)
        response.raise_for_status()
        
        result = response.json()
        text = result['choices'][0]['message']['content']
        
        return self._extract_json(text)
    
    def _call_ollama(self, prompt):
        """Chamar Ollama local"""
        url = self.endpoints['ollama']
        
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "format": "json"
        }
        
        response = requests.post(url, json=payload, timeout=120)
        response.raise_for_status()
        
        result = response.json()
        text = result['response']
        
        return json.loads(text)
    
    def _extract_json(self, text):
        """Extrair JSON de texto que pode conter markdown"""
        # Remover blocos markdown
        if "```json" in text:
            text = text.split("```json")[1].split("```")[0]
        elif "```" in text:
            text = text.split("```")[1].split("```")[0]
        
        return json.loads(text.strip())
