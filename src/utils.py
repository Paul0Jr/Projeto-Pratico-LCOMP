import json
from datetime import datetime
from typing import Any
from src.solver import ExperimentResult


class Logger:

    @staticmethod
    def log(level: str, message: str) -> None:
        icon = Logger.LEVELS.get(level, "•")
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] {icon} {message}")

    @staticmethod
    def debug(message: str) -> None:
        Logger.log("DEBUG", message)

    @staticmethod
    def info(message: str) -> None:
        Logger.log("INFO", message)

    @staticmethod
    def success(message: str) -> None:
        Logger.log("SUCCESS", message)

    @staticmethod
    def warning(message: str) -> None:
        Logger.log("WARNING", message)

    @staticmethod
    def error(message: str) -> None:
        Logger.log("ERROR", message)


class ReportGenerator:

    @staticmethod
    def generate_json_report(results: list[ExperimentResult]) -> str:
        report_data = {
            "generated_at": datetime.now().isoformat(),
            "total_experiments": len(results),
            "valid_arguments": sum(1 for r in results if r.is_valid),
            "invalid_arguments": sum(1 for r in results if not r.is_valid),
            "experiments": []
        }

        for result in results:
            experiment_data = {
                "name": result.name,
                "propositions": result.argument.propositions,
                "premises": result.argument.premises,
                "conclusion": result.argument.conclusion,
                "is_valid": result.is_valid,
                "counterexample": str(result.counterexample) if result.counterexample else None,
                "proof_exists": result.proof is not None,
                "proof_valid": result.proof_valid,
                "error": result.error,
            }
            report_data["experiments"].append(experiment_data)

        return json.dumps(report_data, indent=2, ensure_ascii=False)

    @staticmethod
    def generate_markdown_report(results: list[ExperimentResult]) -> str:
        report = f"# Relatório de Análise - {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n"

        valid_count = sum(1 for r in results if r.is_valid)
        invalid_count = len(results) - valid_count

        report += "##  Resumo Executivo\n\n"
        report += f"- **Total de argumentos analisados**: {len(results)}\n"
        report += f"- **Argumentos válidos**: {valid_count} ({valid_count/len(results)*100:.1f}%)\n"
        report += f"- **Argumentos inválidos**: {invalid_count} ({invalid_count/len(results)*100:.1f}%)\n\n"

        report += "##  Detalhes dos Argumentos\n\n"

        for i, result in enumerate(results, 1):
            status = "✓ Válido" if result.is_valid else "✗ Inválido"
            report += f"### {i}. {result.name} [{status}]\n\n"
            report += f"**Proposições**: {', '.join(result.argument.propositions)}\n\n"

            report += "**Premissas**:\n"
            for j, premise in enumerate(result.argument.premises, 1):
                report += f"{j}. {premise}\n"
            report += f"\n**Conclusão**: {result.argument.conclusion}\n\n"

            if result.is_valid:
                report += " É consequência lógica.\n\n"
            else:
                report += " NÃO é consequência lógica.\n\n"
                if result.counterexample:
                    report += "**Contra-exemplo**:\n"
                    report += "```\n"
                    for prop, value in result.counterexample.items():
                        report += f"{prop} = {value}\n"
                    report += "```\n\n"

            if result.proof:
                report += "**Prova LEAN**:\n"
                report += "```lean\n"
                report += result.proof[:500] + ("..." if len(result.proof) > 500 else "")
                report += "\n```\n\n"

            if result.error:
                report += f"⚠️ **Erro**: {result.error}\n\n"

            report += "---\n\n"

        return report

    @staticmethod
    def generate_latex_report(results: list[ExperimentResult]) -> str:
        report = r"""
\documentclass{article}
\usepackage[utf-8]{inputenc}
\usepackage{amssymb}
\usepackage{amsmath}
\usepackage{listings}
\usepackage{xcolor}

\title{Relatório de Análise de Consequência Lógica}
\author{Sistema LCOMP}
\date{\today}

\lstset{
    language=Lean,
    basicstyle=\ttfamily,
    keywordstyle=\color{blue},
    commentstyle=\color{gray},
    stringstyle=\color{red},
    breaklines=true,
}

\begin{document}

\maketitle

\section{Resumo}

"""
        valid_count = sum(1 for r in results if r.is_valid)
        report += f"Total de argumentos: {len(results)}\\\\\n"
        report += f"Argumentos válidos: {valid_count}\\\\\n"
        report += f"Argumentos inválidos: {len(results) - valid_count}\n\n"

        report += r"\section{Detalhes}" + "\n\n"

        for i, result in enumerate(results, 1):
            report += f"\\subsection{{{i}. {result.name}}}\n\n"
            report += "\\textbf{Proposições}: "
            report += ", ".join(result.argument.propositions) + "\\\\\n\n"

            report += "\\textbf{Premissas}:\n"
            report += "\\begin{enumerate}\n"
            for premise in result.argument.premises:
                report += f"\\item ${premise}$\n"
            report += "\\end{enumerate}\n\n"

            report += f"\\textbf{{Conclusão}}: ${result.argument.conclusion}$\n\n"

            if result.is_valid:
                report += "\\textcolor{green}{✓ É consequência lógica.}\n\n"
            else:
                report += "\\textcolor{red}{✗ NÃO é consequência lógica.}\n\n"

        report += r"\end{document}"
        return report


def format_formula_for_display(formula: str) -> str:
    replacements = {
        "->": "→",
        "=>": "→",
        "<->": "↔",
        "<=>": "↔",
        "AND": "∧",
        "and": "∧",
        " and ": " ∧ ",
        "OR": "∨",
        "or": "∨",
        " or ": " ∨ ",
        "NOT": "¬",
        "not": "¬",
        " not ": " ¬ ",
    }

    result = formula
    for old, new in replacements.items():
        result = result.replace(old, new)

    return result


def validate_argument_structure(propositions: list[str], premises: list[str], conclusion: str) -> bool:
    if not propositions or not isinstance(propositions, list):
        return False
    if not premises or not isinstance(premises, list):
        return False
    if not conclusion or not isinstance(conclusion, str):
        return False

    return len(propositions) > 0 and len(premises) > 0
