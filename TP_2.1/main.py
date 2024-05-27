from gcl import GeneradorLinealCongruencialMixto as gcl

def main():
  generador = gcl()
  print(generador)
  print(generador.next_seed())
  print(generador.next_float())
  print(generador.next_float_range(5, 4))
  print(generador.next_int_range(100, 200))

if __name__ == "__main__":
  main()