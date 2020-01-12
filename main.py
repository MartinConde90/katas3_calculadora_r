from tkinter import *
from tkinter import ttk

HEIGHTBTN = 50
WIDTHBTN = 68

class MainApp(Tk): #MainApp es en si una ventana, y le metemos Tk, del que va a heredar
   def __init__(self): #este es nuestro constructor
        Tk.__init__(self) #es el constructor de Tk, lo llamamos y le damos nuestra instancia
        self.title('Calculadora')
        self.geometry('{}x{}'.format(WIDTHBTN*4, HEIGHTBTN*4))
        
    def start(self):
        self.mainloop()

if __name__ == '__main__':
    app = MainApp()
    app.start()