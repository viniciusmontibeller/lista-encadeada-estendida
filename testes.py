from lista_encadeada_estendida import ListaEncadeadaEstendida

# ----------------- helpers bem simples -----------------
def print_lista(lista: ListaEncadeadaEstendida, titulo: str = ""):
    if titulo:
        print(f"\n== {titulo} ==")

    linear = list(lista.listarDados())
    print("linear:", linear)

    try:
        partes = []
        lista.cursorApontaInicio()
        while True:
            info = lista.cursorInfo()
            if not info:
                break
            itens = list(info.get("elementos", ()))
            qtd   = info.get("quantidade de elementos", len(itens))
            if itens:
                partes.append("|" + ", ".join(map(str, itens)) + f"|({qtd})")
            if not lista.cursorAvancarNo():
                break
        if partes:
            print("nós:   ", " -> ".join(partes))
    except Exception:
        pass

print("---- INÍCIO DOS TESTES (Lista Encadeada Estendida) ----")

lista = ListaEncadeadaEstendida()

# 1) Operações em lista vazia (erros esperados)
print("\n[1] Operações em lista vazia")
print("total():", lista.total())
print_lista(lista, "lista vazia")

print("acessaPosicao(0) -> erro esperado")
try:
    lista.acessaPosicao(0)
except Exception as e:
    print("OK ->", repr(e))

print("excluiDaPosicao(0) -> erro esperado")
try:
    lista.excluiDaPosicao(0)
except Exception as e:
    print("OK ->", repr(e))

print("posicaoDe(999) ->", lista.posicaoDe(999))
print("busca(999)     ->", lista.busca(999))

# 2) Inserções básicas (preenche 1º nó)
print("\n[2] Inserções básicas (preenche 1º nó)")
for v in [3, 7, 9, 11, 18, 20, 21, 27]:
    lista.inserirOrdenado(v)
print_lista(lista, "após inserir 8 valores (1 nó cheio)")

# 3) Inserção que força split e cai no nó correto
print("\n[3] Inserir 25 (split + inserir no nó da direita)")
lista.inserirOrdenado(25)
print_lista(lista, "após inserir 25")

# 4) Inserções de extremos
print("\n[4] Inserir extremos 2 e 60")
lista.inserirOrdenado(2)
lista.inserirOrdenado(60)
print_lista(lista, "após inserir 2 e 60")

# 5) Inserir menor que o nó do cursor (garante que o cursor “volta ao início”)
print("\n[5] Inserir menor que o nó do cursor")
lista.posicaoDe(27)  # move cursor para perto do fim
lista.inserirOrdenado(1)  # deve ir ao primeiro nó
print(list(lista.listarDados()))

# 6) Duplicata (não deve alterar)
print("\n[6] Inserir duplicado 21 (sem alteração esperada)")
ret = lista.inserirOrdenado(21)
print("retorno inserirOrdenado(21):", ret)
print_lista(lista, "após tentar duplicar 21")

# 7) Acessos e buscas
print("\n[7] Acessos e buscas")
print("total():", lista.total())
print("acessaPosicao(0):", lista.acessaPosicao(0))
print("acessaPosicao(total-1):", lista.acessaPosicao(lista.total() - 1))
meio = lista.total() // 2
print(f"acessaPosicao({meio}):", lista.acessaPosicao(meio))

print("posicaoDe(25):", lista.posicaoDe(25))
print("posicaoDe(999):", lista.posicaoDe(999))
print("busca(20):", lista.busca(20))
print("busca(999):", lista.busca(999))

# 8) Acessa/Exclui fora do intervalo (com lista não vazia):
print("\n[8] Acessa/Exclui fora do intervalo")
try: lista.acessaPosicao(lista.total())  # deve dar IndexError
except Exception as e: print("OK ->", repr(e))
try: lista.excluiDaPosicao(lista.total())  # deve dar IndexError
except Exception as e: print("OK ->", repr(e))

# 9) Exclusões: início, meio, fim
print("\n[9] Exclusões diversas")
print("excluiDaPosicao(0) ->", lista.excluiDaPosicao(0))  # remove primeiro
print_lista(lista, "após remover primeiro")

pos25 = lista.posicaoDe(25)
print(f"excluiDaPosicao(posicaoDe(25)={pos25}) ->", lista.excluiDaPosicao(pos25))  # remove 25
print_lista(lista, "após remover 25 (meio)")

print("excluiDaPosicao(total-1) ->", lista.excluiDaPosicao(lista.total() - 1))  # remove último
print_lista(lista, "após remover último")

# 10) Remover vários do início (para possivelmente eliminar um nó inteiro)
print("\n[10] Remover 4 do início (se possível)")
for _ in range(min(4, lista.total())):
    lista.excluiDaPosicao(0)
print_lista(lista, "após remover 4 do início")

# 11) Esvaziar completamente
print("\n[11] Esvaziar completamente com exclusões na posição 0")
while lista.total() > 0:
    lista.excluiDaPosicao(0)
print_lista(lista, "lista após esvaziar")

# 12) Erros esperados novamente em vazia
print("\n[12] Erros esperados em lista vazia (novamente)")
try:
    lista.acessaPosicao(0)
except Exception as e:
    print("acessaPosicao(0) ->", repr(e))
try:
    lista.excluiDaPosicao(0)
except Exception as e:
    print("excluiDaPosicao(0) ->", repr(e))

print("\n---- FIM DOS TESTES ----")