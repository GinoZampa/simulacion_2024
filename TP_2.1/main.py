from gcl import GeneradorLinealCongruencialMixto as randu_generator
from mid_square import middleSquareGenerator as mid_square_generator


def main():
  randu()
  #mid_square()

def randu():
  generador = randu_generator()
  print(generador.__repr__())
  print(generador.next())
  print(generador.next_float())
  print(generador.next_float_range(4, 5))
  print(generador.next_int_range(100, 200))
  print(generador)
  print(generador.valores)

def mid_square():
  generador = mid_square_generator(1931)
  print(generador.__repr__())
  print(generador.next())
  print(generador.next())
  print(generador.next())
  print(generador.next())
  print(generador)
  print(generador.valores)

if __name__ == "__main__":
  main()