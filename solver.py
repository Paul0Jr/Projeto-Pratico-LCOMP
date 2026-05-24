from z3 import *
import os
from lean_prover import generate_lean_proof, generate_counterexample

def create_proposition(name: str) -> BoolRef:
    return Bool(name)

def verify_logical_consequence(premises: list[BoolRef], conclusion: BoolRef) -> tuple[bool, str]:
    solver = Solver()

    for premise in premises:
        solver.add(premise)

    solver.add(Not(conclusion))

    result = solver.check()

    if result == unsat:
        return True, "Logical consequence verified"
    elif result == sat:
        model = solver.model()
        return False, f"Not a logical consequence\nCounterexample: {model}"
    else:
        return None, "Undetermined result"

def example_modus_ponens() -> bool:
    print("=" * 60)
    print("Exemplo 1: Modus Ponens")
    print("=" * 60)

    p = create_proposition("p")
    q = create_proposition("q")

    premises = [p, Implies(p, q)]
    conclusion = q

    print(f"Premissas: p E (p → q)")
    print(f"Conclusão: q")

    is_consequence, result = verify_logical_consequence(premises, conclusion)
    print(f"\n[Z3] {result}")

    if is_consequence:
        print("\nGerando prova em LEAN...")
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

    print(f"Premissas: (p OU q) E NÃO p")
    print(f"Conclusão: q")

    is_consequence, result = verify_logical_consequence(premises, conclusion)
    print(f"\n[Z3] {result}")

    if is_consequence:
        print("\nGerando prova em LEAN...")
        try:
            proof = generate_lean_proof(
                propositions=["p", "q"],
                premises=["p OU q", "NÃO p"],
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

    print(f"Premissas: (p → q) E q")
    print(f"Conclusão: p")
    print("\nNota: Esta é uma FALÁCIA. Não é consequência lógica.\n")

    is_consequence, result = verify_logical_consequence(premises, conclusion)
    print(f"[Z3] {result}")

    if not is_consequence:
        print("\nGerando contra-exemplo...")
        try:
            counterexample = generate_counterexample(
                propositions=["p", "q"],
                premises=["p → q", "q"],
                conclusion="p"
            )
            print("\nContra-exemplo:")
            print(counterexample)
        except Exception as e:
            print(f"Erro ao gerar contra-exemplo: {e}")

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
    print(f"  2. r → NÃO p")
    print(f"  3. p")
    print(f"\nConclusão: q")

    is_consequence, result = verify_logical_consequence(premises, conclusion)
    print(f"\n[Z3] {result}")

    if is_consequence:
        print("\nGerando prova em LEAN...")
        try:
            proof = generate_lean_proof(
                propositions=["p", "q", "r"],
                premises=["p → q", "r → NÃO p", "p"],
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
    print("Resumo")
    print("=" * 60)
    for name, result in results:
        status = "Consequência lógica" if result else "Não é consequência lógica"
        print(f"{name}: {status}")
    print()

if __name__ == "__main__":
    main()