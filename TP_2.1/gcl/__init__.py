import time
import os

class  GeneradorLinealCongruencialMixto:
  def __init__(self, seed: int = int(os.getpid() * time.time()), 
               a: int =1664525, c: int =1013904223, m: int=2**32):
    self.ciclos = 0 
    self.parametros(seed, a, c, m)

  def parametros(self, seed, a, c, m):
    #se necesita primero m para poder validar los otros parametros
    self.set_m(m)
    self.set_seed(seed)
    self.set_a(a)
    self.set_c(c)    
  
  def next(self):
    self.seed = (self.a * self.seed + self.c) % self.m
    self.ciclos += 1
    return self.seed
  
  def next_float(self):
    return self.next() / self.m
  
  def next_float_range(self, min, max):
    if min >= max:
      raise ValueError("min debe ser menor a max")
    return min + (max - min) * self.next_float()
  
  def next_int_range(self, min, max):
    if min >= max:
      raise ValueError("min debe ser menor a max")
    return int(min + (max - min) * self.next_float())
  
  def set_seed(self, seed):
    if seed < 0 or seed >= self.m or seed == None:
      raise ValueError("Rango de seed: [0,m)")
    self.seed = seed
    self.first_seed = self.seed
  def set_a(self, a):
    if  a < 0 or a >= self.m or a == None:
      raise ValueError("Rango de a [0,m)")
    self.a = a
  def set_c(self, c):
    if c > self.m or c == None:
      raise ValueError("Rango de c (inf,m]")
    self.c = c
  def set_m(self, m):
    if m <= 0 or m == None:
      raise ValueError("Rango de m (0,inf)")
    self.m = m
  
  def __repr__(self):
    return "GLC: a={} c={} m={} seed={} \nciclo={} number={}".format(self.a, self.c, self.m, self.first_seed, self.ciclos, self.seed)

  def __str__(self):
    return "ciclo={} number={}".format(self.ciclos, self.seed)
  