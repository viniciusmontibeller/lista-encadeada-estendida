# Lista Encadeada Estendida (com Cursor)

Implementação de uma **lista simplesmente encadeada** onde cada nó contém um array fixo (CAP = 8) de inteiros **ordenados**.
A lista inteira permanece ordenada. Mantemos um **único cursor de nó** para navegação e para executar as operações. O projeto é didático e assume **valores únicos** diferentes de 0, sem levar em consideração acessar informação do elemento.

> **Ideia-chave:** reduzir ponteiros (1 para cada 8 dados), manter inserções ordenadas e evitar realocações grandes.

> **Invariantes**: valores únicos, nós nunca vazios (se zerar, o nó é removido), e ordenação local/global.

## Sumário

- [Visão geral](#visão-geral)  
- [Comportamento](#comportamento)
- [Decisões de implementação](#decisões-de-implementação)
    - [Busca](#busca)
    - [Exclusão](#exclusão)
- [Classes](#classes)
- [Exemplos rápidos](#exemplos-rápidos)  
- [Testes](#testes)
- [Boas Práticas e Limitações](#boas-práticas-e-limitações)  
- [Ideias de evolução](#ideias-de-evolução)

## Visão geral

- **Nó com capacidade fixa:** `CAP = 8` (array nativo do Python via `array('i')`).
- **Ordenação local:** cada nó mantém seus elementos **crescentes**. 
- **Ordenação global:** a concatenação dos nós é crescente.  
- **Valores únicos:** inserções checam duplicidade no nó candidato.
- **Nó nunca vazio:** se a contagem ficar 0 após exclusão, o nó é removido do encadeamento.
- **Cursor único:** ponteiro para o **nó atual**, usado em todas as navegações.
- **Sentinela visual:** posições não usadas iniciam em 0; a contagem define o que é válido.

## Comportamento

### Seleção do cursor(padrão de navegação)
- **Sempre que necessário posicionar pelo valor:**  
  1. Se o cursor está `None`, aponta para o início.
  2. Se o valor buscado é **menor** que `menorValor()` do nó atual, **move o cursor para o início**.
  3. Avança **somente para frente** enquanto `maiorValor() < valor` e existir próximo.
  >Como a lista é simplesmente encadeada, não há retrocesso entre nós.

### Inserção ordenada — `inserirOrdenado(valor)`
- Posiciona o cursor no **nó candidato** (primeiro com `max >= valor`, ou o último).
- Garante **unicidade:** `encontrar(valor)` no nó candidato.
- Nó **cheio** → `splitMetade()` (esquerda = `ceil`, direita = `floor`) e decide o **lado**:
  - Se `valor` for maior que o `maiorValor()` do nó da esquerda, o **cursor passa para a direita**.
- Insere na posição (`limiteInferior` — **busca binária**).

### Acesso por posição — `acessaPosicao(k)`
- Helper `__navegarPosicao(k)` percorre nós acumulando contagens até achar o **nó** e o **índice local**; cursor estaciona no nó certo.

### Contagem/Listagem
- `total()` soma contagens de todos os nós.
- `listarDados()` percorre do início acumulando os elementos válidos.

## Decisões de implementação

### Busca
- `busca(valor)` usa `posicaoDe(valor)` (índice global ou -1).
- Estratégia
    1. Cursor vai ao início.
    2. Pula **nós inteiros** enquanto `maiorValor() < valor`, acumulando a posição base.
    3. No **primeiro nó** com `maiorValor() >= valor`, executa `encontrar(valor)` (busca binária).
    4. Se achou, retorna `base + índice_local`, senão, segue a varredura (valor ausente).
    > Por que basta um nó? Os nós representam intervalos contíguos e a lista é ordenada; logo, existe no máximo um nó candidato.

### Exclusão
- `excluiDaPosicao(k)` retorna o valor removido.
- Estratégia:
    1. `__navegarPosicao(k)` desloca o **cursor** até o nó e calcula o **índice local** (também obtém o **anterior** para reencadear).
    2. `removerDaPosicao(i)` faz **shift** à esquerda dentro do nó.
    3. Se a contagem do nó ficar **0**, o nó é **removido**:
        - Se era o **primeiro**, `__inicio` recebe o próximo.
        - Caso contrário, `anterior.setProximo(cursor.getProximo())`.
        - Cursor passa para o **próximo do removido**.
    4. Não há **merge/rebalanceamento** entre nós após exclusão (não exigido).

## Classes

`No`
- Atributos: `__dados`, ` __quantidade_elementos`, `__proximo`.
- Principais métodos:
    - `menorValor()`, `maiorValor()` — metadados para pular nós;
    - `limiteInferior(v)`, `encontrar(v)` — busca binária.
    - `inserirNaPosicao(i, v)`, `removerDaPosicao(i)` — shifts;
    - `splitMetade()` — divide e encadeia o novo nó (direita).

`ListaEncadeadaEstendida`
- Atributos: `__inicio`, `__cursor`.
- Operações:
    - `inserirOrdenado(v)`, `acessaPosicao(k)`, `excluiDaPosicao(k)`,
    - `posicaoDe(v)`, `busca(v)`, `listarDados()`, `total()`,
    - helpers de cursor: `cursorApontaInicio()`, `cursorAvancarNo()`, `cursorApontarPorValor(v)`.

## Exemplos rápidos

```python
from lista_encadeada_estendida import ListaEncadeadaEstendida

lista = ListaEncadeadaEstendida()
for v in [3, 7, 9, 11, 18, 20, 21, 27]:
    lista.inserirOrdenado(v)

lista.inserirOrdenado(25)  # força split e insere no nó da direita
lista.inserirOrdenado(2)   # menor que todos
lista.inserirOrdenado(60)  # maior que todos

print(lista.listarDados())        # (2, 3, 7, 9, 11, 18, 20, 21, 25, 27, 60)
print(lista.posicaoDe(25))        # 8
print(lista.busca(999))           # False

pos = lista.posicaoDe(25)
print(lista.excluiDaPosicao(pos)) # 25
print(lista.listarDados())        # sem o 25
```

## Testes
O projeto inclui um arquivo de testes por prints que exercita as operações e imprime o estado da lista a cada passo

### Requisitos: 
1) Python 3.8+ (recomendado)
2) Estrutura: no.py, lista_encadeada_estendida.py
3) Testes: testes.py

```
python testes.py
# ou
python3 testes.py
```

> **Nota**: print_lista chama buscar, então move a seleção do cursor — isso é intencional no contexto de testes, apenas para imprimir a partir de um valor conhecido.

## Boas práticas e limitações
- `CAP` é constante e pequena (8); custos dentro do nó são limitados.
- Não há **merge/rebalanceamento** após exclusão (não requerido); nós podem ficar “meio cheios”.
- O array interno inicia com 0 apenas como **sentinela visual**; a **contagem** define o que está válido.
- O projeto assume **valores únicos** e inteiros diferentes de zero (compatível com array('i')).

## Ideias de evolução

- Redistribuição/merge em exclusão (opcional).
- Contador global de elementos para `total()` em.

## Author

[Github](https://github.com/viniciusmontibeller/lista-encadeada-estendida)