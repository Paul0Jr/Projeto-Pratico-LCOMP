# Projeto-Pratico-LCOMP
Repositório voltado para entrega do projeto prático proposto na disciplina de Lógica para Computação.

# Proposta

Avaliar raciocínio de LLM com e sem demonstrações em LEAN. Gerar premissas e conclusao diretamente com formulas em logica proposicional.

Usar Z3 pra saber se é consequência lógica. Pedir para a LLM apresentar a prova usando a linguagem LEAN. Checar se a demonstracão está correta. 
Caso nao seja consequencia logica, pedir para a LLM dar um contra exemplo. Checar o contra exemplo. Comparar se acerta mais quando pedimos pra 
fornecer a demonstracao.

Usar o seguinte material sobre LEAN: https://leanprover.github.io/logic_and_proof_lean3/natural_deduction_for_propositional_logic.html

---

# Pré-requisitos
- Docker e Docker Compose instalados
- Chave da API Google Gemini - [obter aqui](https://aistudio.google.com/apikey)


# 📚 Estrutura do Projeto

```
├── solver.py          # Main - executa os exemplos com Z3 + Gemini
├── lean_prover.py     # Integração com Gemini API para gerar provas LEAN
├── requirements.txt   # Dependências Python
├── Dockerfile         # Configuração Docker
├── docker-compose.yml # Orquestração de containers
├── Makefile          # Atalhos para comandos comuns
└── README.md         # Este arquivo
```

---

# O que o projeto faz

## Verifica consequência lógica com Z3
- Dado um conjunto de premissas e uma conclusão
- Z3 verifica se é logicamente válido
- Usa SAT solving (insatisfiabilidade)

## Gera provas em LEAN (Gemini)
- Se é consequência: pede prova formal em LEAN 3
- Baseado em natural deduction (dedução natural)
- Segue o material: https://leanprover.github.io/logic_and_proof_lean3/

## Gera contra-exemplos (Gemini)
- Se NÃO é consequência: gera atribuição de valores
- Mostra proposições que falsificam o argumento

---