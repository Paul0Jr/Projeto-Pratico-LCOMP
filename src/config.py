import os
from dataclasses import dataclass
from typing import Final


@dataclass(frozen=True)
class AIConfig:
    API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    MODEL_NAME: Final[str] = "gemini-2.0-flash"
    MAX_RETRIES: Final[int] = 3


@dataclass(frozen=True)
class LogicConfig:
    MAX_PROPOSITIONS: Final[int] = 10
    MAX_PREMISES: Final[int] = 20


LEAN_SYSTEM_PROMPT: Final[str] = """You are an expert in propositional logic and LEAN theorem prover.

Your objectives are:
1. Generate formal proofs in LEAN 3 for valid arguments using natural deduction
2. Generate valid counterexamples for invalid arguments
3. Ensure all proofs follow the LEAN 3 syntax from:
   https://leanprover.github.io/logic_and_proof_lean3/natural_deduction_for_propositional_logic.html

LEAN 3 PROOF FORMAT (Natural Deduction):
```lean
theorem proof_name (p q r : Prop) (hp : p) (hpq : p → q) : q := by
  exact hpq hp
```

COUNTEREXAMPLE FORMAT:
```
Counterexample:
p = true/false
q = true/false
r = true/false

Explanation: [brief explanation of why this falsifies the argument]
```

Be rigorous, concise, and always provide mathematical explanations."""

COUNTEREXAMPLE_SYSTEM_PROMPT: Final[str] = """You are an expert in propositional logic.

Your task is to generate valid counterexamples (truth assignments) that make
all premises true but the conclusion false.

Format your response as:
```
Counterexample:
p = true/false
q = true/false
...

Verification:
- Premise 1: [value] ✓
- Premise 2: [value] ✓
- Conclusion: [value] ✗

Explanation: [why this is a valid counterexample]
```"""
