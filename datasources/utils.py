from math import sqrt

class Distribucion:
    def __init__(self, n):
        self.n = n
        self.elementos = []

    #def set_valor_prob(self, valor, prob):
    #    self.elementos.append((valor,prob))

    def media(self):
        suma = 0
        for i in self.elementos:
            suma += i
        return suma/float(self.n)

    def varianza(self):
        suma = 0
        for i in self.elementos:
            suma += i ** 2 
        return suma - self.media() ** 2

    def desviacion(self):
        return sqrt(self.varianza())        

    def mediana(self):
        middle = self.n/2
        if self.n%2==0:
            res = (self.elementos[middle]+self.elementos[middle+1])/2.0
        else:
            res = self.elementos[middle+1]/2.0
        return res

    def minimo(self):
        return min(self.elementos)
    
    def maximo(self):
        return max(self.elementos)

    def rango(self):
        return self.maximo() - self.minimo() 
