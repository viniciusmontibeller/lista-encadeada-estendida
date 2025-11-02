from no import No, CAP

class ListaEncadeadaEstendida():
    def __init__(self):
        self.__inicio = None
        self.__cursor = None
        
    # caso de lista vazia, cria um novo no e direciona o inicio para o nó criado
    # percorre os nós até encontrar um em que o valor é menor que o maior valor do nó, ou seja, se for existir, estará nesse nó
    # caso o elemento que sera inserido ja existir apenas retorna garantindo a unicidade
    # em caso de o nó estar cheio realiza o split do array, retornando o novo nó (direita)
    # caso o novo elemento seja maior que o maior elemento dos elementos do nó gerador, o cursor vai para o novo nó e insere o elemento
    # com base no cursor insere-se o elemento mantendo a ordem
    def inserirOrdenado(self, valor):
        if self.__inicio is None:
            self.__inicio = No()
            self.__cursor = self.__inicio
            
        self.__posicionarCursorParaValor(valor)

        if self.__cursor.encontrar(valor) != -1:
            return
        
        if self.__cursor.getQuantidadeElementos() == CAP:
            direita = self.__cursor.splitMetade()
            
            if valor > self.__cursor.maiorValor():
                self.__cursor = direita
                
        indice = self.__cursor.limiteInferior(valor)
        self.__cursor.inserirNaPosicao(indice, valor)
    
    # usando o metodo auxiliar do cursor, navega ate a posicao desejada. Desloca o cursor, estacionando no nó onde o elemento esta inserido. 
    # Com o indice do nó selecionado, retorna o dado
    def acessaPosicao(self, posicao):
        _, i = self.__navegarPosicao(posicao)
        return self.__cursor.getDados()[i]
    
    # utilizando o método auxiliar de nevegarPosicao, temos o no anterior e o indice do elemento procurado
    # Remove-se o elemento do nó(array)
    # Verifica se o nó ficou vazio após a remoção do elemento, caso tenha ficado, se o nó excluido for o primeiro nó, desloca o inicio para o proximo do nó excluido
    # nos outros casos, redireciona o proximo do nó anterior para o proximo do nó que será apagado e redireciona o cursor para o proximo do nó que sera apagado
    # caso seja apagado o ultimo nó, cursor sera direcionado para None
    def excluiDaPosicao(self, posicao):
        anterior, i = self.__navegarPosicao(posicao)
        valor = self.__cursor.removerDaPosicao(i)
        
        if self.__cursor.getQuantidadeElementos() == 0:
            if anterior is None:
                self.__inicio = self.__cursor.getProximo()
            else:
                anterior.setProximo(self.__cursor.getProximo())
                
            self.cursorAvancarNo()
        return valor
    
    # percorre todos os nós, apresentando todos os elementos da lista
    def listarDados(self):
        elementos = []
        self.cursorApontaInicio()
        
        while self.__cursor is not None:
            for i in range(self.__cursor.getQuantidadeElementos()):
                elementos.append(self.__cursor.getDados()[i])
            self.cursorAvancarNo()
        
        return tuple(elementos)
    
    # Utilizando do método seguinte, retorna se o elemento existe na lista ou não
    def busca(self, valor):
        return self.posicaoDe(valor) != -1
    
    # percorre todos os nós, utilizando da verificação de se o maior elemento do nó é menor que o valor requisitado, acumulando a quantidade elementos e indo para o proximo nó
    # quando o valor for menor que o maior elemento do nó, verificamos se o elemento existe, e caso exista soma a quantidade acumulada e retorna a posicao do valor na lista
    # após percorrer todos os nós, caso nao encontre, retorna -1
    def posicaoDe(self, valor):
        posicao_acumulada = 0
        self.cursorApontaInicio()
        
        while self.__cursor is not None:
            if self.__cursor.maiorValor() < valor:
                posicao_acumulada += self.__cursor.getQuantidadeElementos()
                self.cursorAvancarNo()
                continue
            
            indice = self.__cursor.encontrar(valor)
            
            if indice != - 1:
                return posicao_acumulada + indice
            posicao_acumulada += self.__cursor.getQuantidadeElementos()
            self.cursorAvancarNo()
            
        return -1
    
    # percorre os nós acumulando a quantidade de elementos existente, retornando esse total.
    def total(self):
        total = 0
        self.cursorApontaInicio()
        while self.__cursor is not None:
            total += self.__cursor.getQuantidadeElementos()
            self.cursorAvancarNo()
        return total
    
    # --------- operacoes do cursor -------- #
    
    # move o cursor para o inicio
    def cursorApontaInicio(self):
        self.__cursor = self.__inicio
        
    # auxiliar para deslocar cursor com base no valor do elemento
    def cursorApontarPorValor(self, valor):
        self.__posicionarCursorParaValor(valor)
    
    # auxiliar de deslocamento do cursor
    def cursorAvancarNo(self):
        if self.__cursor is None:
            return
        self.__cursor = self.__cursor.getProximo()
    
    # Mostra informacoes do nó atual
    def cursorInfo(self):
        if self.__cursor is None: return "Nó inexistente"
        return {
            "quantidade de elementos":  {self.__cursor.__quantidade_elementos()},
            "elementos": {tuple(self.__cursor.getDados()[:self.__cursor.getQuantidadeElementos()])}
        }
    
    # auxiliar para mover o cursor para uma posicao. 
    # Move o cursor para o primeiro nó com maior valor de elemento maior que o valor passado. Caso nao exista, ou cursor fica no ultimo nó da fila
    # Verifica se o cursor atual possui seu menor valor maior que o valor passado, ou seja, o valor esta em nós anteriores, em caso contrario, parte do cursor ja presente na lista.
    # Caso positivo, recomeça do início. Como temos um encadeamento simples (proximo), so podemos avancar na lista, nao permitindo retroceder nela(posicoes negativas)
    def __posicionarCursorParaValor(self, valor):
        if self.__inicio is None:
            return

        if self.__cursor is None:
            self.cursorApontaInicio()
            
        if self.__cursor.getQuantidadeElementos() == 0:
            return
        
        if self.__cursor.menorValor() > valor:
            self.cursorApontaInicio()
        
        while self.__cursor.getProximo() is not None and self.__cursor.maiorValor() < valor:
            self.cursorAvancarNo()
        
    # Partindo do inicio, percorre a quantidade de elementos em cada nó para encontrar a posicao desejada
    # Desloca-se o nó e decrementa o valor da posicao com a quantidade de elementos do nó, retornando a posicao dentro do nó atual.
    def __navegarPosicao(self, posicao):
        if posicao < 0:
            raise IndexError("Valor de posição deve ser positivo")
        if self.__inicio is None:
            raise IndexError("Lista vazia")
        
        anterior = None
        self.cursorApontaInicio()
        
        while self.__cursor is not None:
            if posicao < self.__cursor.getQuantidadeElementos():
                return anterior, posicao
            posicao -= self.__cursor.getQuantidadeElementos()
            anterior = self.__cursor
            self.cursorAvancarNo()
            
        raise IndexError("Posicão não existente na lista")