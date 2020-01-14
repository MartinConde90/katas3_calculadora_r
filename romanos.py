valores = {'I': 1, 'V': 5, 'X':10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}
valores_5 = {'V': 5,'L': 50,'D': 500}
simbolosOrdenados = ['I', 'V', 'X', 'L', 'C', 'D', 'M']

rangos = {
    0: {1: 'I', 5: 'V', 'next': 'X'},
    1: {1: 'X', 5: 'L', 'next': 'C'},
    2: {1: 'C', 5: 'D', 'next': 'M'},
    3: {1: 'M', 'next': 'X'},
}

def numParentesis(cadena):
    num = 0
    for c in cadena: #cuenta los parentesis en cada grupo
        if c == '(':
            num += 1
        else:
            break
    return num

def contarParentesis(numRomano):
    res = []
    grupoParentesis = numRomano.split(')') # split elimina lo que le metas entre parentesis

    ix = 0
    while ix < len(grupoParentesis): # mientras ix sea menor que el numero de grupos de numeros
        grupo = grupoParentesis[ix]  # metemos el primero en grupo, ya que ix es 0
        numP = numParentesis(grupo)  # metemos en numP, el numero de parentesis de ese grupo
        if numP > 0:                 # si el numero de parentesis es mayor que 0, entra
            for j in range(ix+1, ix+numP):     # para j, en el rango 1(en el primer caso) y el numero de parentesis
                if grupoParentesis[j] != '':   #asi verifica que hay parentesis despues del numero, entre grupo y grupo
                    return 0 #explota o Falla
            ix += numP - 1 # restamos 1 al numero de parentesis porque el numero de espacios entre ellos, es uno menos
                           # y asi tenemos el ix listo para que pase al siguiente grupo
        
        if len(grupo[numP:]) > 0: #si lo que va despues de los parentesis es mayor que 0
            res.append([numP, grupo[numP:]]) # metes el numero de parentesis y lo que va despues de los parentesis en el grupo
        ix += 1
    
    #Este if sirve para tratar los casos de parentesis mal formateados, compara los parentesis de uno con el siguiente
    for i in range(len(res)-1):
        if res[i][0] <= res[i+1][0]:
            return 0
    return res

def romano_individual(numRomano):
    numRepes = 1
    ultimoCaracter = ''
    numArabigo = 0

    for letra in numRomano:      
        #incrementamos el valor del numero arabigo con el valor numero del simbolo romano
        if letra in valores:
            numArabigo += valores[letra] #lo ponemos aqui ya que es una variable general

            if ultimoCaracter == '':
                pass

            elif valores[ultimoCaracter] > valores[letra]: #si el numero es menor que el anterior
                numRepes = 1

            elif valores[ultimoCaracter] == valores[letra]: #si hay dos numeros iguales seguidos
                numRepes += 1

                if letra in valores_5 and ultimoCaracter in valores_5: #solo deberiamos comprobar uno, porque en el elif ya dice que son iguales
                    return 0

                if numRepes > 3:
                    return 0

            elif valores[ultimoCaracter] < valores[letra]: #cuando hay 2 numeros menores delante de uno mayor
                if numRepes > 1: #no permite repeticiones en las restas
                    return 0

                if ultimoCaracter in valores_5: #no permite restas de valores de 5 (5, 50, 500)
                    return 0

                distancia = simbolosOrdenados.index(letra) - simbolosOrdenados.index(ultimoCaracter) #No permite que se resten unidades de mas de un orden
                if distancia > 2:
                    return 0

                numArabigo -= valores[ultimoCaracter] * 2
                numRepes = 1

        else: #si el simbolo romano no está permitido, devolvemos error (0)
            return 0 

        ultimoCaracter = letra

    return numArabigo

def romano_a_arabigo(numRomano):
    numArabigoTotal = 0
    res = contarParentesis(numRomano)

    for grupo in res: # recorres los grupos
        romano = grupo[1] #la posicion 1 de el grupo en el que estas, es decir el numero en si
        factor = pow(10, 3 * grupo[0]) #elevas a 10, el 3 multiplicado por el numero de parentesis
        numArabigoTotal += romano_individual(romano) * factor 

    return numArabigoTotal

def invertir(cad):
    return cad[::-1] #para darle la vuelta a la cifra
    
def gruposDeMil(num):
    cad = str(num)
    dac = invertir(cad)
    grupos = []
    rango = 0

    for i in range(0, len(cad), 3): #desde 0 hasta len, de 3 en 3
        grupos.append([rango, int(invertir(dac[i:i+3]))]) # hacemos otro invertir para poner los numeros al derecho
        rango += 1 #el rango son los parentesis, al leer el numero desde atras, vamos aumentando en 1 en cada grupo

    for i in range(len(grupos)-1): # restamos uno a la longitud para tener el numero real de item segun python
            grupoMenor = grupos[i] # grupo del que partimos
            grupoMayor = grupos[i+1] # grupo siguiente con el que comparamos
            unidadesMayor = grupoMayor[1] % 10 # si el resto de la posicion 1 del grupo (el numero, la 0 es el rango)
                                               #  da 4 o mas, se queda donde está
            if unidadesMayor < 4:              #si el resto da menor de 4, pertenece a los millares del grupo anterior
                grupoMenor[1] = grupoMenor[1] + unidadesMayor * 1000 # añadimos al grupo anterior, las unidades del mayor, por mil
                grupoMayor[1] = grupoMayor[1] - unidadesMayor    #al grupo mayor le quitamos sus unidades

    grupos.reverse()
    return grupos

def arabigo_individual(valor):
    cad = invertir(str(valor))
    res = ''

    for i in range(len(cad)-1,-1,-1): #con el numero invertido, comenzamos por el final, asi sabemos su longitud y que unidad es
        digit = int(cad[i])
        if digit <= 3:
            res += digit*rangos[i][1] #el numero, multip por el simbolo romano que hay en ese rango y en esa posicion
        elif digit == 4:
            res += (rangos[i][1]+rangos[i][5])
        elif digit == 5:
            res += rangos [i][5]
        elif digit <9:
            res += (rangos[i][5]+rangos[i][1]*(digit-5))
        else:
            res += rangos[i][1]+rangos[i]['next']

    return res

def arabigo_a_romano(valor):
    g1000 = gruposDeMil(valor)
    romanoGlobal = ''

    for grupo in g1000:
        rango = grupo[0]
        numero = grupo[1]
        if numero > 0:
            miRomano = '(' * rango + arabigo_individual(numero) + ')'*rango
        else: 
            miRomano = ''
        romanoGlobal += miRomano

    return romanoGlobal
