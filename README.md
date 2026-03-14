# ♿ Padronix - Estruturador de Artigos Acadêmicos com IA

Add-on para NVDA que automatiza a formatação de artigos acadêmicos em múltiplos padrões (ABNT, APA, IEEE) usando Inteligência Artificial.

<div align="center">

[![NVDA Certified](https://img.shields.io/badge/NVDA%20Certified-Expert%202025-green?style=for-the-badge)](https://certification.nvaccess.org/page/2)
[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-GPL%20v2-blue?style=for-the-badge)](LICENSE)

</div>

---

## 🎯 Objetivo

**Padronix** é um add-on para o leitor de telas NVDA que permite:
- Formatação automática de artigos acadêmicos
- Suporte a múltiplos padrões: ABNT, APA, IEEE, Vancouver, MLA
- Integração com IA (Google Gemini, OpenAI, OpenRouter, Ollama)
- Acessibilidade total para deficientes visuais

---

## ✨ Funcionalidades

### 📚 Padrões Suportados
- **ABNT NBR 6023**: Referências bibliográficas (brasileiro)
- **APA 7ª Edição**: American Psychological Association
- **IEEE**: Institute of Electrical and Electronics Engineers
- **Vancouver**: Medicina e ciências da saúde
- **MLA 9ª Edição**: Modern Language Association

### 🤖 Integração com IA
O add-on se conecta a múltiplos provedores:
- 🧠 **Google Gemini** (recomendado)
- 🤖 **OpenAI** GPT-4
- 🌐 **OpenRouter** (acesso a múltiplos modelos)
- 🏠 **Ollama** (modelos locais)

### 🛠️ Recursos de Acessibilidade
- Totalmente acessível via NVDA
- Atalhos de teclado personalizáveis
- Feedback sonoro e verbal
- Interface simplificada

---

## 📋 Requisitos

### Sistema
- Windows 10/11
- NVDA 2024.1 ou superior
- Python 3.8+ (para desenvolvimento)

### Dependências
```bash
# Python (desenvolvimento)
pip install wxPython
pip install requests
pip install google-generativeai  # Para Gemini
```

---

## 🚀 Instalação

### Método 1: Instalador (.nvda-addon)
1. Baixe o arquivo `.nvda-addon` na [página de releases](../../releases)
2. Execute o arquivo e confirme a instalação no NVDA
3. Reinicie o NVDA

### Método 2: Instalação Manual
1. Clone o repositório:
```bash
git clone https://github.com/mpquemel/nvda-padronix-addon.git
```

2. Instale as dependências:
```bash
cd nvda-padronix-addon
pip install -r requirements.txt
```

3. Execute o script de construção:
```bash
python create_addon.py
```

4. Instale o arquivo `.nvda-addon` gerado na pasta `build/`

---

## 🎮 Como Usar

### Atalhos Padrão
| Atalho | Função |
|--------|--------|
| `NVDA+Shift+P` | Abrir configurações do Padronix |
| `NVDA+Shift+F` | Formatar texto selecionado |
| `NVDA+Shift+C` | Converter referências |

### Fluxo de Uso
1. **Configurar IA**: Acesse NVDA > Preferências > Padronix > Configurar
2. **Selecionar Padrão**: Escolha o padrão desejado (ABNT, APA, etc.)
3. **Selecionar Texto**: Selecione o texto a ser formatado
4. **Aplicar**: Use o atalho `NVDA+Shift+F`

---

## 🏗️ Estrutura do Projeto

```
nvda-padronix-addon/
├── addon/
│   ├── globalPlugins/       # Plugins globais do NVDA
│   │   └── padronix/        # Código principal
│   ├── doc/                 # Documentação
│   └── locale/              # Traduções
├── build/                   # Arquivos de build
├── create_addon.py          # Script de construção
├── manifest.ini             # Manifesto do add-on
├── requirements.txt         # Dependências
└── README.md               # Este arquivo
```

---

## 👨‍💻 Desenvolvimento

### Configurar Ambiente
```bash
# Clone
gh repo clone mpquemel/nvda-padronix-addon
cd nvda-padronix-addon

# Instale dependências
pip install -r requirements.txt

# Execute o build
python create_addon.py
```

### Estrutura de Código
- **`globalPlugins/padronix/`**: Código principal do add-on
- **`addonDocs/`**: Documentação do usuário
- **`locale/`**: Traduções (pt_BR, en, es)

---

## 📚 Documentação

- 📖 [Guia de Instalação](INSTALACAO.md)
- ✅ [Checklist de Conformidade](CHECKLIST_CONFORMIDADE.md)
- 📦 [Bibliotecas Instaladas](LIBS_INSTALADAS.md)
- 🆘 [Documentação NVDA](https://www.nvaccess.org/download/)

---

## 👨‍💻 Autor

**Melhym Pereira Quemel**

- 🎓 Mestre em Direito (UNESA)
- 💻 Graduando em Engenharia de Software
- ✅ NVDA Certified Expert 2025 (Nº 00756)
- 📧 mpquemel@gmail.com
- 🌐 https://quemel.adv.br

---

## 🤝 Contribuição

Contribuições são bem-vindas! Especialmente:
- 🌍 Traduções para outros idiomas
- 📚 Novos padrões bibliográficos
- 🐛 Correções de bugs
- 💡 Sugestões de features

---

## 📄 Licença

Este projeto está licenciado sob a **GNU General Public License v2.0** - veja o arquivo [LICENSE](LICENSE) para detalhes.

---

## 🙏 Agradecimentos

- Comunidade NVDA Brasil
- NV Access (desenvolvedores do NVDA)
- Moonshot AI (Kimi K2.5)

---

<div align="center">

**Feito com 💙 para tornar a pesquisa acadêmica mais acessível.**

</div>
