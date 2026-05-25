from dataclasses import dataclass
from typing import Optional

import sys
import subprocess
try:
    import pkg_resources
except ImportError:
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "setuptools", "-q"])
        import pkg_resources
    except:
        pass

from z3 import Solver, BoolRef, Bool, Not, unsat, sat, unknown, And, Or, Implies


@dataclass
class LogicalArgument:
    premises: list[str]
    conclusion: str
    propositions: list[str]


class PropositionalLogicVerifier:

    def __init__(self):
        self.solver: Optional[Solver] = None
        self.propositions: dict[str, BoolRef] = {}

    def create_proposition(self, name: str) -> BoolRef:
        if name not in self.propositions:
            self.propositions[name] = Bool(name)
        return self.propositions[name]

    def parse_formula(self, formula: str) -> BoolRef:
        import re

        formula = formula.strip()

        formula = re.sub(r'[¬~!]', 'NOT', formula)
        formula = formula.replace("NOT", "Not")

        formula = re.sub(r'(\)|\w)\s*\|\s*(\(|\w)', r'\1 | \2', formula)
        formula = formula.replace(" OR ", " | ").replace(" or ", " | ")
        formula = re.sub(r'\|', 'Or', formula)

        formula = formula.replace(" AND ", " & ").replace(" and ", " & ")
        formula = formula.replace("∧", " & ").replace("∨", " | ")
        formula = re.sub(r'&', 'And', formula)

        formula = formula.replace("→", "=>").replace("IMPLIES", "=>")
        formula = formula.replace("=>", "Implies")

        formula = formula.replace("↔", "<=>").replace("IFF", "<=>")
        formula = formula.replace("<=>", "Iff")

        formula = formula.replace("Not ", "Not(")
        formula = re.sub(r'Not\(\w+\)', lambda m: m.group(0) + ')', formula)

        formula = re.sub(r'(\w+|\))\s+Or\s+(\w+|\()', r'Or(\1, \2)', formula)
        formula = re.sub(r'(\w+|\))\s+And\s+(\w+|\()', r'And(\1, \2)', formula)
        formula = re.sub(r'(\w+|\))\s+Implies\s+(\w+|\()', r'Implies(\1, \2)', formula)
        formula = re.sub(r'(\w+|\))\s+Iff\s+(\w+|\()', r'Iff(\1, \2)', formula)

        props = self._extract_propositions(formula)

        namespace = {name: self.create_proposition(name) for name in props}
        namespace.update({
            "Not": lambda a: Not(a),
            "And": lambda a, b: And(a, b),
            "Or": lambda a, b: Or(a, b),
            "Implies": lambda a, b: Implies(a, b),
            "Iff": lambda a, b: And(Implies(a, b), Implies(b, a)),
            "And": And,
            "Or": Or,
        })

        try:
            result = eval(formula, {"__builtins__": {}}, namespace)
            return result
        except Exception as e:
            raise ValueError(f"Fórmula inválida: {formula}") from e

    def _extract_propositions(self, formula: str) -> set[str]:
        import re
        keywords = {"Not", "And", "Or", "Implies", "Iff", "True", "False"}
        props = set(re.findall(r'\b[a-zA-Z_]\w*\b', formula)) - keywords
        return props

    def verify_consequence(self, premises: list[str], conclusion: str) -> tuple[bool, Optional[dict]]:
        solver = Solver()

        try:
            for premise_str in premises:
                premise = self.parse_formula(premise_str)
                solver.add(premise)

            conclusion_formula = self.parse_formula(conclusion)
            solver.add(Not(conclusion_formula))

            result = solver.check()

            if result == unsat:
                return True, None
            elif result == sat:
                model = solver.model()
                counterexample = {str(var): model[var] for var in self.propositions.values()}
                return False, counterexample
            else:
                raise RuntimeError("Solver retornou resultado indeterminado")

        except Exception as e:
            raise RuntimeError(f"Erro ao verificar consequência lógica: {e}") from e

    def reset(self):
        self.solver = None
        self.propositions.clear()
