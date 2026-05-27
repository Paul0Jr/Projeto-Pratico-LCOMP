import os
import json
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

SYSTEM_PROMPT = """Você é um especialista em lógica proposicional e gerador de premissas de teste.

Seu objetivo é gerar premissas em lógica proposicional sem especificar se são válidas ou inválidas.
Isso será verificado automaticamente.

Use os operadores formais:
- → (implicação)
- ∧ (conjunção)
- ∨ (disjunção)
- ¬ (negação)
- ↔ (bicondicional)

Seja conciso e direto."""

model = genai.GenerativeModel("gemini-3.1-flash-lite", system_instruction=SYSTEM_PROMPT)

def generate_premises() -> dict:
    """Gera 4 premissas aleatórias em lógica proposicional"""

    prompt = """Gere exatamente 4 premissas em lógica proposicional aleatórias (variedade de complexidade).

    Retorne EXATAMENTE neste formato JSON (sem explicação adicional):

    {
        "premises": [
            {
                "name": "Nome descritivo 1",
                "propositions": ["proposições"],
                "premises": ["premissa"],
                "conclusion": "conclusao da premissa"
            },
            {
                "name": "Nome descritivo 2",
                "propositions": ["proposições"],
                "premises": ["premissa"],
                "conclusion": "conclusao da premissa"
            },
            {
                "name": "Nome descritivo 3",
                "propositions": ["proposições"],
                "premises": ["premissa"],
                "conclusion": "conclusao da premissa"
            },
            {
                "name": "Nome descritivo 4",
                "propositions": ["proposições"],
                "premises": ["premissa"],
                "conclusion": "conclusao da premissa"
            }
        ]
    }

    Garanta que:
    - Exatamente 4 premissas
    - Cada uma com: name, propositions, premises, conclusion
    - Nomes descritivos em português
    - Operadores formais corretos
    - As proposições devem estar no formato ["p", "q",...]
    - Variedade: ao menos uma premissa deve ser inválida, as outras podem ser válidas (será verificado automaticamente)"""

    response = model.generate_content(prompt)

    try:
        json_str = response.text
        if "```json" in json_str:
            json_str = json_str.split("```json")[1].split("```")[0]
        elif "```" in json_str:
            json_str = json_str.split("```")[1].split("```")[0]

        return json.loads(json_str)
    except (json.JSONDecodeError, IndexError) as e:
        print(f"Erro ao fazer parse do JSON: {e}")
        print(f"Resposta recebida: {response.text}")
        return None

def save_premises_to_file(premises: dict, filename: str = "generated_premises.json") -> None:
    """Salva as premissas geradas em um arquivo JSON"""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(premises, f, ensure_ascii=False, indent=2)

def load_premises_from_file(filename: str = "generated_premises.json") -> dict:
    """Carrega premissas de um arquivo JSON"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Arquivo {filename} não encontrado")
        return None

def validate_premises_structure(premises: dict) -> bool:
    """Valida se as premissas têm a estrutura correta"""
    if not premises or "premises" not in premises:
        return False

    if len(premises["premises"]) != 4:
        return False

    for p in premises["premises"]:
        required_keys = {"name", "propositions", "premises", "conclusion"}
        if not all(key in p for key in required_keys):
            return False

    return True

if __name__ == "__main__":
    print("Gerando 4 premissas em lógica proposicional:")
    print("=" * 60)

    premises = generate_premises()

    if premises and validate_premises_structure(premises):
        print("\nResumo:")
        for i, p in enumerate(premises["premises"], 1):
            print(f"{i}. {p['name']}")

        save_premises_to_file(premises)

        print("\nDetalhes das premissas:")
        print("=" * 60)
        for i, p in enumerate(premises["premises"], 1):
            print(f"\nPremissa {i}: {p['name']}")
            print(f"Proposições: {', '.join(p['propositions'])}")
            print(f"Premissas: {', '.join(p['premises'])}")
            print(f"Conclusão: {p['conclusion']}")
    else:
        print("\n✗ Erro: Premissas não têm estrutura válida")
        if premises:
            print(f"Premissas recebidas: {premises}")
