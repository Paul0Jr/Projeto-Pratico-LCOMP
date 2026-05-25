#!/usr/bin/env python3

from pathlib import Path

CACHE_FILE = Path(".cache_results.json")

if __name__ == "__main__":
    if CACHE_FILE.exists():
        CACHE_FILE.unlink()
        print("Cache limpo com sucesso!")
        print(f"Arquivo removido: {CACHE_FILE}")
    else:
        print("Nenhum cache para limpar.")

