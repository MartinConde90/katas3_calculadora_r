class RomanNumber():
    value = 0
    __romanValue = ''

    __valores = {'I':1, 'V': 5, 'X':10, 'L': 50, 'C':100, 'D': 500, 'M': 1000}
    __valores5 = { 'V': 5,  'L': 50,  'D': 500 } 
    __simbolosOrdenados = ['I', 'V', 'X', 'L', 'C', 'D', 'M']

    __rangos = {
        0: {1: 'I', 5 : 'V', 'next': 'X'},
        1: {1: 'X', 5 : 'L', 'next': 'C'},
        2: {1: 'C', 5 : 'D', 'next': 'M'},
        3: {1: 'M', 'next': ''}
    }

    def __init__(self, value=None):
        if isinstance(value, int):
            self.value = value
            self.__romanValue = self.__arabigo_a_romano()
        elif isinstance(value, str):
            self.__romanValue = value
            self.value = self.__romano_a_arabigo()
        else:
            raise TypeError('Argumento de RomanNumber ha de ser un entero o una cadena')

    def cadenaAromano(self, cadena):
        self.__romanValue = cadena
        self.value = self.__romano_a_arabigo()

    def __invertir(self,cad):
        return cad[::-1] #para darle la vuelta a la cifra
        
    def __gruposDeMil(self): #no hay que informarle nada porque(abajo), todos las funciones sirven a la clase
        cad = str(self.value)#esto ya es self.value
        dac = self.__invertir(cad)
        grupos = []

        rango = 0
        for i in range(0, len(cad), 3): #desde 0 hasta len, de 3 en 3
            grupos.append([rango, int(self.__invertir(dac[i:i+3]))]) # hacemos otro invertir para poner los numeros al derecho
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

    def __arabigo_individual(self,valor): #aqui informamos *valor*, porque no es un atributo de la clase, no es general
        cad = self.__invertir(str(valor))
        res = ''

        for i in range(len(cad)-1,-1,-1): #con el numero invertido, comenzamos por el final, asi sabemos su longitud y que unidad es
            digit = int(cad[i])
            if digit <= 3:
                res += digit*self.__rangos[i][1] #el numero, multip por el simbolo romano que hay en ese rango y en esa posicion
            elif digit == 4:
                res += (self.__rangos[i][1]+self.__rangos[i][5]) #rangos se llama porque es propia de la clase
            elif digit == 5:
                res += self.__rangos [i][5]
            elif digit <9:
                res += (self.__rangos[i][5]+self.__rangos[i][1]*(digit-5))
            else:
                res += self.__rangos[i][1]+self.__rangos[i]['next']

        return res

    def __arabigo_a_romano(self): #aqui no ponemos valor, porque si que es el de la clase
        g1000 = self.__gruposDeMil()
        romanoGlobal = ''

        for grupo in g1000:
            rango = grupo[0]
            numero = grupo[1]
            if numero > 0:
                miRomano = '(' * rango + self.__arabigo_individual(numero) + ')'*rango
            else: 
                miRomano = ''
            romanoGlobal += miRomano

        return romanoGlobal

    def __numParentesis(self, cadena):
        num = 0
        for c in cadena: #cuenta los parentesis en cada grupo
            if c == '(':
                num += 1
            else:
                break
        return num

    def __contarParentesis(self):
        res = []
        grupoParentesis = self.__romanValue.split(')') # split elimina lo que le metas entre parentesis

        ix = 0
        while ix < len(grupoParentesis): # mientras ix sea menor que el numero de grupos de numeros
            grupo = grupoParentesis[ix]  # metemos el primero en grupo, ya que ix es 0
            numP = self.__numParentesis(grupo)  # metemos en numP, el numero de parentesis de ese grupo
            if numP > 0:                 # si el numero de parentesis es mayor que 0, entra
                if ix+numP >= len(grupoParentesis):
                    raise ValueError('Número de paréntesis incorrecto - Faltan cierres')
                for j in range(ix+1, ix+numP):     # para j, en el rango 1(en el primer caso) y el numero de parentesis
                    if grupoParentesis[j] != '':   #asi verifica que hay parentesis despues del numero, entre grupo y grupo
                        raise ValueError('Simbolos entre parentesis de cierre') #explota o Falla
                ix += numP - 1 # restamos 1 al numero de parentesis porque el numero de espacios entre ellos, es uno menos
                            # y asi tenemos el ix listo para que pase al siguiente grupo
            else:
                if len(grupoParentesis)-ix > 1:
                    raise ValueError('Número de paréntesis incorrecto - Sobran cierres')
            if len(grupo[numP:]) > 0: #si lo que va despues de los parentesis es mayor que 0
                res.append([numP, grupo[numP:]]) # metes el numero de parentesis y lo que va despues de los parentesis en el grupo
            ix += 1
        
        #Este if sirve para tratar los casos de parentesis mal formateados, compara los parentesis de uno con el siguiente
        for i in range(len(res)-1):
            if res[i][0] <= res[i+1][0]:
                raise ValueError('Numero de parentesis incorrecto')
        return res

    def __romano_individual(self, numRomano):
        numRepes = 1
        ultimoCaracter = ''
        numArabigo = 0

        for letra in numRomano:      
            #incrementamos el valor del numero arabigo con el valor numero del simbolo romano
            if letra in self.__valores:
                numArabigo += self.__valores[letra] #lo ponemos aqui ya que es una variable general
                if ultimoCaracter == '':
                    pass
                elif self.__valores[ultimoCaracter] > self.__valores[letra]: #si el numero es menor que el anterior
                    numRepes = 1
                elif self.__valores[ultimoCaracter] == self.__valores[letra]: #si hay dos numeros iguales seguidos
                    numRepes += 1
                    if letra in self.__valores and ultimoCaracter in self.__valores: #solo deberiamos comprobar uno, porque en el elif ya dice que son iguales
                        raise ValueError('Mas de un valor de 5 repetido')
                    if numRepes > 3:
                        raise ValueError('mas de 3 repeticiones')
                elif self.__valores[ultimoCaracter] < self.__valores[letra]: #cuando hay 2 numeros menores delante de uno mayor
                    if numRepes > 1: #no permite repeticiones en las restas
                        raise ValueError('No se ademiten repeticiones en restas')
                    if ultimoCaracter in self.__valores: #no permite restas de valores de 5 (5, 50, 500)
                        raise ValueError('No se pueden restar valores de 5')
                    distancia = self.__simbolosOrdenados.index(letra) - self.__simbolosOrdenados.index(ultimoCaracter) #No permite que se resten unidades de mas de un orden
                    if distancia > 2:
                        raise ValueError('Distancia en resta mayor de factor 2')
                    numArabigo -= self.__valores[ultimoCaracter] * 2
                    numRepes = 1

            else:  #si el simbolo romano no está permitido, devolvemos error (0)
                raise ValueError('Simbolo incorrecto') 

            ultimoCaracter = letra

        return numArabigo

    def __romano_a_arabigo(self):
        numArabigoTotal = 0
        res = self.__contarParentesis()

        for elemento in res:
            romano = elemento[1]
            factor = pow(10, 3 * elemento[0])

            numArabigoTotal += self.__romano_individual(romano) * factor

        return numArabigoTotal

    def __str__(self):
        return "{}".format(self.__romanValue)

    def __int__(self):
        return self.value

    def __repr__(self):
        return self.__romanValue

    def __add__(self, value): #self es el numero instanciado, el primero, y value es lo que queremos sumarle
        resultado = int(value) + self.value  #me haces el entero de value y a self le aplicas value para que sea entero
        resultado = RomanNumber(resultado)
        return resultado

    def __radd__(self, value): # con esta funcion espejo, si lo de arriba no se puede hacer, esto le da la vuelta los valores, y el value de arriba ahora es el self
        return self.__add__(value)

    def __sub__(self, value):
        resultado = max(0, self.value - int(value))
        resultado = RomanNumber(resultado)
        return resultado


    def __rsub__(self, value):
        return self.__sub__(value)

    def __mul__(self, value):
        resultado = int(value) * self.value
        resultado = RomanNumber(resultado)
        return resultado

    def __rmul__(self, value):
        return self.__mul__(value)

    def __truediv__(self, value):
        resultado = int(value) // self.value
        resultado = RomanNumber(resultado)
        return resultado

    def __rtruediv__(self, value):
        return self.__rtruediv__(value)

    def __div__(self, value):
        return self.__truediv__(value)
    
    def __rdiv__(self, value):
        return self.__div__(value)

    def __lt__(self, value):
        return int(self) < int(value)