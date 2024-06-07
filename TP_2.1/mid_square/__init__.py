class MediosCuadrados:
    def __init__(self, seed, digits):
        if seed == 0:
          seed = 1
        self.seed = seed
        self.digits = digits
        self.current = seed

    def next(self):
        cuadrado = self.current ** 2
        cuadrado_str = str(cuadrado).zfill(2 * self.digits)
        arranque = (len(cuadrado_str) - self.digits) // 2
        self.current = int(cuadrado_str[arranque:arranque+self.digits])
        return self.current / (10 ** self.digits)

    def generar_secuencia(self, n):
        return [self.next() for _ in range(n)]