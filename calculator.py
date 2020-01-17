from tkinter import *
from tkinter import ttk
from romannumber import *

HEIGHTBTN = 50
WIDTHBTN = 68

class CalcButton(ttk.Frame):
    def __init__(self, parent, text, command, wbtn= 1, hbtn=1): #parent es el contenedor donde fijo el widget
        ttk.Frame.__init__(self, parent, width=wbtn*WIDTHBTN, heigh=hbtn*HEIGHTBTN)

        self.pack_propagate(0)

        s = ttk.Style()
        s.theme_use('alt')
        s.configure('my.TButton', font='Helvetica')

        self.__btn = ttk.Button(self, text=text, command=command, style='my.TButton')
        self.__btn.pack(side=TOP, expand=TRUE, fill=BOTH)

class Display(ttk.Frame):
    cadena= '_'
    __maxnumbers = 12

    def __init__(self, parent):
        ttk.Frame.__init__(self, parent, width=4*WIDTHBTN, height=HEIGHTBTN)

        self.pack_propagate(0)
        
        s = ttk.Style()
        s.theme_use('alt')
        s.configure('my.TLabel', font='Helvetica 20')

        self.__lbl = ttk.Label(self,text=self.cadena, style='my.TLabel', anchor=E, background='black', foreground='white')
        self.__lbl.pack(side=TOP, fill=BOTH, expand=True)
    
    def addChar(self, caracter):
        if len(self.cadena) >= self.__maxnumbers:
            return

        if self.cadena == '_':
            self.cadena = ''
        self.cadena += caracter

        try:
            nr = RomanNumber(self.cadena)
        except ValueError:
                self.cadena = self.cadena[:-1]

        self.__lbl.config(text=self.cadena)

    def clear(self):
        self.cadena = '_'
        self.__lbl.config(text=self.cadena)

    def muestra(self, cadena):
        self.cadena = cadena
        self.__lbl.config(text=cadena)

class Selector(ttk.Frame):
    tipus = 'R'

    def __init__(self, parent, command, tipus='R'):
        ttk.Frame.__init__(self, parent, width=WIDTHBTN*2, height=HEIGHTBTN)

        self.pack_propagate(0)
        self.tipus = tipus
        self.command = command
    
        self.value = StringVar() #strinVar es un objeto de control de TKinter
        self.value.trace("w", self.selected) #trace, si se produce un cambio en su valor *value, va a llamar a una funcion determinada
                                             #si cambia a esto, me haces esto, en este caso A o R
        self.value.set(self.tipus)


        self.__rbR = ttk.Radiobutton(self, text='Romano', variable=self.value, value='R', command=lambda: command('R'))
        self.__rbA = ttk.Radiobutton(self, text='Arábigo', variable=self.value, value='A', command=lambda: command('A'))

        self.__rbR.pack(side=TOP, fill=BOTH, expand=True)
        self.__rbA.pack(side=TOP, fill=BOTH, expand=True)

    def selected(self, *args):
        self.command(self.value.get())

#A TRAVES DE PARENT, UNA CLASE SIEMPRE TIENE ACCESO A LOS METODOS Y ATRIBUTOS PUBLICOS DE SU PADRE



