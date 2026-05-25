from src.solver import LogicalConsequenceSolver, CLASSIC_EXAMPLES
from src.logic import LogicalArgument
from src.utils import Logger, ReportGenerator


def example_1_basic_verification():
    Logger.info("Exemplo 1: Verificação básica com Z3")

    argument = LogicalArgument(
        propositions=["p", "q"],
        premises=["p", "p => q"],
        conclusion="q"
    )

    solver = LogicalConsequenceSolver()
    result = solver.solve(argument, generate_proof=False)

    Logger.info(f"Argumento válido? {result.is_valid}")
    Logger.info("=" * 60 + "\n")


def example_2_proof_generation():
    Logger.info("Exemplo 2: Geração de prova em LEAN")

    argument = LogicalArgument(
        propositions=["p", "q", "r"],
        premises=["p => q", "q => r", "p"],
        conclusion="r"
    )

    solver = LogicalConsequenceSolver()
    result = solver.solve(argument, generate_proof=True)

    if result.proof:
        Logger.success("Prova gerada com sucesso!")
        Logger.info(f"Validade da prova: {result.proof_valid}")
    else:
        Logger.warning("Não foi possível gerar prova")

    Logger.info("=" * 60 + "\n")


def example_3_counterexample():
    Logger.info("Exemplo 3: Contra-exemplo para argumento inválido")

    argument = LogicalArgument(
        propositions=["p", "q"],
        premises=["p => q", "q"],
        conclusion="p"
    )

    solver = LogicalConsequenceSolver()
    result = solver.solve(argument)

    if not result.is_valid:
        Logger.warning("Argumento é uma falácia (Afirmação do Consequente)")
        Logger.info(f"Contra-exemplo encontrado: {result.counterexample}")
    else:
        Logger.error("Erro: deveria ser inválido")

    Logger.info("=" * 60 + "\n")


def example_4_batch_analysis():
    Logger.info("Exemplo 4: Análise em lote")

    arguments = [
        CLASSIC_EXAMPLES["modus_ponens"],
        CLASSIC_EXAMPLES["modus_tollens"],
        CLASSIC_EXAMPLES["disjunctive_syllogism"],
        CLASSIC_EXAMPLES["affirming_consequent"],
    ]

    solver = LogicalConsequenceSolver()
    results = solver.batch_solve(arguments, generate_proofs=False)

    report = ReportGenerator.generate_markdown_report(results)
    print(report)

    Logger.info("=" * 60 + "\n")


def example_5_custom_argument():
    Logger.info("Exemplo 5: Argumento customizado")

    argument = LogicalArgument(
        propositions=["p", "q", "r", "s"],
        premises=[
            "p | q",
            "r & s",
            "!p => r"
        ],
        conclusion="q | s"
    )

    solver = LogicalConsequenceSolver()
    result = solver.solve(argument)

    Logger.info(f"Conclusão válida? {result.is_valid}")
    if result.counterexample:
        Logger.info(f"Contra-exemplo: {result.counterexample}")

    Logger.info("=" * 60 + "\n")


def example_6_classic_arguments():
    Logger.info("Exemplo 6: Argumentos clássicos de lógica")

    classic_names = [
        "modus_ponens",
        "modus_tollens",
        "disjunctive_syllogism",
        "hypothetical_syllogism",
        "destructive_dilemma",
        "affirming_consequent",
        "denying_antecedent",
    ]

    solver = LogicalConsequenceSolver()

    for name in classic_names:
        argument = CLASSIC_EXAMPLES[name]
        result = solver.solve(argument, generate_proof=False)

        status = "✓ VÁLIDO" if result.is_valid else "✗ INVÁLIDO"
        Logger.info(f"{name:30} -> {status}")

    Logger.info("=" * 60 + "\n")


if __name__ == "__main__":
    Logger.info("Iniciando exemplos de uso do framework LCOMP")
    Logger.info("=" * 60)

    example_1_basic_verification()
    example_6_classic_arguments()

