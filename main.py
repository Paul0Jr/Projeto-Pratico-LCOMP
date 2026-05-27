#!/usr/bin/env python3

import subprocess
import sys

if __name__ == "__main__":
    result = subprocess.run([sys.executable, "premises_generator.py"], check=False)

    if result.returncode == 0:
        subprocess.run([sys.executable, "solver.py"], check=False)
    else:
        print("Erro ao gerar premissas")
        sys.exit(1)
