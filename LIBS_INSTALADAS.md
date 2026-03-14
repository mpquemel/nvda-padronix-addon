# 📦 Dependências Vendorizadas do Padronix

**Data da Instalação:** 2026-03-05  
**Python Target:** 3.13.2 (64-bit)  
**Comando Executado:** `pip install python-docx --target lib\shared --upgrade`

---

## 📁 Estrutura de Pastas

```
padronix/lib/
├── shared/          # Bibliotecas puras Python (multi-arquitetura)
│   ├── docx/        # python-docx 1.2.0
│   ├── lxml/        # lxml 6.0.2 (código Python)
│   └── typing_extensions.py
├── x64/             # Binários 64-bit (lxml .pyd)
│   ├── builder.cp313-win_amd64.pyd
│   ├── etree.cp313-win_amd64.pyd
│   ├── objectify.cp313-win_amd64.pyd
│   ├── sax.cp313-win_amd64.pyd
│   └── _elementpath.py
└── x86/             # (vazio - para futura compilação 32-bit)
```

---

## 📦 Pacotes Instalados

| Pacote | Versão | Localização | Tipo |
|--------|--------|-------------|------|
| **python-docx** | 1.2.0 | `lib/shared/docx/` | Puro Python |
| **lxml** | 6.0.2 | `lib/shared/lxml/` + `lib/x64/` | Misto (Python + binários) |
| **typing_extensions** | 4.15.0 | `lib/shared/typing_extensions.py` | Puro Python |

---

## 🔧 Binários Movidos para `lib/x64/`

Os seguintes arquivos `.pyd` (extensões C compiladas) foram movidos para `lib/x64/`:

1. `builder.cp313-win_amd64.pyd` - Construtor de árvores XML
2. `etree.cp313-win_amd64.pyd` - Parser XML/HTML principal (4.1 MB)
3. `objectify.cp313-win_amd64.pyd` - API Objectify (1.7 MB)
4. `sax.cp313-win_amd64.pyd` - Parser SAX (121 KB)
5. `_elementpath.cp313-win_amd64.pyd` - XPath engine (147 KB)
6. `_elementpath.py` - Wrapper Python

**Total de binários:** 6 arquivos (~6.2 MB)

---

## 🎯 Como Funciona o Carregamento

O arquivo `globalPlugins/padronix/__init__.py` faz:

```python
def _inject_lib_path() -> None:
    # 1. Injeta lib/shared (python-docx, lxml Python)
    sys.path.insert(0, str(lib_base / "shared"))
    
    # 2. Detecta arquitetura (32/64-bit)
    is_64bit = struct.calcsize("P") * 8 == 64
    arch_folder = "x64" if is_64bit else "x86"
    
    # 3. Injeta lib/x64 ou lib/x86 (binários)
    sys.path.insert(0, str(lib_base / arch_folder))
```

**Resultado:** Quando você faz `import docx` ou `import lxml`, o Python encontra:
- Código puro em `lib/shared/`
- Binários em `lib/x64/`

---

## ✅ Teste de Validação

Execute no Console Python do NVDA (NVDA+Ctrl+Z):

```python
# Teste python-docx
from docx import Document
doc = Document()
doc.add_heading('Teste Padronix', 0)
doc.add_paragraph('Bibliotecas carregadas com sucesso!')
print("✅ python-docx OK")

# Teste lxml
from lxml import etree
root = etree.Element("teste")
print("✅ lxml OK")

# Teste arquitetura
import struct
print(f"✅ Arquitetura: {struct.calcsize('P') * 8}-bit")
```

**Saída esperada:**
```
✅ python-docx OK
✅ lxml OK
✅ Arquitetura: 64-bit
```

---

## 🔄 Atualizando Dependências

Para atualizar no futuro:

```bash
# 1. Limpar pastas atuais
Remove-Item -Recurse -Force lib\shared\*
Remove-Item -Recurse -Force lib\x64\*

# 2. Reinstalar
pip install python-docx --target lib\shared --upgrade

# 3. Mover binários
Copy-Item -Path "lib\shared\lxml\*.pyd" -Destination "lib\x64\" -Force
Copy-Item -Path "lib\shared\lxml\_elementpath.py" -Destination "lib\x64\" -Force
```

---

## 📝 Notas Importantes

1. **Python 3.13:** As bibliotecas foram compiladas para Python 3.13 (CPython 3.13)
2. **64-bit apenas:** Apenas `lib/x64` tem binários. `lib/x86` está vazio.
3. **NVDA 2026:** Requer NVDA com Python 3.13+ embutido
4. **Compatibilidade:** python-docx 1.2.0 requer lxml >= 3.1.0 (instalado: 6.0.2 ✅)

---

**Próximo passo:** Testar o complemento no NVDA e validar que as bibliotecas carregam corretamente.
