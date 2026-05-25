import os
from typing import Optional
from dataclasses import dataclass, field
from src.logic import PropositionalLogicVerifier, LogicalArgument
from src.lean_prover import LeanProofGenerator
from src.validator import LeanProofValidator, ProofStatus


@dataclass
class ExperimentResult:
    name: str
    argument: LogicalArgument
    is_valid: bool
    counterexample: Optional[dict] = None
    proof: Optional[str] = None
    proof_valid: bool = False
    error: Optional[str] = None
    metadata: dict = field(default_factory=dict)


class LogicalConsequenceSolver:

    def __init__(self, api_key: Optional[str] = None):
        self.verifier = PropositionalLogicVerifier()
        self.proof_generator: Optional[LeanProofGenerator] = None
        self.proof_validator = LeanProofValidator()

        try:
            self.proof_generator = LeanProofGenerator(api_key)
        except ValueError:
            pass

    def solve(self, argument: LogicalArgument, generate_proof: bool = True) -> ExperimentResult:
        result = ExperimentResult(
            name="argumento",
            argument=argument,
            is_valid=False
        )

        try:
            is_valid, counterexample = self.verifier.verify_consequence(
                argument.premises,
                argument.conclusion
            )

            result.is_valid = is_valid
            result.counterexample = counterexample

            if is_valid and generate_proof and self.proof_generator:
                try:
                    proof = self.proof_generator.generate_proof(
                        propositions=argument.propositions,
                        premises=argument.premises,
                        conclusion=argument.conclusion
                    )
                    result.proof = proof

                    validation = self.proof_validator.validate_syntax(proof)
                    result.proof_valid = validation.status == ProofStatus.VALID
                    result.metadata["proof_validation"] = {
                        "status": validation.status.value,
                        "score": validation.score,
                        "details": validation.details
                    }

                except Exception as e:
                    result.error = f"Erro ao gerar prova: {str(e)}"

            elif not is_valid and self.proof_generator:
                try:
                    counterexample_text = self.proof_generator.generate_counterexample(
                        propositions=argument.propositions,
                        premises=argument.premises,
                        conclusion=argument.conclusion
                    )
                    result.metadata["counterexample_text"] = counterexample_text

                except Exception as e:
                    result.error = f"Erro ao gerar contra-exemplo: {str(e)}"

        except Exception as e:
            result.error = str(e)

        return result

    def batch_solve(
        self,
        arguments: list[LogicalArgument],
        generate_proofs: bool = True
    ) -> list[ExperimentResult]:
        results = []
        for i, arg in enumerate(arguments, 1):
            print(f"Processando argumento {i}/{len(arguments)}...", end=" ")
            result = self.solve(arg, generate_proof=generate_proofs)
            result.name = f"Argumento {i}"
            results.append(result)
            status = "✓ válido" if result.is_valid else "✗ inválido"
            print(status)

        return results


CLASSIC_EXAMPLES = {
    "modus_ponens": LogicalArgument(
        propositions=["p", "q"],
        premises=["p", "p => q"],
        conclusion="q"
    ),
    "modus_tollens": LogicalArgument(
        propositions=["p", "q"],
        premises=["p => q", "!q"],
        conclusion="!p"
    ),
    "disjunctive_syllogism": LogicalArgument(
        propositions=["p", "q"],
        premises=["p | q", "!p"],
        conclusion="q"
    ),
    "hypothetical_syllogism": LogicalArgument(
        propositions=["p", "q", "r"],
        premises=["p => q", "q => r"],
        conclusion="p => r"
    ),
    "affirming_consequent": LogicalArgument(
        propositions=["p", "q"],
        premises=["p => q", "q"],
        conclusion="p"
    ),
    "denying_antecedent": LogicalArgument(
        propositions=["p", "q"],
        premises=["p => q", "!p"],
        conclusion="!q"
    ),
    "destructive_dilemma": LogicalArgument(
        propositions=["p", "q", "r", "s"],
        premises=["p => q", "r => s", "!q | !s"],
        conclusion="!p | !r"
    ),
}
