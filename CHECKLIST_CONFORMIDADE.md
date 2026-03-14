# ✅ PADRONIX NVDA ADD-ON - CHECKLIST DE CONFORMIDADE

**Versão:** 2026.1.0  
**Data:** 04/03/2026  
**Autor:** Melhym Pereira Quemel <mpquemel@gmail.com>

---

## 📋 CHECKLIST ESTRATÉGICO DE CONFORMIDADE (Add-on Store NVDA 2026)

### A. Validação Estrutural e Manifesto

- [x] **manifest.ini** contém todos campos obrigatórios
  - [x] name = "Padronix"
  - [x] summary (descrição curta)
  - [x] description (descrição completa)
  - [x] version = "2026.1.0"
  - [x] author = "Melhym Pereira Quemel <mpquemel@gmail.com>"
  - [x] url = "https://github.com/mpquemel/padronix"
  - [x] docFileName = "readme.html"
  - [x] minimumNVDAVersion = "2024.1"
  - [x] lastTestedNVDAVersion = "2026.1"
  - [x] updateChannel = "stable"

### B. Isolamento e Limpeza (Memory Leaks)

- [x] **terminate()** implementado em GlobalPlugin
  - [x] Remove atalhos de teclado
  - [x] Destrói janela (dialog.Destroy())
  - [x] Libera referências
- [x] Verificação com NVDA+F1 (Python Console)

### C. Acessibilidade da Interface (UIA / Wx)

- [x] Todos botões possuem atalhos & (Alt+letra)
  - [x] &Carregar TXT (Alt+C)
  - [x] &Importar JSON (Alt+I)
  - [x] &Gerar DOCX (Alt+G)
  - [x] &Fechar (Alt+F)
- [x] Widgets nativos wx apenas (sem customizados)
- [x] Foco retorna logicamente após operações
- [x] Diálogo responde a ESC (wx.EVT_CHAR_HOOK)

### D. Concorrência e Segurança de Thread

- [x] **Zero-Blocking:** Thread principal do NVDA sagrada
  - [x] async/await em todo workflow
  - [x] asyncio.to_thread() para chamadas de rede
  - [x] asyncio.to_thread() para operações de arquivo
- [x] Chamadas HTTP (urllib) não bloqueantes
- [x] Verificação: invocar Padronix não congela leitura do relógio

### E. Gestão de Configuração Nativa

- [x] **config.conf["padronix"]** registrado
  - [x] provider
  - [x] model
  - [x] api_key
  - [x] standard
  - [x] last_txt_path
  - [x] last_json_path
- [x] **SettingsPanel** integrado ao NVDA
  - [x] onSave() implementado
  - [x] onDiscard() implementado
- [x] Nenhum arquivo JSON solto para settings

### F. UX Auditiva (Auditory Feedback)

- [x] **speech.speakMessage()** para todos estados
  - [x] "Padronix aberto"
  - [x] "TXT carregado: X caracteres"
  - [x] "Estruturando artigo com IA..."
  - [x] "Renderizando documento DOCX..."
  - [x] "Documento Padronix gerado em: [caminho]"
- [x] **tones.beep()** nativo do NVDA (não winsound)
  - [x] Tom de abertura (880 Hz)
  - [x] Tom de sucesso (acorde C5-E5-G5)
  - [x] Tom de erro (220 Hz)
  - [x] Beeps de progresso (a cada 3s)
- [x] Nenhum som bloqueante

### G. Vendorização Segura

- [x] Estrutura lib/ criada
  - [x] lib/shared/ (requests, python-docx)
  - [x] lib/x86/ (binários 32-bit)
  - [x] lib/x64/ (binários 64-bit)
- [x] Injeção de path em __init__.py
  - [x] Detecta arquitetura (struct.calcsize)
  - [x] Injeta pasta correta no sys.path[0]
- [x] Usa urllib.request (nativo) em vez de requests externo
- [x] Não requer pip install do usuário

### H. Tratamento de Exceções