class Calculator(ttk.Frame):
    op1 = None
    operacion = None
    op2 = None

    cadena = ''
    __maxnumbers = 12

    def __createLayoutArabic(self):
        layoutArabic = ttk.Frame(self, name='layoutArabic') #ese self es calculator
        CalcButton(layoutArabic, text= 'C', command=self.clear).grid(column=0, row=0)
        CalcButton(layoutArabic, text= '+/-', command=None).grid(column=1, row=0)
        CalcButton(layoutArabic, text= '%', command=None).grid(column=2, row=0)
        CalcButton(layoutArabic, text='÷', command=lambda: self.operar('/')).grid(column=3, row=0)

        CalcButton(layoutArabic, text='7', command=lambda: self.addChar('7')).grid(column=0, row=2)
        CalcButton(layoutArabic, text='8', command=lambda: self.addChar('8')).grid(column=1, row=2)
        CalcButton(layoutArabic, text='9', command=lambda: self.addChar('9')).grid(column=2, row=2)
        CalcButton(layoutArabic, text='x', command=lambda: self.operar('x')).grid(column=3, row=2)

        CalcButton(layoutArabic, text='4', command=lambda: self.addChar('4')).grid(column=0, row=3)
        CalcButton(layoutArabic, text='5', command=lambda: self.addChar('5')).grid(column=1, row=3)
        CalcButton(layoutArabic, text='6', command=lambda: self.addChar('6')).grid(column=2, row=3)
        CalcButton(layoutArabic, text='-', command=lambda: self.operar('-')).grid(column=3, row=3)

        CalcButton(layoutArabic, text='1', command=lambda: self.addChar('1')).grid(column=0, row=4)
        CalcButton(layoutArabic, text='2', command=lambda: self.addChar('2')).grid(column=1, row=4)
        CalcButton(layoutArabic, text='3', command=lambda: self.addChar('3')).grid(column=2, row=4)
        CalcButton(layoutArabic, text='+', command=lambda: self.operar('+')).grid(column=3, row=4)

        CalcButton(layoutArabic, text='0', command=lambda: self.addChar('0')).grid(column=1, row=5)
        CalcButton(layoutArabic, text=',', command=lambda: self.addChar(',')).grid(column=2, row=5)
        CalcButton(layoutArabic, text='=', command=lambda: self.operar('=')).grid(column=3, row=5)
        return layoutArabic


    def __createLayoutRoman(self):
        layoutRoman = ttk.Frame(self, name='layoutRoman')
        self.buttonAC = CalcButton(layoutRoman, text="AC", command=self.clear, wbtn=3)
        self.buttonAC.grid(column=0, row=1, columnspan=3)
        #layaout en el parentesis, sustituye a *parent*, asi ya no depende de calculator y podemos alternar entre R y A
        self.buttonC = CalcButton(layoutRoman, text="C", command=lambda: self.addChar('C'))
        self.buttonC.grid(column=0, row=2)
        self.buttonD = CalcButton(layoutRoman, text="D", command=lambda: self.addChar('D'))
        self.buttonD.grid(column=1, row=2)
        self.buttonM = CalcButton(layoutRoman, text="M", command=lambda: self.addChar('M')) 
        self.buttonM.grid(column=2, row=2)

        self.buttonX = CalcButton(layoutRoman, text="X", command=lambda: self.addChar('X'))
        self.buttonX.grid(column=0, row=3)
        self.buttonL = CalcButton(layoutRoman, text="L", command=lambda: self.addChar('L'))
        self.buttonL.grid(column=1, row=3)
        self.buttonPL = CalcButton(layoutRoman, text="(", command=lambda: self.addChar('('))
        self.buttonPL.grid(column=2, row=3,)

        self.buttonI = CalcButton(layoutRoman, text="I", command=lambda: self.addChar('I'))
        self.buttonI.grid(column=0, row=4)
        self.buttonV = CalcButton(layoutRoman, text="V", command=lambda: self.addChar('V'))
        self.buttonV.grid(column=1, row=4)
        self.buttonPR = CalcButton(layoutRoman, text=")", command=lambda: self.addChar(')'))
        self.buttonPR.grid(column=2, row=4,)

        self.buttonDiv = CalcButton(layoutRoman, text="÷", command=lambda: self.operar('/'))
        self.buttonDiv.grid(column=3, row=1)
        self.buttonMul = CalcButton(layoutRoman, text="x", command=lambda: self.operar('x'))
        self.buttonMul.grid(column=3, row=2)
        self.buttonSub = CalcButton(layoutRoman, text="-", command=lambda: self.operar('-'))
        self.buttonSub.grid(column=3, row=3)
        self.buttonAdd = CalcButton(layoutRoman, text="+", command=lambda: self.operar('+'))
        self.buttonAdd.grid(column=3, row=4)


        self.buttonEqu = CalcButton(layoutRoman, text="=", command=lambda: self.operar('='), wbtn=2)
        self.buttonEqu.grid(column=2, row=5, columnspan=2)

        return layoutRoman

    def __init__(self, parent, modo='R'):
        ttk.Frame.__init__(self, parent)

        self.modo = modo

        self.pantalla = Display(self)
        self.pantalla.grid(column=0, row=0, columnspan=4)

        self.layoutRoman = self.__createLayoutRoman()

        self.layoutArabic = self.__createLayoutArabic()

        self.selector = Selector(self, command=self.eligeModo, tipus=self.modo)
        self.selector.grid(column=0, row=5, columnspan=2, sticky=W+S) #sticky = ponlo al oeste sur

    def operar(self, operacion):
        if operacion in ['+', '-', '/', 'x']:     
            if self.modo == 'R':
                self.op1 = RomanNumber(self.cadena)
            if self.modo == 'A':
                candidato = self.cadena.replace(',', '.')
                self.op1 = float(candidato)

            self.operacion = operacion
            self.clear()
        elif operacion == '=':
            if self.modo == 'R':
                self.op2 = RomanNumber(self.cadena)
            if self.modo == 'A':
                candidato = self.cadena.replace(',', '.')
                self.op2 = float(candidato)

            if self.operacion == '+':
                resultado = self.op1 + self.op2

            if self.operacion == '-':
                resultado = self.op1 - self.op2
            
            if self.operacion == '/':
                resultado = self.op1 / self.op2

            if self.operacion == 'x':
                resultado = self.op1 * self.op2

            if self.modo == 'A':
                resultado = str(resultado).replace('.', ',')
            self.pantalla.muestra(resultado)


    def eligeModo(self, modo):
        self.modo = modo
        if modo == 'A':
            print('Tengo que ser alfanumérica')
            self.layoutRoman.grid_forget()
            self.layoutArabic.grid(column=0, row=1, columnspan=4, rowspan=5)
        elif modo == 'R':
            print('Tengo que ser romana')
            self.layoutArabic.grid_forget()
            self.layoutRoman.grid(column=0, row=1, columnspan=4, rowspan=5)

        else:
            print('Modo "{}" erróneo'.format(modo))
            

    def clear(self):
        if self.modo == 'R':
            self.cadena = '_'

        if self.modo == 'A':
            self.cadena = '0'

        self.pantalla.muestra(self.cadena)


    
    def addChar(self, caracter):
        print(caracter)
        if len(self.cadena) >= self.__maxnumbers:
            return

        if self.modo == 'R':
            if self.cadena == '_':
                self.cadena = ''
            self.cadena += caracter


            try:
                nr = RomanNumber(self.cadena)
            except ValueError:
                self.cadena = self.cadena[:-1]


        if self.modo == 'A':
            if self.cadena == '0':
                self.cadena = ''
            self.cadena += caracter

            try:
                candidato = self.cadena.replace(',', '.')
                na = float(candidato)
            except ValueError:
                self.cadena = self.cadena[:-1]

        self.pantalla.muestra(self.cadena)
        print('cadena', self.cadena)