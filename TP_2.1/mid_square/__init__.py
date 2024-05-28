import time
import os

class  middleSquareGenerator:
  def __init__(self, seed: int = None):
    self.ciclo = 0
    self.valores = []
    if seed == None or seed <= 1 : #si no se pasa seed se toma el pid del proceso y el tiempo actual
      self.seed = int(str(int(os.getpid() * time.time())).zfill(8)[:8])
      self.first_seed = self.seed
    else:
      self.seed = seed 
      self.first_seed = self.seed

  def next(self):#trnasforma a strin ve si tiene 8 digitos toma los 4 del medio y los eleva al cuadrado
    if self.ciclo == 0: 
      self.ciclo += 1
      self.seed = self.seed * self.seed
      self.valores.append([self.ciclo, self.seed])
      return self.seed
    self.seed = str(self.seed)
    if self.seed.__len__() != 8:
      self.seed = self.seed.zfill(8)[:8]
    self.seed = int(self.seed[2:6])
    self.seed = self.seed * self.seed
    self.ciclo += 1
    self.valores.append([self.ciclo, self.seed])
    return self.seed
  
  def next_float(self):
    return self.next() / 10000000
  
  def next_float_range(self, min, max):
    if min >= max:
      raise ValueError("min debe ser menor a max")
    return min + (max - min) * self.next_float()
  
  def next_int_range(self, min, max):
    if min >= max:
      raise ValueError("min debe ser menor a max")
    return int(min + (max - min) * self.next_float())
  
  def __repr__(self) -> str:
    return "mid_square: seed={} \nciclo={} number={}".format(self.first_seed, self.ciclo, self.seed)
  
  def __str__(self):
    return "ciclo={} number={}".format(self.ciclo, self.seed)