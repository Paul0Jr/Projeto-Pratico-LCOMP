from z3 import *
import os
import json
from lean_prover import (
    generate_lean_proof,
    generate_counterexample,
    generate_counterexample_with_guidance,
    generate_counterexample_without_guidance,
    compare_counterexamples,
    validate_counterexample
)
from premises_generator import load_premises_from_file, validate_premises_structure

def create_proposition(name: str) -> BoolRef:
    return Bool(name)

def formula_to_z3(formula: str, props: dict) -> BoolRef:
    """Converte uma fórmula em string para expressão Z3"""
    # Substitui os operadores lógicos por suas equivalentes em Z3
    formula = formula.strip()

    def parse_expr(expr):
        expr = expr.strip()

        # Remove parênteses externos
        while expr.startswith('(') and expr.endswith(')'):
            expr = expr[1:-1].strip()

        # Negação
        if expr.startswith('¬'):
            return Not(parse_expr(expr[1:].strip()))

        # Bicondicional (↔)
        if '↔' in expr and not expr.startswith('('):
            parts = expr.split('↔')
            left = parse_expr(parts[0])
            right = parse_expr(parts[1])
            return And(Implies(left, right), Implies(right, left))

        # Implicação (→)
        if '→' in expr:
            parts = expr.split('→')
            left = parse_expr(parts[0])
            right = parse_expr(parts[1])
            return Implies(left, right)

        # Disjunção (∨)
        if '∨' in expr:
            parts = [p.strip() for p in expr.split('∨')]
            result = parse_expr(parts[0])
            for part in parts[1:]:
                result = Or(result, parse_expr(part))
            return result

        # Conjunção (∧)
        if '∧' in expr:
            parts = [p.strip() for p in expr.split('∧')]
            result = parse_expr(parts[0])
            for part in parts[1:]:
                result = And(result, parse_expr(part))
            return result

        # Proposição simples
        expr_clean = expr.strip()
        if expr_clean in props:
            return props[expr_clean]
        else:
            raise ValueError(f"Proposição desconhecida: {expr_clean}")

    return parse_expr(formula)

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

def run_example(premise_data: dict, example_num: int) -> bool:
    """Função genérica para executar um exemplo com dados de premissas"""
    print("=" * 60)
    print(f"Exemplo {example_num}: {premise_data['name']}")
    print("=" * 60)

    proposition_names = premise_data['propositions']
    premise_strs = premise_data['premises']
    conclusion_str = premise_data['conclusion']
    premise_type = premise_data['type']

    props = {name: create_proposition(name) for name in proposition_names}

    try:
        premises = [formula_to_z3(p, props) for p in premise_strs]
        conclusion = formula_to_z3(conclusion_str, props)
    except Exception as e:
        print(f"Erro ao converter fórmulas: {e}")
        return False

    print(f"Premissas:")
    for i, p in enumerate(premise_strs, 1):
        print(f"  {i}. {p}")
    print(f"Conclusão: {conclusion_str}")
    print(f"Tipo Esperado: {premise_type}\n")

    is_consequence, result = verify_logical_consequence(premises, conclusion)
    print(f"[Z3] {result}")

    if is_consequence and premise_type == "VALID":
        print("\nGerando prova em LEAN:")
        try:
            proof = generate_lean_proof(
                propositions=proposition_names,
                premises=premise_strs,
                conclusion=conclusion_str
            )
            print("\nProva em LEAN:")
            print(proof)
        except Exception as e:
            print(f"Erro ao gerar prova: {e}")

    elif not is_consequence and premise_type == "INVALID":
        print("\n" + "=" * 60)
        print("COMPARAÇÃO: Contra-exemplos COM vs SEM Guidance")
        print("=" * 60)

        try:
            comparison = compare_counterexamples(
                propositions=proposition_names,
                premises=premise_strs,
                conclusion=conclusion_str
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


def first_example(premise_data: dict) -> bool:
    return run_example(premise_data, 1)

def second_example(premise_data: dict) -> bool:
    return run_example(premise_data, 2)

def third_example(premise_data: dict) -> bool:
    return run_example(premise_data, 3)

def fourth_example(premise_data: dict) -> bool:
    return run_example(premise_data, 4)

def main() -> None:
    print("\n" + "=" * 60)
    print("Verificador de Consequência Lógica com Z3 e Gemini")
    print("=" * 60)

    if not os.getenv("GEMINI_API_KEY"):
        print("\nAviso: GEMINI_API_KEY não está configurada")
        print("\nContinuando apenas com Z3:\n")

    premises = load_premises_from_file()

    if not premises or not validate_premises_structure(premises):
        print("\nErro: Não foi possível carregar as premissas geradas.")
        print("Execute primeiro: python premises_generator.py")
        return

    results = []
    premise_list = premises['premises']

    results.append(("Exemplo um", first_example(premise_list[0])))
    results.append(("Exemplo dois", second_example(premise_list[1])))
    results.append(("Exemplo três", third_example(premise_list[2])))
    results.append(("Exemplo quatro", fourth_example(premise_list[3])))

    print("=" * 60)
    print("RESUMO FINAL")
    print("=" * 60)
    for name, result in results:
        status = "É consequência lógica" if result else "NÃO é consequência lógica"
        print(f"{name}: {status}")
    print()

if __name__ == "__main__":
    main()