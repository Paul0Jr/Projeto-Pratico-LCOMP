import os
import sys
from src.solver import LogicalConsequenceSolver, CLASSIC_EXAMPLES
from src.logic import LogicalArgument


def print_header(title: str, width: int = 70):
    print("\n" + "=" * width)
    print(f"  {title}")
    print("=" * width + "\n")


def print_result(result):
    print(f"Nome: {result.name}")
    print(f"Proposições: {', '.join(result.argument.propositions)}")
    print(f"\nPremissas:")
    for i, premise in enumerate(result.argument.premises, 1):
        print(f"  {i}. {premise}")
    print(f"\nConclusão: {result.argument.conclusion}")

    if result.is_valid:
        print(f"\n[Z3] ✓ É consequência lógica")
    else:
        print(f"\n[Z3] ✗ NÃO é consequência lógica")
        if result.counterexample:
            print("Contra-exemplo:")
            for prop, value in result.counterexample.items():
                print(f"  {prop} = {value}")

    if result.proof:
        print(f"\n[LEAN Proof]:\n{result.proof}")
        if result.proof_valid:
            print("✓ Prova sintaticamente válida")
        else:
            print("⚠ Prova requer verificação")

    if result.error:
        print(f"\n⚠ Erro: {result.error}")

    print("-" * 70)


def main():
    print_header("Verificador de Consequência Lógica com Z3 e LEAN 3")

    has_api_key = bool(os.getenv("GEMINI_API_KEY"))
    if not has_api_key:
        print("⚠ GEMINI_API_KEY não configurada")
        print("   Para usar geração de provas, defina:")
        print("   export GEMINI_API_KEY='sua-chave-aqui'\n")

    solver = LogicalConsequenceSolver()

    print_header("Exemplos Clássicos de Lógica Proposicional")

    examples_to_run = [
        ("Modus Ponens", CLASSIC_EXAMPLES["modus_ponens"]),
        ("Modus Tollens", CLASSIC_EXAMPLES["modus_tollens"]),
        ("Silogismo Disjuntivo", CLASSIC_EXAMPLES["disjunctive_syllogism"]),
        ("Afirmação do Consequente (Falácia)", CLASSIC_EXAMPLES["affirming_consequent"]),
        ("Negação do Antecedente (Falácia)", CLASSIC_EXAMPLES["denying_antecedent"]),
    ]

    results = []
    for title, argument in examples_to_run:
        print(f"\n{title}")
        print("-" * 70)
        result = solver.solve(argument, generate_proof=has_api_key)
        result.name = title
        print_result(result)
        results.append(result)

    print_header("Resumo dos Resultados")
    valid_count = sum(1 for r in results if r.is_valid)
    invalid_count = len(results) - valid_count

    print(f"Total de argumentos analisados: {len(results)}")
    print(f"Argumentos válidos: {valid_count}")
    print(f"Argumentos inválidos: {invalid_count}")
    print(f"Taxa de sucesso: {(valid_count/len(results)*100):.1f}%")


if __name__ == "__main__":
    main()
