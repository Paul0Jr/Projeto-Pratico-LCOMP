import os
from typing import Optional
import google.generativeai as genai
from src.config import AIConfig, LEAN_SYSTEM_PROMPT, COUNTEREXAMPLE_SYSTEM_PROMPT


class LeanProofGenerator:

    def __init__(self, api_key: Optional[str] = None):
        key = api_key or AIConfig.API_KEY
        if not key:
            raise ValueError(
                "GEMINI_API_KEY não configurada. "
                "Configure via variável de ambiente ou argumento."
            )
        genai.configure(api_key=key)
        self.model_name = AIConfig.MODEL_NAME

    def generate_proof(
        self,
        propositions: list[str],
        premises: list[str],
        conclusion: str,
        explanation: bool = True
    ) -> str:
        propositions_str = " ".join(f"({prop} : Prop)" for prop in propositions)

        prompt = f"""Generate a LEAN 3 proof for the following valid argument using natural deduction.

**Propositions**: {propositions_str}

**Premises**:
{chr(10).join(f'  {i+1}. {p}' for i, p in enumerate(premises))}

**Conclusion**: {conclusion}

**Requirements**:
1. Use LEAN 3 syntax with natural deduction tactics (intro, exact, apply, have, cases, etc.)
2. Follow the structure: theorem name (propositions) : conclusion := by ...
3. Include brief comments explaining each major step
4. Ensure the proof is complete (no sorry unless necessary)

{"5. Provide a brief mathematical explanation of why the argument is valid." if explanation else ""}"""

        model = genai.GenerativeModel(
            self.model_name,
            system_instruction=LEAN_SYSTEM_PROMPT
        )

        response = model.generate_content(prompt)
        return response.text

    def generate_counterexample(
        self,
        propositions: list[str],
        premises: list[str],
        conclusion: str
    ) -> str:
        prompt = f"""Generate a counterexample for the following INVALID argument in propositional logic.

**Propositions**: {", ".join(propositions)}

**Premises**:
{chr(10).join(f'  {i+1}. {p}' for i, p in enumerate(premises))}

**Conclusion**: {conclusion}

**Requirements**:
1. Find a truth assignment that makes ALL premises true
2. But makes the CONCLUSION false
3. Show the truth values clearly
4. Verify each premise and the conclusion
5. Explain why this is a valid counterexample

Format:
```
Counterexample:
p = true/false
q = true/false
...

Verification:
- Premise 1: [calculation] = true ✓
- Premise 2: [calculation] = true ✓
- Conclusion: [calculation] = false ✗

Explanation: [clear explanation of why this falsifies the argument]
```"""

        model = genai.GenerativeModel(
            self.model_name,
            system_instruction=COUNTEREXAMPLE_SYSTEM_PROMPT
        )

        response = model.generate_content(prompt)
        return response.text

    @staticmethod
    def validate_lean_syntax(proof: str) -> bool:
        required_elements = [
            ("theorem" in proof or "lemma" in proof),
            (":=" in proof or ":= by" in proof),
            ("(" in proof and ":" in proof),
        ]
        return all(required_elements)