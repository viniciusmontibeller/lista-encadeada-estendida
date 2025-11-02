from array import array

CAP = 8

#aqui estamos usando o numero 0 como espaco vazio, poderia ser substituido para -1. Nesse caso estamos assumindo valores da lista como maiores que 0.
class No():
    def __init__(self):
        self.__dados = array('i', [0] * CAP)  # Iniciado 8 posicoes vazias
        self.__quantidade_elementos = 0
        self.__proximo = None
        
    def getDados(self):
        return self.__dados
    
    def getQuantidadeElementos(self):
        return self.__quantidade_elementos
        
    def getProximo(self):
        return self.__proximo
    
    def setProximo(self, proximoNo):
        self.__proximo = proximoNo
        
    # usado para verificar maior elemento no nó
    # pode ser utilizado para acelerar buscas, pulando o nó caso seja maior que o maior valor.
    def maiorValor(self):
        return self.__dados[self.__quantidade_elementos - 1] if self.__quantidade_elementos else None
    
    # usado para acelerar posicionamento do cursor, caso o valor da busca esteja antes do menor valor significa que a busca deve comecar do inicio
    def menorValor(self):
        return self.__dados[0] if self.__quantidade_elementos else None

    # no intervalo de elementos do array, vai selecionando partindo em "metades" retornando o valor inferior
    # busca binaria selecionando "metades", se maiores seleciona parte da direita, e se maiores a parte da esquerda
    # serve como auxiliar onde inserir mantendo a ordem
    def limiteInferior(self, valor):
        menor = 0
        maior = self.__quantidade_elementos

        while menor < maior:
            metade = (menor + maior) // 2
            if self.__dados[metade] < valor:
                menor = metade + 1
            else:
                maior = metade
        return menor

    # retorna o indice do valor procurado ou -1 caso nao encontre
    # tambem com busca binaria selecionando "metades", se maiores seleciona parte da direita, e se maiores a parte da esquerda
    # assumindo que os valores sao unicos nao e necessario validar em caso de duplicidade
    def encontrar(self, valor):
        menor = 0
        maior = self.__quantidade_elementos - 1

        while menor <= maior:
            metade = (menor + maior) // 2
            valor_metade = self.__dados[metade]
            if valor_metade == valor:
                return metade
            elif valor_metade < valor:
                menor = metade + 1
            else:
                maior = metade - 1
        return -1

    # verifica se ha espaco
    # insere o elemento "empurrando" os elementos para a direita (shift)
    # shift do final ate a posicao escolhida para nao ter sobrescrição
    # insere o valor e incrementa a quantidade de elementos
    def inserirNaPosicao(self, posicao, valor):
        if posicao < 0 or posicao > self.__quantidade_elementos or self.__quantidade_elementos >= CAP:
            raise IndexError("Valor de posição não é valido")
        for i in range(self.__quantidade_elementos, posicao, -1):
            self.__dados[i] = self.__dados[i - 1]
        self.__dados[posicao] = valor
        self.__quantidade_elementos += 1

    # remove o elemento da posicao escolhida e move os elementos para a esquerda, mantendo a sequencia
    # como foi feito o shift dos elementos ate o penultimo, zera o ultimo elemento para consistencia, como feito na inicialização
    # retorna o valor devolvido, caso desejar para mostrar
    def removerDaPosicao(self, posicao):
        if posicao < 0 or posicao >= self.__quantidade_elementos:
            raise IndexError("Valor de posição não é valido")
        valor = self.__dados[posicao]
        for i in range(posicao, self.__quantidade_elementos - 1):
            self.__dados[i] = self.__dados[i + 1]
        self.__dados[self.__quantidade_elementos - 1] = 0
        self.__quantidade_elementos -= 1
        return valor

    # dividir um no em dois, sendo o novo no construido apartir da metade direita do no atual
    # pegando o intervalo da metade direita, insere-se no novo no comecando do indice zero
    # apos mover, zera o indice no nó gerador para ficar apenas com a metade da esquerda
    # sabendo a quantidade de elementos do novo no (metade), atualiza seu contador de elementos
    # com a retirada de desses elementos atualiza-se a quantidade de elementos atuais
    # o proximo nó do novo nó criado herda do nó gerador, dando cuntinuidade a sequencia, e o proximo do nó gerador aponta para o novo nó
    # usando a divisao inteira, o nó da "esquerda" (nó gerador) tera quantidade de metade arredondada para cima, e o da "direita" (novo nó), tera quantidade da metade erredondada para baixo.
    def splitMetade(self):
        novo = No()
        metade = self.__quantidade_elementos // 2  # arredondado para o menor inteiro
        inicio = self.__quantidade_elementos - metade
        k = 0
        for i in range(inicio, self.__quantidade_elementos):
            novo.__dados[k] = self.__dados[i]
            self.__dados[i] = 0
            k += 1
        novo.__quantidade_elementos = metade
        self.__quantidade_elementos = inicio
        novo.__proximo = self.__proximo
        self.__proximo = novo
        return novo
