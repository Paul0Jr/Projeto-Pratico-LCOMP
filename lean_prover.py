import os
from anthropic import Anthropic

client = Anthropic()

SYSTEM_PROMPT = """You are an expert in propositional logic and LEAN theorem prover.

Your objectives are:
1. Generate formal proofs in LEAN 3 for valid arguments
2. Generate valid counterexamples for invalid arguments

LEAN 3 FORMAT (based on https://leanprover.github.io/logic_and_proof_lean3/natural_deduction_for_propositional_logic.html):

For VALID proofs, use:
```lean
theorem proof (p q r : Prop) : conclusion := by
  intro
  -- Use tactics: exact, apply, have, cases, contradiction, etc.
  sorry
```

For COUNTEREXAMPLES, describe a truth assignment that falsifies the argument:
```
Counterexample:
p = true
q = false
r = true
...
```

Be concise and direct. Always explain the logic used."""

def generate_lean_proof(propositions: list[str], premises: list[str], conclusion: str) -> str:
    propositions_str = " ".join(f"({prop} : Prop)" for prop in propositions)

    prompt = f"""Generate a LEAN proof for the following valid argument:

Propositions: {propositions_str}

Premises:
{chr(10).join(f'  {i+1}. {p}' for i, p in enumerate(premises))}

Conclusion: {conclusion}

Generate the corresponding LEAN code using natural deduction."""

    response = client.messages.create(
        model="claude-opus-4-7",
        max_tokens=1024,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": prompt}]
    )

    return response.content[0].text

def generate_counterexample(propositions: list[str], premises: list[str], conclusion: str) -> str:
    prompt = f"""Generate a counterexample for the following INVALID argument:

Propositions: {", ".join(propositions)}

Premises:
{chr(10).join(f'  {i+1}. {p}' for i, p in enumerate(premises))}

Conclusion: {conclusion}

Show a truth assignment that makes ALL premises true but the conclusion FALSE.
Format:
p = true
q = false
...

Explain why this is a valid counterexample."""

    response = client.messages.create(
        model="claude-opus-4-7",
        max_tokens=512,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": prompt}]
    )

    return response.content[0].text

def validate_lean_proof(proof: str) -> bool:
    checks = [
        "theorem" in proof or "lemma" in proof,
        ":=" in proof or ":= by" in proof,
    ]

    return all(checks)

def interactive_conversation() -> None:
    history = []

    print("\nModo Conversacional - Digite 'sair' para encerrar")
    print("=" * 60)

    while True:
        user_input = input("\nVocê: ").strip()

        if user_input.lower() == "sair":
            break

        history.append({"role": "user", "content": user_input})

        response = client.messages.create(
            model="claude-opus-4-7",
            max_tokens=1024,
            system=SYSTEM_PROMPT,
            messages=history
        )

        assistant_response = response.content[0].text
        history.append({"role": "assistant", "content": assistant_response})

        print(f"\nClaude: {assistant_response}")

if __name__ == "__main__":
    print("Teste - Gerando prova para Modus Ponens...")
    print("=" * 60)

    proof = generate_lean_proof(
        propositions=["p", "q"],
        premises=["p", "p → q"],
        conclusion="q"
    )

    print("\nProva gerada:")
    print(proof)
    print("\nVálida?" if validate_lean_proof(proof) else "\nInválida?")

