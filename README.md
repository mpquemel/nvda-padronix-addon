# 📚 NVDA Padronix
### IA para Formatação Acadêmica Acessível

O **NVDA Padronix** é um add-on especializado para o leitor de telas NVDA que automatiza a formatação de referências bibliográficas e artigos acadêmicos, utilizando Inteligência Artificial para garantir a conformidade com os padrões mais rigorosos de escrita científica.

---

## 🎯 O Problema
A formatação de referências bibliográficas (ABNT, APA, IEEE, etc.) é uma das tarefas mais tediosas e propensas a erros na escrita acadêmica. Para pessoas com deficiência visual, conferir cada vírgula, itálico ou ponto final em uma norma técnica complexa é um desafio imenso, tornando o processo lento e exaustivo.

## 💡 A Solução
O Padronix utiliza a potência dos LLMs para analisar textos brutos e transformá-los instantaneamente em referências normatizadas. Ele não apenas "troca letras", mas entende a estrutura da obra (autor, título, editora, ano) e aplica a norma escolhida com precisão cirúrgica.

### ✨ Funcionalidades Principais
- **Suporte Multireferencial:** Formatação automática para **ABNT, APA, IEEE, Vancouver e MLA**.
- **Integração com Grandes Modelos:** Conexão com Google Gemini (Sugerido), OpenAI, OpenRouter e Ollama local.
- **Fluxo de Trabalho Integrado:** O usuário seleciona o texto no documento e aplica a formatação via atalho, sem precisar abrir sites externos.
- **Acessibilidade Nativa:** Desenvolvido especificamente para o NVDA, com feedback sonoro e interface simplificada.

---

## 🛠️ Guia de Instalação

### Usuários (Instalação Rápida)
1. Baixe o arquivo `.nvda-addon` na [página de releases](/mpquemel/nvda-padronix-addon/releases).
2. Execute o arquivo e confirme a instalação no NVDA.
3. Reinicie o NVDA.

### Desenvolvedores (Build do Código)
```bash
# Clone o repositório
git clone https://github.com/mpquemel/nvda-padronix-addon.git
cd nvda-padronix-addon

# Instale as dependências
pip install -r requirements.txt

# Gere o arquivo do add-on
python create_addon.py
```

---

## ⌨️ Comandos e Atalhos

| Atalho | Função |
|--------|---------|
| **NVDA + Shift + P** | Abrir configurações do Padronix |
| **NVDA + Shift + F** | Formatar texto selecionado |
| **NVDA + Shift + C** | Converter referências |

---

## 📂 Estrutura do Projeto
- `addon/globalPlugins/padronix/`: Núcleo lógico e integração com a API de IA.
- `doc/`: Manuais de usuário e guias de conformidade.
- `locale/`: Suporte a múltiplos idiomas (pt_BR, en, es).

---

## 📜 Licença e Créditos
Este projeto está licenciado sob a **GNU General Public License v2.0**.
Desenvolvido por **Melhym Pereira Quemel**, NVDA Certified Expert.

Tornando a pesquisa acadêmica verdadeiramente inclusiva. 🎓