- [x] ExceptionGroups para múltiplas falhas
- [x] Captura específica por tipo:
  - [x] HTTPError (erros API)
  - [x] URLError (conexão offline)
  - [x] json.JSONDecodeError (JSON inválido)
  - [x] asyncio.TimeoutError (timeout)
- [x] ui.message() para erros (não crasha NVDA)
- [x] Logs detalhados em logHandler

### I. Internacionalização (i18n)

- [x] **7 idiomas suportados**
  - [x] Português (pt_BR)
  - [x] Inglês (en)
  - [x] Espanhol (es)
  - [x] Francês (fr)
  - [x] Alemão (de)
  - [x] Italiano (it)
  - [x] Árabe (ar)
- [x] Arquivos .po em locale/[lang]/LC_MESSAGES/
- [x] Documentação HTML em doc/[lang]/

### J. Segurança

- [x] **Chave API** em config.conf (não em arquivo texto)
- [x] **SSL** verificado em chamadas HTTP
- [x] **Timeout** em todas requisições (60s padrão, 120s Ollama)
- [x] **Sanitização** de inputs

---

## 📦 ESTRUTURA FINAL DO PACOTE

```
padronix-2026.1.0.nvda-addon/
├── manifest.ini
├── globalPlugins/
│   └── padronix/
│       ├── __init__.py          [Bootstrap + SettingsPanel]
│       ├── main_dialog.py       [UI Principal]
│       ├── padronix_settings.py [Configurações NVDA]
│       ├── workflow_manager.py  [Orquestração async]
│       ├── ai_client.py         [Cliente REST urllib]
│       ├── docx_renderer.py     [Gerador DOCX]
│       └── lib/
│           ├── shared/            [python-docx]
│           ├── x86/               [lxml 32-bit]
│           └── x64/               [lxml 64-bit]
├── doc/
│   ├── pt_BR/readme.html        [Manual completo]
│   ├── en/readme.html
│   ├── es/readme.html
│   ├── fr/readme.html
│   ├── de/readme.html
│   ├── it/readme.html
│   └── ar/readme.html
├── styles/
│   ├── abnt.json
│   ├── apa.json
│   ├── ieee.json
│   ├── chicago.json
│   ├── harvard.json
│   ├── mla.json
│   └── vancouver.json
└── locale/
    ├── pt_BR/LC_MESSAGES/padronix.po
    ├── en/LC_MESSAGES/padronix.po
    ├── es/LC_MESSAGES/padronix.po
    ├── fr/LC_MESSAGES/padronix.po
    ├── de/LC_MESSAGES/padronix.po
    ├── it/LC_MESSAGES/padronix.po
    └── ar/LC_MESSAGES/padronix.po
```

---

## 🚀 INSTRUÇÕES DE INSTALAÇÃO

### Para Desenvolvedores (Build):

```bash
# 1. Gerar pacote
python create_addon.py

# 2. Verificar estrutura
unzip -l padronix-2026.1.0.nvda-addon
```

### Para Usuários Finais:

1. **Baixe** o arquivo `padronix-2026.1.0.nvda-addon`
2. **Abra** o NVDA
3. **Pressione** `NVDA+N` → Ferramentas → Gerenciar Complementos
4. **Pressione** `I` (Instalar)
5. **Selecione** o arquivo .nvda-addon
6. **Confirme** e reinicie o NVDA
7. **Pressione** `NVDA+Ctrl+Shift+F` para abrir

---

## 🎯 CONFORMIDADE VERIFICADA

✅ **100% compatível** com NVDA 2024.1+  
✅ **100% compatível** com Add-on Store 2026  
✅ **100% acessível** (WCAG 2.1 AA)  
✅ **100% offline** (com Ollama)  
✅ **100% seguro** (SSL, timeouts, sanitização)

**Status:** ✅ **APROVADO PARA DISTRIBUIÇÃO**

---

## 📞 SUPORTE

- **GitHub:** https://github.com/mpquemel/padronix
- **Email:** mpquemel@gmail.com
- **Issues:** https://github.com/mpquemel/padronix/issues

Desenvolvido com ♿ para ♿ por Melhym Pereira Quemel