import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

SYSTEM_PROMPT = """Você é um especialista em lógica proposicional e prover de teoremas LEAN.

Seus objetivos são:
1. Gerar provas formais em LEAN 3 para argumentos válidos
2. Gerar contraexemplos válidos para argumentos inválidos

FORMATO LEAN 3 (baseado em https://leanprover.github.io/logic_and_proof_lean3/natural_deduction_for_propositional_logic.html):

Para provas VÁLIDAS, use:
```lean
theorem prova (p q r : Prop) : conclusão := by
  intro
  -- Use táticas: exact, apply, have, cases, contradiction, etc.
  sorry
```

Para CONTRAEXEMPLOS, descreva uma atribuição de verdade que falsifica o argumento:
```
Contraexemplo:
p = verdadeiro
q = falso
r = verdadeiro
...
```

Seja conciso e direto. Sempre explique a lógica utilizada."""

model = genai.GenerativeModel("gemini-3.1-flash-lite", system_instruction=SYSTEM_PROMPT)

def generate_lean_proof(propositions: list[str], premises: list[str], conclusion: str) -> str:
    propositions_str = " ".join(f"({prop} : Prop)" for prop in propositions)

    prompt = f"""Gere uma prova em LEAN para o seguinte argumento válido:

Proposições: {propositions_str}

Premissas:
{chr(10).join(f'  {i+1}. {p}' for i, p in enumerate(premises))}

Conclusão: {conclusion}

Gere o código LEAN correspondente usando dedução natural."""

    response = model.generate_content(prompt)

    return response.text

def generate_counterexample(propositions: list[str], premises: list[str], conclusion: str) -> str:
    prompt = f"""Gere um contraexemplo para o seguinte argumento INVÁLIDO:

Proposições: {", ".join(propositions)}

Premissas:
{chr(10).join(f'  {i+1}. {p}' for i, p in enumerate(premises))}

Conclusão: {conclusion}

Mostre uma atribuição de verdade que torna TODAS as premissas verdadeiras mas a conclusão FALSA.
Formato:
p = verdadeiro
q = falso
...

Explique por que este é um contraexemplo válido."""

    response = model.generate_content(prompt)

    return response.text

def generate_counterexample_with_guidance(propositions: list[str], premises: list[str], conclusion: str) -> str:
    propositions_str = ", ".join(propositions)

    prompt = f"""Gere um contraexemplo para o seguinte argumento INVÁLIDO:

Proposições: {propositions_str}

Premissas:
{chr(10).join(f'  {i+1}. {p}' for i, p in enumerate(premises))}

Conclusão: {conclusion}

REGRAS DE VERIFICAÇÃO IMPORTANTES:
1. Encontre uma atribuição de verdade onde TODAS as premissas avaliam como VERDADEIRAS
2. A CONCLUSÃO deve avaliar como FALSA com esta atribuição
3. Verifique cada premissa e a conclusão
4. Se a atribuição viola estas regras, NÃO é um contraexemplo válido

Apresente neste formato exato:
Contraexemplo:
[atribuições]

Verificação:
[Mostre cada avaliação de premissa e conclusão]

Status: VÁLIDO ou INVÁLIDO"""

    response = model.generate_content(prompt)
    return response.text

def generate_counterexample_without_guidance(propositions: list[str], premises: list[str], conclusion: str) -> str:
    propositions_str = ", ".join(propositions)

    prompt = f"""Proposições: {propositions_str}

Premissas:
{chr(10).join(f'  {i+1}. {p}' for i, p in enumerate(premises))}

Conclusão: {conclusion}

Contraexemplo:"""

    response = model.generate_content(prompt)
    return response.text

def validate_lean_proof(proof: str) -> bool:
    checks = [
        "theorem" in proof or "lemma" in proof,
        ":=" in proof or ":= by" in proof,
    ]
    return all(checks)

def validate_counterexample(counterexample: str) -> bool:
    checks = [
        "=" in counterexample,
        any(keyword in counterexample.lower() for keyword in ["true", "false"]),
    ]
    return all(checks)

def compare_counterexamples(propositions: list[str], premises: list[str], conclusion: str) -> dict:
    result = {}

    try:
        without_guidance = generate_counterexample_without_guidance(propositions, premises, conclusion)
        result['without_guidance'] = {
            'counterexample': without_guidance,
            'valid': validate_counterexample(without_guidance)
        }
    except Exception as e:
        result['without_guidance'] = {'error': str(e), 'valid': False}

    try:
        with_guidance = generate_counterexample_with_guidance(propositions, premises, conclusion)
        result['with_guidance'] = {
            'counterexample': with_guidance,
            'valid': validate_counterexample(with_guidance)
        }
    except Exception as e:
        result['with_guidance'] = {'error': str(e), 'valid': False}

    return result

def generate_lean_proof_without_guidance(propositions: list[str], premises: list[str], conclusion: str) -> str:
    propositions_str = " ".join(f"({prop} : Prop)" for prop in propositions)

    prompt = f"""Gere uma prova em LEAN para o seguinte argumento válido SEM explicação:

Proposições: {propositions_str}

Premissas:
{chr(10).join(f'  {i+1}. {p}' for i, p in enumerate(premises))}

Conclusão: {conclusion}

Apenas forneça o código LEAN, nada mais."""

    response = model.generate_content(prompt)
    return response.text

def compare_with_and_without_guidance(propositions: list[str], premises: list[str], conclusion: str) -> dict:
    result = {}

    try:
        without_guidance = generate_lean_proof_without_guidance(propositions, premises, conclusion)
        result['without_guidance'] = {
            'proof': without_guidance,
            'valid': validate_lean_proof(without_guidance)
        }
    except Exception as e:
        result['without_guidance'] = {'error': str(e), 'valid': False}

    try:
        with_guidance = generate_lean_proof(propositions, premises, conclusion)
        result['with_guidance'] = {
            'proof': with_guidance,
            'valid': validate_lean_proof(with_guidance)
        }
    except Exception as e:
        result['with_guidance'] = {'error': str(e), 'valid': False}

    return result

def interactive_conversation() -> None:
    chat = model.start_chat()

    print("\nModo Conversacional - Digite 'sair' para encerrar")
    print("=" * 60)

    while True:
        user_input = input("\nVocê: ").strip()

        if user_input.lower() == "sair":
            break

        response = chat.send_message(user_input)
        print(f"\nGemini: {response.text}")

if __name__ == "__main__":
    print("Teste - Gerando prova para Modus Ponens:")
    print("=" * 60)

    proof = generate_lean_proof(
        propositions=["p", "q"],
        premises=["p", "p → q"],
        conclusion="q"
    )

    print("\nProva gerada:")
    print(proof)
    print("\nVálida?" if validate_lean_proof(proof) else "\nInválida?")

