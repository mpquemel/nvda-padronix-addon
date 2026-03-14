#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Padronix - Criador de Pacote NVDA Add-on
Copyright (C) 2026 Melhym Pereira Quemel

Cria arquivo .nvda-addon pronto para distribuição.
"""

from __future__ import annotations

import os
import sys
import zipfile
import shutil
from pathlib import Path
from datetime import datetime


def log(message: str) -> None:
    """Log com timestamp."""
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {message}")


def create_addon() -> None:
    """Cria pacote .nvda-addon."""
    
    print("=" * 60)
    print("PADRONIX - CRIADOR DE ADD-ON NVDA")
    print("=" * 60)
    print()
    
    # Diretórios
    base_dir: Path = Path(__file__).parent
    build_dir: Path = base_dir / "build"
    addon_name: str = "padronix-2026.1.0.nvda-addon"
    addon_path: Path = base_dir / addon_name
    
    log("Limpando builds anteriores...")
    
    # Limpar build anterior
    if build_dir.exists():
        shutil.rmtree(build_dir)
    build_dir.mkdir(exist_ok=True)
    
    if addon_path.exists():
        addon_path.unlink()
    
    # Estrutura temporária
    temp_addon: Path = build_dir / "padronix"
    
    log("Criando estrutura de diretórios...")
    
    # Criar diretórios
    dirs_to_create = [
        temp_addon / "globalPlugins" / "padronix",
        temp_addon / "globalPlugins" / "lib" / "shared",
        temp_addon / "globalPlugins" / "lib" / "x86",
        temp_addon / "globalPlugins" / "lib" / "x64",
        temp_addon / "doc" / "pt_BR",
        temp_addon / "doc" / "en",
        temp_addon / "doc" / "es",
        temp_addon / "doc" / "fr",
        temp_addon / "doc" / "de",
        temp_addon / "doc" / "it",
        temp_addon / "doc" / "ar",
        temp_addon / "styles",
        temp_addon / "locale" / "pt_BR" / "LC_MESSAGES",
        temp_addon / "locale" / "en" / "LC_MESSAGES",
        temp_addon / "locale" / "es" / "LC_MESSAGES",
        temp_addon / "locale" / "fr" / "LC_MESSAGES",
        temp_addon / "locale" / "de" / "LC_MESSAGES",
        temp_addon / "locale" / "it" / "LC_MESSAGES",
        temp_addon / "locale" / "ar" / "LC_MESSAGES",
    ]
    
    for dir_path in dirs_to_create:
        dir_path.mkdir(parents=True, exist_ok=True)
    
    log("Copiando arquivos do plugin...")
    
    # Arquivos Python
    plugin_files: list[str] = [
        "__init__.py",
        "main_dialog.py",
        "padronix_settings.py",
        "workflow_manager.py",
        "ai_client.py",
        "docx_renderer.py",
    ]
    
    plugin_src: Path = base_dir / "globalPlugins" / "padronix"
    plugin_dst: Path = temp_addon / "globalPlugins" / "padronix"
    
    for filename in plugin_files:
        src: Path = plugin_src / filename
        dst: Path = plugin_dst / filename
        if src.exists():
            shutil.copy(src, dst)
            log(f"  ✓ {filename}")
        else:
            log(f"  ✗ {filename} (NÃO ENCONTRADO)")
    
    # Manifest
    manifest_src: Path = base_dir / "manifest.ini"
    manifest_dst: Path = temp_addon / "manifest.ini"
    if manifest_src.exists():
        shutil.copy(manifest_src, manifest_dst)
        log("  ✓ manifest.ini")
    
    # Documentação
    log("Copiando documentação...")
    for lang in ["pt_BR", "en", "es", "fr", "de", "it", "ar"]:
        readme_src: Path = base_dir / "doc" / lang / "readme.html"
        readme_dst: Path = temp_addon / "doc" / lang / "readme.html"
        if readme_src.exists():
            shutil.copy(readme_src, readme_dst)
            log(f"  ✓ doc/{lang}/readme.html")
    
    # Estilos
    log("Copiando estilos acadêmicos...")
    styles_src: Path = base_dir / "styles"
    styles_dst: Path = temp_addon / "styles"
    if styles_src.exists():
        for style_file in styles_src.glob("*.json"):
            shutil.copy(style_file, styles_dst / style_file.name)
            log(f"  ✓ styles/{style_file.name}")
    
    # Traduções
    log("Copiando traduções...")
    for lang in ["pt_BR", "en", "es", "fr", "de", "it", "ar"]:
        po_src: Path = base_dir / "locale" / lang / "LC_MESSAGES" / "padronix.po"
        po_dst: Path = temp_addon / "locale" / lang / "LC_MESSAGES" / "padronix.po"
        if po_src.exists():
            shutil.copy(po_src, po_dst)
            log(f"  ✓ locale/{lang}/padronix.po")
    
    # Criar ZIP (arquivo .nvda-addon é um ZIP renomeado)
    log("Criando arquivo .nvda-addon...")
    
    with zipfile.ZipFile(addon_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file_path in temp_addon.rglob("*"):
            if file_path.is_file():
                arcname: str = str(file_path.relative_to(temp_addon))
                zipf.write(file_path, arcname)
    
    # Estatísticas
    size_kb: float = addon_path.stat().st_size / 1024
    
    print()
    print("=" * 60)
    print("✅ PACOTE CRIADO COM SUCESSO!")
    print("=" * 60)
    print(f"📦 Arquivo: {addon_name}")
    print(f"📏 Tamanho: {size_kb:.2f} KB")
    print(f"📁 Local: {addon_path}")
    print()
    print("🔧 Para instalar no NVDA:")
    print("   1. Abra o NVDA")
    print("   2. Pressione NVDA+N → Ferramentas → Gerenciar Complementos")
    print("   3. Pressione I para Instalar")
    print("   4. Selecione o arquivo .nvda-addon")
    print()
    print("=" * 60)


if __name__ == "__main__":
    try:
        create_addon()
    except Exception as e:
        print(f"\n❌ ERRO: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
