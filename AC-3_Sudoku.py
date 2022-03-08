import queue

cols = "ABCDEFGHI"	
filas = "123456789"

#Funçao para percorrer todas as filas e colunas do sudoku: ['A1', 'A2', 'A3', 'A4' ... I6', 'I7', 'I8', 'I9']
def percorrerSudoku(columnas, filas):
    return [c + f for c in columnas for f in filas]

elementos = percorrerSudoku(cols, filas)


class csp:
	def __init__(self, dominio=filas, num=""):
		self.variaveis = elementos # 81 variáveis --> X
		#self.dominio = self.dicionarioSudoku(num)  # o domíno --> D
		self.valores = self.dicionarioSudoku(num)  # gerar os valores

		""" Existem 27 restriçoes alldiff diferentes: 
						- uma para cada linha
						- uma para cada coluna
						- uma para cada quadrado 3 x 3
		"""

		# Todo o espaço do Sudoku
		# Array com varios arrays [[A1, B1, C1, D1, E1, F1, E1, G1, H1, I1], [A2, B2, C2, D2, E2, F2, E2, G2, H2, I2]...]
		self.unitlist = ([percorrerSudoku(cols, c) for c in filas] +  # cruzamento entre colunas com linhas
						 [percorrerSudoku(r, filas) for r in cols] +  # cruzamento de linhas com colunas
						 [percorrerSudoku(rs, cs) for rs in ('ABC', 'DEF', 'GHI') for cs in
						('123', '456', '789')])  # abrangencia de todos os espaços do sudoku

         #Para criar os arcos
		# estrutura da lista
		# Criamos um dicionario (dict) com par valor onde ex:
		# "A1" : [['A1', 'B1', 'C1', 'D1', 'E1', 'F1', 'G1', 'H1', 'I1'], ['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9'], ['A1', 'A2', 'A3', 'B1', 'B2', 'B3', 'C1', 'C2', 'C3']]
		# Ou seja, As restricçoes por linha [1 array], coluna [2 array] e quad(3x3) [3 array]
		self.units = dict((s, [u for u in self.unitlist if s in u]) for s in elementos)  # estrutura da lista

         #Faz um diccionario com por exemplo o elemento A1 com aqueles elementos pertenzesntes aos arcos que estao em zero
		# verificação dos pares
		# Criamos um dicionario (dict) com par valor onde ex:
		# "A1" : {'G1', 'C1', 'A6', 'B1', 'A5', 'B2', 'C3', 'A7', 'D1', 'B3', 'E1', 'H1', 'A3', 'A4', ...}
		# Ou seja, as restricoes num objecto ao qual o AI não pode ser igual
		self.pares = dict((s, set(sum(self.units[s], [])) - {s}) for s in elementos)  # verificação dos pares

		# restrições de pares duplicados
		# criamos o objecto onde vamos ter todas as comparacoes
		# (A1, A2), (A1, A3), (A1, A4)... (B1, B2), (B1, B3)...
		self.constraints = {(variable, par) for variable in self.variaveis for par in self.pares[variable]}  # restrições de pares duplicados
        
         #Isto cria um dicionario de para cada elemento asigna o domínio 1 até 9 caso nao tenha atribuido nada
         #{'A1': '123456789', 'A2': '123456789', 'A3': '3', 'A4': '123456789', 'A5': '2', 'A6': '123456789', 'A7': '6', 'A8': '123456789', 'A9': '123456789', 'B1': '9',
		# Receber uma string como input e retornar no dicionátio verificando que são numeors válidos
	def dicionarioSudoku(self, num=""):
		i = 0
		valores = dict()
		for elemento in self.variaveis:
			if num[i] != '0':
				valores[elemento] = num[i] #aqui o domínio é unico pois já é dado
			else:
				valores[elemento] = filas #aqui colocale o dominio total desde 1 até 9
			i = i + 1
		return valores


"""Implementação do algoritmo AC-3"""


"""Main AC-3 a recursividade acontece aqui dentro"""
def AC3(csp):
    q = queue.Queue() # Fila de arcos com todos os arcos do CSP
    for arc in csp.constraints:
        q.put(arc) #criamos a queue de arcos
    i = 0
    while not q.empty(): 
        (Xi, Xj) = q.get() #Remove o primeiro arco da lista
        i = i + 1
        if Revise(csp, Xi, Xj):#Aplicação da função revise que recebe o csp e as variaveis em causa
            if len(csp.valores[Xi]) == 0:#Após o revise das variaveis é verificado se o dominio esta vazio, se estiver nso existe solução
                return False
            for Xk in (csp.pares[Xi] - set(Xj)):
                q.put((Xk, Xi))
    return True


# WORKING OF THE REVISE ALGORITHM
def Revise(csp, Xi, Xj):
    revised = False
    dominio = set(csp.valores[Xi])#Coloca o dominio de Xi em values

    for x in dominio:#Vai iterar por todos os valores do dominio
        if not consistente(csp, x, Xi, Xj):#Função que verifica se o valor do dominio satisfaz a restrição
            csp.valores[Xi] = csp.valores[Xi].replace(x, '')#Caso nao satisfaça o valor é retirado do dominio
            revised = True

    return revised


# nconsistence que verifica se cada valor do dominio Xi satisfaz a restricao
def consistente(csp, x, Xi, Xj):
    for y in csp.valores[Xj]: #vai ver se algum valor de Xi e Xj é compatível
        if Xj in csp.pares[Xi] and y != x:#  Se o valor da variavel nao satifaz a restriçao ele returna true
            return True
    return False



def esqueleto(tabuleiro):

	lst = [x for x in tabuleiro]  # Criar uma lista nova com todos os elementos da lista puzzle

	for i, num in enumerate(lst):

		if i == 0: #Verifica se está no inicio da lista e coloca a | espaço e o numero
			print('| ', end='')		# | 2
			print(num, end=' ')		# | 1

		elif int(i + 1) % 27 == 0:	#| 5 4 8 | 1 3 2 | 9 7 6 |
			print(num, end=' |\n')	#| 9 6 7 | 3 4 5 | 8 2 1 |
			print("-" * 24)			#| 2 5 1 | 8 7 6 | 4 9 3 |
			print('| ', end='')		# ------------------------

		elif int(i + 1) % 9 == 0: #| 4 8 3 | 9 2 1 | 6 5 7 |
			print(num, end=' |\n')
			print('| ', end='')

		elif int(i + 1) % 3 == 0: #| 4 8 3 |
			print(num, end=' | ')

		else:
			print(num, end=' ')


if __name__ == "__main__":
	sudokuInicial = "003020600900305001001806400008102900700000008006708200002609500800203009005010300"


print("Sudoku Inicial\n")
esqueleto(sudokuInicial)
sudoku = csp(num=sudokuInicial)
print("\nSudoku Soluçao\n")
resolver = AC3(sudoku)
puzzleResolvido = "".join(str(sudoku.valores[x]) for x in sudoku.valores)
esqueleto(puzzleResolvido)

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    