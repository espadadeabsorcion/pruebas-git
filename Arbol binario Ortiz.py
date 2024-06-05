import sys
from PyQt6.QtWidgets import QApplication, QMessageBox, QMainWindow, QWidget, QPushButton
from PyQt6.uic import loadUi 

class Nodo:
    def __init__(self, valor, padre=None):
        self.valor = valor
        self.hijo_izquierdo = None
        self.hijo_derecho = None
        self.padre = padre

    def es_hoja(self):
        return not self.hijo_izquierdo and not self.hijo_derecho

    def get_hermano(self):
        if self.padre is None:
            return None
        for hijo in self.padre.hijos:
            if hijo != self:
                return hijo
        return None
    
class Arbol_Binario:
    def __init__(self, root):
        self.root = Nodo(root)

    def agregar_hijo(self, padre, hijo_valor, lado):
        nodo_padre = self.buscar_nodo(self.root, padre)
        if nodo_padre:
            if lado == "izquierdo":
                nodo_padre.hijo_izquierdo = Nodo(hijo_valor, padre)
            else:
                nodo_padre.hijo_derecho = Nodo(hijo_valor, padre)
        else:
            print(f"No se encontró el Nodo {padre}")

    def buscar_nodo(self, nodo, valor):
        if nodo.valor == valor:
            return nodo
        if nodo.hijo_izquierdo:
            resultado = self.buscar_nodo(nodo.hijo_izquierdo, valor)
            if resultado:
                return resultado
        if nodo.hijo_derecho:
            resultado = self.buscar_nodo(nodo.hijo_derecho, valor)
            if resultado:
                return resultado
        return None
             
    def imprimir_arbol(self, nodo=None, nivel=0):
        if nodo is None:
            nodo = self.root
        print(" " * nivel + str(nodo.valor))
        if nodo.hijo_izquierdo:
            self.imprimir_arbol(nodo.hijo_izquierdo, nivel + 1)
        if nodo.hijo_derecho:
            self.imprimir_arbol(nodo.hijo_derecho, nivel + 1)
            
    def imprimir_hijos(self, padre_valor):
        nodo_padre = self.buscar_nodo(self.root, padre_valor)
        if nodo_padre:
            if nodo_padre.hijos:
                print(f"Hijos de {padre_valor}: {', '.join(str(hijo.valor) for hijo in nodo_padre.hijos)}")
            else:
                print(f"{padre_valor} no tiene hijos.")
        else:
            print(f"No se encontró el Nodo {padre_valor}")
            
    def imprimir_padre(self, hijo_valor):
        nodo_hijo = self.buscar_nodo(self.root, hijo_valor)
        if nodo_hijo:
            nodo_padre = self.buscar_padre(self.root, hijo_valor)
            if nodo_padre:
                print(f"El padre de {hijo_valor} es {nodo_padre.valor}")
            else:
                print(f"{hijo_valor} es el nodo raíz, no tiene padre.")
        else:
            print(f"No se encontró el Nodo {hijo_valor}")

    def buscar_padre(self, nodo, valor):
        for hijo in nodo.hijos:
            if any(nodo.valor == valor for nodo in hijo.hijos):
                return hijo
            resultado = self.buscar_padre(hijo, valor)
            if resultado:
                return resultado
        return None
 
    def index(self, valor):
        return self.buscar_posicion(self.root, valor)

    def buscar_posicion(self, nodo, valor, posicion_actual=0):
        if nodo.valor == valor:
            return posicion_actual
        for hijo in nodo.hijos:
            posicion_actual += 1
            resultado = self.buscar_posicion(hijo, valor, posicion_actual)
            if resultado != -1:
                return resultado
        return -1
    
    def imprimir_arbol_niveles(self, nodo=None, nivel=0):
        if nodo is None:
            nodo = self.root
        print(" " * nivel + str(nodo.valor))
        for hijo in nodo.hijos:
            self.imprimir_arbol_niveles(hijo, nivel + 1)
            
    def inorden(self, padre):

        recorrido = ""
        temporal = padre

        if temporal.hijo_izquierdo is not None:

            recorrido += self.inorden(temporal.hijo_izquierdo)
            
        recorrido += temporal.valor
            
        if temporal.hijo_derecho is not None:

            recorrido += self.inorden(temporal.hijo_derecho)
            
        return recorrido
    
    def inorden_completo(self):
        
        return(self.inorden(self.root))
    
    def preorden(self, padre):

        recorrido = ""
        temporal = padre
        
        recorrido += temporal.valor

        if temporal.hijo_izquierdo is not None:

            recorrido += self.preorden(temporal.hijo_izquierdo)
            
        if temporal.hijo_derecho is not None:

            recorrido += self.preorden(temporal.hijo_derecho)
            
        return recorrido
    
    def preorden_completo(self):
        
        return(self.preorden(self.root))
    
    def posorden(self, padre):

        recorrido = ""
        temporal = padre

        if temporal.hijo_izquierdo is not None:

            recorrido += self.posorden(temporal.hijo_izquierdo)
            
        if temporal.hijo_derecho is not None:

            recorrido += self.posorden(temporal.hijo_derecho)
        
        recorrido += temporal.valor
        
        return recorrido
    
    def posorden_completo(self):
        
        return(self.posorden(self.root))

class Menu(QMainWindow):
    
    def __init__(self, arbol):
        super().__init__()
        loadUi("fondo.ui", self)    
        self.arbol = arbol
        self.botonpre.clicked.connect(self.preorden)
        self.botonin.clicked.connect(self.inorden)
        self.botonpos.clicked.connect(self.posorden)

    def preorden(self):
        msg = QMessageBox(self)
        msg.setWindowTitle("Respuesta")
        msg.setText(f"Recorrido preorden \n{self.arbol.preorden_completo()}")
        msg.exec()        
        
    def inorden(self):
        msg = QMessageBox(self)
        msg.setWindowTitle("Respuesta")
        msg.setText(f"Recorrido inorden \n{self.arbol.inorden_completo()}")
        msg.exec()

        
    def posorden(self):
        msg = QMessageBox(self)
        msg.setWindowTitle("Respuesta")
        msg.setText(f"Recorrido posorden \n{self.arbol.posorden_completo()}")
        msg.exec() 
        
    
mi_Arbol = Arbol_Binario("F")
mi_Arbol.agregar_hijo("F","B","izquierdo")
mi_Arbol.agregar_hijo("F","G", "derecho")
mi_Arbol.agregar_hijo("B","A","izquierdo")
mi_Arbol.agregar_hijo("B","D", "derecho")
mi_Arbol.agregar_hijo("D","C","izquierdo")
mi_Arbol.agregar_hijo("D","E", "derecho")
mi_Arbol.agregar_hijo("G","I", "derecho")
mi_Arbol.agregar_hijo("I","H", "izquierdo")


app=QApplication(sys.argv)
main=Menu(mi_Arbol)
main.show()
app.exec()