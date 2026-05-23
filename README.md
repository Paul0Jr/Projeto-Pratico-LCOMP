# Projeto-Pratico-LCOMP
Repositório voltado para entrega do projeto prático proposto na disciplina de Lógica para Computação.

# Proposta

Avaliar raciocínio de LLM com e sem demonstrações em LEAN. Gerar premissas e conclusao diretamente com formulas em logica proposicional.

Usar Z3 pra saber se é consequência lógica. Pedir para a LLM apresentar a prova usando a linguagem LEAN. Checar se a demonstracão está correta. 
Caso nao seja consequencia logica, pedir para a LLM dar um contra exemplo. Checar o contra exemplo. Comparar se acerta mais quando pedimos pra 
fornecer a demonstracao.

Usar o seguinte material sobre LEAN: https://leanprover.github.io/logic_and_proof_lean3/natural_deduction_for_propositional_logic.html

# Executar com Docker

## Opção 1: Docker Compose (Recomendado)
```bash
docker-compose up
```

## Opção 2: Docker build + run
```bash
# Build
docker build -t lcomp-solver .

# Run
docker run -it -v $(pwd):/app lcomp-solver
```

## Opção 3: Run interativo
```bash
docker run -it -v $(pwd):/app lcomp-solver bash
```
"
