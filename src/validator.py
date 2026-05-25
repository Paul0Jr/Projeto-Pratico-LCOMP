from dataclasses import dataclass
from enum import Enum
from typing import Optional
import re


class ProofStatus(Enum):
    VALID = "válido"
    INCOMPLETE = "incompleto"
    INVALID_SYNTAX = "sintaxe inválida"
    UNVERIFIED = "não verificado"


@dataclass
class ValidationResult:
    status: ProofStatus
    message: str
    details: dict
    score: float


class LeanProofValidator:

    REQUIRED_KEYWORDS = ["theorem", "lemma", "def"]
    PROOF_KEYWORDS = ["by", ":="]
    TACTIC_KEYWORDS = ["exact", "apply", "intro", "cases", "have", "rw", "simp", "contradiction"]

    @staticmethod
    def validate_syntax(proof: str) -> ValidationResult:
        if not proof or not isinstance(proof, str):
            return ValidationResult(
                status=ProofStatus.INVALID_SYNTAX,
                message="Prova vazia ou inválida",
                details={"error": "proof_empty"},
                score=0.0
            )

        details = {"proof_length": len(proof)}
        score = 0.0

        has_declaration = any(kw in proof for kw in LeanProofValidator.REQUIRED_KEYWORDS)
        if not has_declaration:
            return ValidationResult(
                status=ProofStatus.INVALID_SYNTAX,
                message="Prova não contém declaração de theorem/lemma/def",
                details=details,
                score=0.2
            )
        score += 0.3

        has_proof = any(kw in proof for kw in LeanProofValidator.PROOF_KEYWORDS)
        if not has_proof:
            return ValidationResult(
                status=ProofStatus.INCOMPLETE,
                message="Prova não contém corpo (:= ou by)",
                details=details,
                score=0.5
            )
        score += 0.3

        if "sorry" in proof:
            return ValidationResult(
                status=ProofStatus.INCOMPLETE,
                message="Prova contém 'sorry' (incompleta)",
                details={**details, "contains_sorry": True},
                score=0.6
            )
        score += 0.2

        if not LeanProofValidator._check_parentheses(proof):
            return ValidationResult(
                status=ProofStatus.INVALID_SYNTAX,
                message="Parênteses desbalanceados",
                details=details,
                score=0.4
            )
        score += 0.1

        tactics_used = sum(1 for tactic in LeanProofValidator.TACTIC_KEYWORDS if tactic in proof)
        details["tactics_used"] = tactics_used

        return ValidationResult(
            status=ProofStatus.VALID,
            message="Prova sintaticamente válida",
            details=details,
            score=min(1.0, score + (tactics_used / 10))
        )

    @staticmethod
    def validate_structure(proof: str) -> ValidationResult:
        details = {}

        type_match = re.search(r'\((\w+)\s*:\s*Prop\)', proof)
        details["has_type_annotations"] = bool(type_match)

        hypotheses = re.findall(r'\(h\w*\s*:', proof)
        details["num_hypotheses"] = len(hypotheses)

        conclusion_match = re.search(r':\s*(\w+)\s*:=', proof)
        details["has_conclusion"] = bool(conclusion_match)

        score = 0.0
        if details["has_type_annotations"]:
            score += 0.3
        if details["num_hypotheses"] > 0:
            score += 0.3
        if details["has_conclusion"]:
            score += 0.4

        status = ProofStatus.VALID if score > 0.6 else ProofStatus.UNVERIFIED

        return ValidationResult(
            status=status,
            message="Validação estrutural completa",
            details=details,
            score=score
        )

    @staticmethod
    def _check_parentheses(text: str) -> bool:
        stack = []
        pairs = {'(': ')', '[': ']', '{': '}'}

        for char in text:
            if char in pairs:
                stack.append(char)
            elif char in pairs.values():
                if not stack or pairs[stack.pop()] != char:
                    return False

        return len(stack) == 0

    @staticmethod
    def extract_proof_info(proof: str) -> dict:
        return {
            "name": LeanProofValidator._extract_theorem_name(proof),
            "propositions": LeanProofValidator._extract_propositions(proof),
            "tactics": LeanProofValidator._extract_tactics(proof),
            "line_count": len(proof.split('\n')),
            "has_comments": '--' in proof or '/-' in proof,
        }

    @staticmethod
    def _extract_theorem_name(proof: str) -> Optional[str]:
        match = re.search(r'(?:theorem|lemma)\s+(\w+)', proof)
        return match.group(1) if match else None

    @staticmethod
    def _extract_propositions(proof: str) -> list[str]:
        matches = re.findall(r'\(\s*(\w+)\s*:\s*Prop\s*\)', proof)
        return matches

    @staticmethod
    def _extract_tactics(proof: str) -> list[str]:
        tactics = []
        for tactic in LeanProofValidator.TACTIC_KEYWORDS:
            if tactic in proof:
                tactics.append(tactic)
        return tactics
