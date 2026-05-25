from z3 import *
import os
from lean_prover import (
    generate_lean_proof,
    generate_counterexample,
    generate_counterexample_with_guidance,
    generate_counterexample_without_guidance,
    compare_counterexamples,
    validate_counterexample
)

def create_proposition(name: str) -> BoolRef:
    return Bool(name)

def format_formula(formula: str) -> str:
    """Convert text notation to propositional logic symbols"""
    formula = formula.replace(" E ", " ∧ ")
    formula = formula.replace(" OU ", " ∨ ")
    formula = formula.replace("NÃO ", "¬")
    formula = formula.replace("→", "→")
    return formula

def verify_logical_consequence(premises: list[BoolRef], conclusion: BoolRef) -> tuple[bool, str]:
    solver = Solver()

    for premise in premises:
        solver.add(premise)

    solver.add(Not(conclusion))

    result = solver.check()

    if result == unsat:
        return True, "Consequência lógica verificada"
    elif result == sat:
        model = solver.model()
        return False, f"Não é consequência lógica\nContra-exemplo: {model}"
    else:
        return None, "Resultado indeterminado"

def example_modus_ponens() -> bool:
    print("=" * 60)
    print("Exemplo 1: Modus Ponens")
    print("=" * 60)

    p = create_proposition("p")
    q = create_proposition("q")

    premises = [p, Implies(p, q)]
    conclusion = q

    print(f"Premissas:")
    print(f"  1. p")
    print(f"  2. p → q")
    print(f"Conclusão: q")

    is_consequence, result = verify_logical_consequence(premises, conclusion)
    print(f"\n[Z3] {result}")

    if is_consequence:
        print("\nGerando prova em LEAN:")
        try:
            proof = generate_lean_proof(
                propositions=["p", "q"],
                premises=["p", "p → q"],
                conclusion="q"
            )
            print("\nProva em LEAN:")
            print(proof)
        except Exception as e:
            print(f"Erro ao gerar prova: {e}")

    print()
    return is_consequence

def example_disjunctive_syllogism() -> bool:
    print("=" * 60)
    print("Exemplo 2: Silogismo Disjuntivo")
    print("=" * 60)

    p = create_proposition("p")
    q = create_proposition("q")

    premises = [Or(p, q), Not(p)]
    conclusion = q

    print(f"Premissas:")
    print(f"  1. p ∨ q")
    print(f"  2. ¬p")
    print(f"Conclusão: q")

    is_consequence, result = verify_logical_consequence(premises, conclusion)
    print(f"\n[Z3] {result}")

    if is_consequence:
        print("\nGerando prova em LEAN:")
        try:
            proof = generate_lean_proof(
                propositions=["p", "q"],
                premises=["p ∨ q", "¬p"],
                conclusion="q"
            )
            print("\nProva em LEAN:")
            print(proof)
        except Exception as e:
            print(f"Erro ao gerar prova: {e}")

    print()
    return is_consequence

def example_affirming_consequent() -> bool:
    print("=" * 60)
    print("Exemplo 3: Afirmação do Consequente (Falácia)")
    print("=" * 60)

    p = create_proposition("p")
    q = create_proposition("q")

    premises = [Implies(p, q), q]
    conclusion = p

    print(f"Premissas:")
    print(f"  1. p → q")
    print(f"  2. q")
    print(f"Conclusão: p")
    print("\nNota: Esta é uma FALÁCIA. Não é consequência lógica.\n")

    is_consequence, result = verify_logical_consequence(premises, conclusion)
    print(f"[Z3] {result}")

    if not is_consequence:
        print("\n" + "=" * 60)
        print("COMPARAÇÃO: Contra-exemplos COM vs SEM Guidance")
        print("=" * 60)

        try:
            comparison = compare_counterexamples(
                propositions=["p", "q"],
                premises=["p → q", "q"],
                conclusion="p"
            )

            print("\n--- SEM GUIDANCE ---")
            if 'error' in comparison['without_guidance']:
                print(f"Erro: {comparison['without_guidance']['error']}")
            else:
                print(comparison['without_guidance']['counterexample'])
                print(f"\nVálido: {comparison['without_guidance']['valid']}")

            print("\n--- COM GUIDANCE ---")
            if 'error' in comparison['with_guidance']:
                print(f"Erro: {comparison['with_guidance']['error']}")
            else:
                print(comparison['with_guidance']['counterexample'])
                print(f"\nVálido: {comparison['with_guidance']['valid']}")

            print("\n" + "-" * 60)
            accuracy_without = comparison['without_guidance']['valid']
            accuracy_with = comparison['with_guidance']['valid']
            print(f"RESULTADO: Guidance {'melhorou' if accuracy_with else 'não melhorou'} a geração de contra-exemplos")

        except Exception as e:
            print(f"Erro ao comparar contra-exemplos: {e}")

    print()
    return is_consequence

def example_complex_reasoning() -> bool:
    print("=" * 60)
    print("Exemplo 4: Raciocínio Complexo")
    print("=" * 60)

    p = create_proposition("p")
    q = create_proposition("q")
    r = create_proposition("r")

    premises = [
        Implies(p, q),
        Implies(r, Not(p)),
        p
    ]
    conclusion = q

    print(f"Premissas:")
    print(f"  1. p → q")
    print(f"  2. r → ¬p")
    print(f"  3. p")
    print(f"\nConclusão: q")

    is_consequence, result = verify_logical_consequence(premises, conclusion)
    print(f"\n[Z3] {result}")

    if is_consequence:
        print("\nGerando prova em LEAN:")
        try:
            proof = generate_lean_proof(
                propositions=["p", "q", "r"],
                premises=["p → q", "r → ¬p", "p"],
                conclusion="q"
            )
            print("\nProva em LEAN:")
            print(proof)
        except Exception as e:
            print(f"Erro ao gerar prova: {e}")

    print()
    return is_consequence

def main() -> None:
    print("\n" + "=" * 60)
    print("Verificador de Consequência Lógica com Z3 e Gemini")
    print("=" * 60)

    if not os.getenv("GEMINI_API_KEY"):
        print("\nAviso: GEMINI_API_KEY não está configurada")
        print("Para usar a geração de provas em LEAN, defina:")
        print("export GEMINI_API_KEY='sua-chave-aqui'")
        print("\nContinuando apenas com Z3...\n")

    results = []
    results.append(("Modus Ponens", example_modus_ponens()))
    results.append(("Silogismo Disjuntivo", example_disjunctive_syllogism()))
    results.append(("Afirmação do Consequente", example_affirming_consequent()))
    results.append(("Raciocínio Complexo", example_complex_reasoning()))

    print("=" * 60)
    print("RESUMO FINAL")
    print("=" * 60)
    for name, result in results:
        status = "✓ Consequência lógica" if result else "✗ Não é consequência lógica"
        print(f"{name}: {status}")
    print()

if __name__ == "__main__":
    main()