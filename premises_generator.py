import os
import json
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

SYSTEM_PROMPT = """Você é um especialista em lógica proposicional e gerador de premissas de teste.

Seus objetivos são:
1. Gerar premissas válidas em lógica proposicional (consequências lógicas)
2. Gerar premissas inválidas em lógica proposicional (falácias lógicas)

FORMATO DE RESPOSTA JSON:
Sempre retorne um JSON com exatamente 4 premissas (2 válidas, 2 inválidas).
Cada premissa deve conter:
- propositions: lista das proposições usadas
- premises: lista de premissas
- conclusion: conclusão
- type: "VALID" ou "INVALID" (consequência lógica ou não)
- name: nome descritivo

Use os operadores formais:
- → (implicação)
- ∧ (conjunção)
- ∨ (disjunção)
- ¬ (negação)
- ↔ (bicondicional)

Seja conciso e direto."""

model = genai.GenerativeModel("gemini-3.1-flash-lite", system_instruction=SYSTEM_PROMPT)

def generate_premises() -> dict:
    """Gera 4 premissas: 2 válidas e 2 inválidas em lógica proposicional"""

    prompt = """Gere exatamente 4 premissas em lógica proposicional seguindo este padrão:

    PREMISSA 1 (VÁLIDA): Use Modus Ponens ou similar
    PREMISSA 2 (VÁLIDA): Use Silogismo Disjuntivo ou similar
    PREMISSA 3 (INVÁLIDA): Use Afirmação do Consequente ou similar
    PREMISSA 4 (INVÁLIDA): Use outra falácia diferente

    Para cada premissa, retorne EXATAMENTE neste formato JSON (sem explicação adicional):

    {
        "premises": [
            {
                "name": "Nome da Premissa 1",
                "type": "VALID",
                "propositions": ["p", "q"],
                "premises": ["p", "p → q"],
                "conclusion": "q"
            },
            {
                "name": "Nome da Premissa 2",
                "type": "VALID",
                "propositions": ["p", "q"],
                "premises": ["p ∨ q", "¬p"],
                "conclusion": "q"
            },
            {
                "name": "Nome da Premissa 3",
                "type": "INVALID",
                "propositions": ["p", "q"],
                "premises": ["p → q", "q"],
                "conclusion": "p"
            },
            {
                "name": "Nome da Premissa 4",
                "type": "INVALID",
                "propositions": ["p", "q", "r"],
                "premises": ["p → q", "q → r"],
                "conclusion": "p → r"
            }
        ]
    }

    Garanta que:
    - Exatamente 2 premissas têm type "VALID"
    - Exatamente 2 premissas têm type "INVALID"
    - Nomes descritivos em português
    - Operadores formais corretos"""

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
    print(f"Premissas salvas em {filename}")

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

    valid_count = sum(1 for p in premises["premises"] if p.get("type") == "VALID")
    invalid_count = sum(1 for p in premises["premises"] if p.get("type") == "INVALID")

    return valid_count == 2 and invalid_count == 2

if __name__ == "__main__":
    print("Gerando premissas em lógica proposicional...")
    print("=" * 60)

    premises = generate_premises()

    if premises and validate_premises_structure(premises):
        print("\n✓ Premissas geradas com sucesso!")
        print("\nResumo:")
        for i, p in enumerate(premises["premises"], 1):
            status = "✓ VÁLIDA" if p["type"] == "VALID" else "✗ INVÁLIDA"
            print(f"{i}. {p['name']} ({status})")

        save_premises_to_file(premises)

        print("\nDetalhes das premissas:")
        print("=" * 60)
        for i, p in enumerate(premises["premises"], 1):
            print(f"\nPremissa {i}: {p['name']}")
            print(f"Tipo: {p['type']}")
            print(f"Proposições: {', '.join(p['propositions'])}")
            print(f"Premissas: {', '.join(p['premises'])}")
            print(f"Conclusão: {p['conclusion']}")
    else:
        print("\n✗ Erro: Premissas não têm estrutura válida")
        if premises:
            print(f"Premissas recebidas: {premises}")
