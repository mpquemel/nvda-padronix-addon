# 📦 Padronix - Guia de Instalação Completa

**Versão:** 2026.1.0  
**Autor:** Melhym Pereira Quemel  
**Email:** mpquemel@gmail.com  
**GitHub:** https://github.com/mpquemel/padronix

---

## 🔧 Pré-requisitos

1. **NVDA 2024.1 ou superior** instalado
2. **Windows 10 ou 11**
3. **Acesso de administrador** (para instalar dependências)

---

## 📋 Passo a Passo de Instalação

### Passo 1: Instalar Dependências do Python

O Padronix precisa de duas bibliotecas Python:

```bash
python-docx  (para criar documentos Word)
requests     (para comunicar com APIs de IA)
```

#### Opção A: Usar o script automático (Recomendado)

1. Abra o **Prompt de Comando como Administrador**
2. Navegue até a pasta do Padronix:
   ```
   cd C:\Users\mpque\.openclaw\workspace\padronix
   ```
3. Execute o instalador:
   ```
   install_dependencies.bat
   ```

O script vai:
- Detectar se o NVDA é 32-bit ou 64-bit
- Instalar as bibliotecas na pasta correta do Python do NVDA
- Verificar se tudo funcionou

#### Opção B: Instalação manual

Se preferir fazer manualmente:

**Para NVDA 64-bit:**
```bash
"C:\Program Files\NVDA\python\python.exe" -m pip install python-docx requests
```

**Para NVDA 32-bit:**
```bash
"C:\Program Files (x86)\NVDA\python\python.exe" -m pip install python-docx requests
```

### Passo 2: Criar o Pacote .nvda-addon

1. No Prompt de Comando (não precisa ser administrador):
   ```
   cd C:\Users\mpque\.openclaw\workspace\padronix
   ```

2. Execute o criador de pacotes:
   ```
   python create_addon.py
   ```

3. Aguarde a mensagem:
   ```
   SUCCESSO! Add-on criado: padronix-2026.1.0.nvda-addon
   ```

### Passo 3: Instalar no NVDA

1. **Com o NVDA aberto**, pressione `NVDA+N` para abrir o menu

2. Navegue até:
   ```
   Ferramentas → Gerenciar Complementos
   ```
   Ou use o atalho: `NVDA+Shift+F1`

3. Pressione `I` para **Instalar**

4. Navegue até o arquivo:
   ```
   C:\Users\mpque\.openclaw\workspace\padronix\padronix-2026.1.0.nvda-addon
   ```

5. Pressione `Enter` para confirmar

6. Quando perguntado se deseja reiniciar o NVDA:
   - Pressione `Tab` até "Sim"
   - Pressione `Enter`

### Passo 4: Verificar Instalação

Após o NVDA reiniciar:

1. Pressione `NVDA+Ctrl+Shift+F`

2. Você deve ouvir: **"Padronix aberto"**

3. Se ouvir isso, **instalação concluída com sucesso!** 🎉

---

## 🐛 Solução de Problemas

### "Erro ao abrir Padronix"

**Causa:** Dependências não instaladas corretamente

**Solução:**
```bash
# Verificar se python-docx está instalado
python -c "import docx; print('OK')"

# Se der erro, reinstalar:
pip install python-docx requests
```

### "Módulo docx não encontrado"

**Causa:** Bibliotecas instaladas no Python do sistema, não do NVDA

**Solução:**
```bash
# Usar o Python do NVDA explicitamente:
"C:\Program Files\NVDA\python\python.exe" -m pip install python-docx requests
```

### "Ollama offline"

**Causa:** Ollama não está rodando

**Solução:**
1. Abra o Prompt de Comando
2. Digite: `ollama serve`
3. Deixe a janela aberta enquanto usa o Padronix

---

## 📁 Estrutura de Arquivos

Após a instalação, o Padronix fica organizado assim:

```
padronix-2026.1.0.nvda-addon (ZIP)
├── manifest.ini
├── globalPlugins/
│   ├── padronix/
│   │   ├── __init__.py
│   │   ├── main_dialog.py
│   │   ├── padronix_settings.py
│   │   ├── workflow_manager.py
│   │   ├── ai_client.py
│   │   └── docx_renderer.py
│   └── lib/ (dependências)
├── doc/
│   ├── pt_BR/readme.html
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
│   └── ...
└── locale/
    ├── pt_BR/LC_MESSAGES/padronix.po
    ├── en/LC_MESSAGES/padronix.po
    └── ...
```

---

## 🔑 Obtendo Chaves de API

### Google Gemini (Gratuito)

1. Acesse: https://makersuite.google.com/app/apikey
2. Faça login com conta Google
3. Clique em "Create API Key"
4. Copie a chave (começa com `AIza...`)

### OpenAI (Pago)

1. Acesse: https://platform.openai.com/api-keys
2. Crie conta ou faça login
3. Clique em "+ Create new secret key"
4. Copie imediatamente (começa com `sk-proj-...`)

### OpenRouter (Múltiplos modelos)

1. Acesse: https://openrouter.ai/keys
2. Faça login
3. Clique em "Create Key"
4. Copie a chave (começa com `sk-or-...`)

### Ollama (Local e Gratuito)

1. Baixe em: https://ollama.ai/download
2. Instale
3. No Prompt de Comando:
   ```
   ollama pull llama3
   ```
4. Não precisa de chave API!

---

## 📞 Suporte

- **GitHub Issues:** https://github.com/mpquemel/padronix/issues
- **Email:** mpquemel@gmail.com
- **Documentação:** Pressione `NVDA+Ctrl+Shift+F` → Botão "Ajuda"

---

## 📜 Licença

GPL-3.0 - Software Livre

Desenvolvido com ♿ para ♿ por Melhym Pereira Quemel
