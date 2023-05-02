# Importa a classe No do arquivo no.py
from no import No

# Abertura do arquivo .dat        
file = open('automato2.dat','r')

# Variavel tipo lista recebe todas as linhas individuais do arquivo
lines = file.readlines()

# Divide os estados em termos individuais separados por vírgula 
# Salva quantidade de elementos na variável qtd
qtd = len(lines[0].split(','))

# Alfabeto
lines[1].split(',')
sigma = lines[1].replace("\n","")

i=2 # -> as transições começam a partir da linha 3 do arquivo
objs = []

qtdTransit = 0
# Lê as transições enquanto não encontrar o estado inicial
while lines[i][0] != '>':
    lines[i] = lines[i].split(',')              # Separa origem, simbolo e destino
    lines[i][2] = lines[i][2].replace("\n","")  # Remove \n do final 
    objs.append(No(lines[i][0], lines[i][1], lines[i][2]))
    qtdTransit = qtdTransit + 1 
    if(len(objs) > 1):
        if(objs[-2].origin == objs[-1].origin):
            if(objs[-2].symbol == objs[-1].symbol):
                # Posições negativas acessam a lista do final para o inicio
                print("O autômato não é um AFD!")
                print("Devido as transições: δ({},{})={} e δ({},{})={}".format(
                      objs[-2].origin, objs[-2].symbol, objs[-2].destiny,
                      objs[-1].origin, objs[-1].symbol,objs[-1].destiny))
                exit()
    i = i+1 

# Separa e remove o caractere * dos estados finais
lines[-1] = lines[-1].replace("*","")
lines[-1] = lines[-1].split(',')
finals = lines[-1]

# Quantidade de estados finais
qtdfinal = len(lines[-1])

#Define matriz
table = [[' ' for i in range(qtd)] for j in range(qtd)]

for i in range(qtd-1):
    for j in range(i+1):
        table[i][j] = 'X '

#Definição dos testes
test1 = sigma[0],sigma[2]
test2 = sigma[0]+str(sigma[0]),sigma[0]+str(sigma[2]),sigma[2]+str(sigma[0]),sigma[2]+str(sigma[2])

#Analisa os estados equivalentes
for i in range(0,qtd-1):
    for j in range(0,qtd-1):
        if(table[i][j] == 'X '):
            if('q'+str(i+1) in finals) & ('q'+str(j) in finals):   
                table[i][j] = 'Ｏ'
            if(('q'+str(i+1) in finals) == False) & (('q'+str(j) in finals) == False):
                table[i][j] = 'Ｏ'

#Exibe tabela
print("Tabela de Relação após o passo 2")
for i in range(qtd-1):
    for j in range(qtd):
        print(table[i][j], end=' ')
    print()

# Função que busca a transição, dado um estado e simbolo, e retorna o estado de destino
def search(t,s):
    for i in range (0,qtdTransit):
        if(objs[i].origin == t) and (objs[i].symbol == s):
            return objs[i].destiny

estado = []
estado2 = []

#Testa os estados equivalentes com t=1
for i in range(0,qtd-1):#Percorre a tabela
    for j in range(0,qtd-1):
        if(table[i][j] == 'Ｏ'):       
                # Testa as entradas com qi+1
                for l in range(0,2):   # T1 há apenas 2 testes para cada estado
                    estado = search('q'+str(i+1),test1[l])
                    estado2 = search('q'+str(j),test1[l])  
                    if(estado in finals and estado2 not in finals) or (estado not in finals and estado2 in finals): # Se os estados não forem equivalentes
                        table[i][j] = '⊗ '
                    else: # t=2
                        for l in range(0,4): #T2 há 4 testes para cada estado
                            # Testa as entradas com qi+1
                            estado = search('q'+str(i+1),test2[l][0])
                            estado = search(estado,test2[l][1])
                            # Testa as entradas com qj
                            estado2 = search('q'+str(j),test2[l][0])
                            estado2 = search(estado2,test2[l][1])
                            if (estado in finals and estado2 not in finals) or (estado not in finals and estado2 in finals): # Se os estados não forem equivalentes
                                table[i][j] = '⊗ '

print("\nTabela de Relação do autômato minimizado")
for i in range(qtd):
    for j in range(qtd):
        print(table[i][j], end=' ')
    print()