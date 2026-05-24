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
    print("Example 1: Modus Ponens")
    print("=" * 60)

    p = create_proposition("p")
    q = create_proposition("q")

    premises = [p, Implies(p, q)]
    conclusion = q

    print(f"Premises: p AND (p → q)")
    print(f"Conclusion: q")

    is_consequence, result = verify_logical_consequence(premises, conclusion)
    print(f"\n[Z3] {result}")

    if is_consequence:
        print("\nGenerating LEAN proof...")
        try:
            proof = generate_lean_proof(
                propositions=["p", "q"],
                premises=["p", "p → q"],
                conclusion="q"
            )
            print("\nLEAN Proof:")
            print(proof)
        except Exception as e:
            print(f"Error generating proof: {e}")

    print()
    return is_consequence

def example_disjunctive_syllogism() -> bool:
    print("=" * 60)
    print("Example 2: Disjunctive Syllogism")
    print("=" * 60)

    p = create_proposition("p")
    q = create_proposition("q")

    premises = [Or(p, q), Not(p)]
    conclusion = q

    print(f"Premises: (p OR q) AND NOT p")
    print(f"Conclusion: q")

    is_consequence, result = verify_logical_consequence(premises, conclusion)
    print(f"\n[Z3] {result}")

    if is_consequence:
        print("\nGenerating LEAN proof...")
        try:
            proof = generate_lean_proof(
                propositions=["p", "q"],
                premises=["p OR q", "NOT p"],
                conclusion="q"
            )
            print("\nLEAN Proof:")
            print(proof)
        except Exception as e:
            print(f"Error generating proof: {e}")

    print()
    return is_consequence

def example_affirming_consequent() -> bool:
    print("=" * 60)
    print("Example 3: Affirming the Consequent (Fallacy)")
    print("=" * 60)

    p = create_proposition("p")
    q = create_proposition("q")

    premises = [Implies(p, q), q]
    conclusion = p

    print(f"Premises: (p → q) AND q")
    print(f"Conclusion: p")
    print("\nNote: This is a FALLACY. Not a logical consequence.\n")

    is_consequence, result = verify_logical_consequence(premises, conclusion)
    print(f"[Z3] {result}")

    if not is_consequence:
        print("\nGenerating counterexample...")
        try:
            counterexample = generate_counterexample(
                propositions=["p", "q"],
                premises=["p → q", "q"],
                conclusion="p"
            )
            print("\nCounterexample:")
            print(counterexample)
        except Exception as e:
            print(f"Error generating counterexample: {e}")

    print()
    return is_consequence

def example_complex_reasoning() -> bool:
    print("=" * 60)
    print("Example 4: Complex Reasoning")
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

    print(f"Premises:")
    print(f"  1. p → q")
    print(f"  2. r → NOT p")
    print(f"  3. p")
    print(f"\nConclusion: q")

    is_consequence, result = verify_logical_consequence(premises, conclusion)
    print(f"\n[Z3] {result}")

    if is_consequence:
        print("\nGenerating LEAN proof...")
        try:
            proof = generate_lean_proof(
                propositions=["p", "q", "r"],
                premises=["p → q", "r → NOT p", "p"],
                conclusion="q"
            )
            print("\nLEAN Proof:")
            print(proof)
        except Exception as e:
            print(f"Error generating proof: {e}")

    print()
    return is_consequence

def main() -> None:
    print("\n" + "=" * 60)
    print("Logical Consequence Verifier with Z3 and Claude")
    print("=" * 60)

    if not os.getenv("ANTHROPIC_API_KEY"):
        print("\nWarning: ANTHROPIC_API_KEY not configured")
        print("To use LEAN proof generation, set:")
        print("export ANTHROPIC_API_KEY='your-key-here'")
        print("\nContinuing with Z3 only...\n")

    results = []
    results.append(("Modus Ponens", example_modus_ponens()))
    results.append(("Disjunctive Syllogism", example_disjunctive_syllogism()))
    results.append(("Affirming the Consequent", example_affirming_consequent()))
    results.append(("Complex Reasoning", example_complex_reasoning()))

    print("=" * 60)
    print("Summary")
    print("=" * 60)
    for name, result in results:
        status = "Consequence" if result else "Not a consequence"
        print(f"{name}: {status}")
    print()

if __name__ == "__main__":
    main()