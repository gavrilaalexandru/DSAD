from functools import reduce
import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# list comprehensions
numere_pp = []
for each in range(20):
    if each % 2 == 0:
        numere_pp.append(each ** 2)
print(numere_pp)

# echivalent cu blocul de cod de mai sus
numere_pp = [x ** 2 for x in range(20) if x % 2 == 0] # for -> parcurgere; in stanga -> mapare; in dreapta -> filtrare elemente
print(numere_pp)

celsius = [10, -5, 3, 17, 22, 28]
# f = 9/5 * c + 32
fahrenheit = [round(9/5 * c +32, 1) for c in celsius]
print("Celsius: ", celsius)
print("Fahrenheit: ", fahrenheit)

# dict comprehensions
nume = ["Ana", "Andrei", "Alina"]
note = [10, 9.5, 9]
catalog = {k: v for k, v in zip(nume, note)}
print(catalog, type(catalog),
      catalog.keys(), type(catalog.keys()),
      catalog.values(), type(catalog.values()),
      catalog.items(), type(catalog.items()))

# map(funct, iterable)
secventa = (1,2,3,4)
result = map(lambda x: x ** 2, secventa)
print(result, type(result), list(result))

# l1 = [1,2,3,4]
# l2 = list((1,2,3,4))
# l3 = list("ana") # citeste unul cate unul pentru ca ia un iterable

# filter(func, iterable)
temp_poz = filter(lambda t: t>= 0, celsius) # conditie; sa raspunda cu true/false
print(temp_poz, type(temp_poz), list(temp_poz))

# metode de filtrare folosind list comprehensions
note = [3, 7, 4, 5, 9, 10, 8]
promovat = [n for n in note if n >= 5]
status = ["promovat" if n>= 5 else "restant" for n in note]
print(promovat)
print(status)

emails = ["user@gmail.com", "user@stud.ase.ro", "user@yahoo.com"]
valid_emails = list(filter(lambda e: e.endswith("ase.ro"), emails))
print(valid_emails)

# reduce(funct, iterable)
suma = reduce(lambda a,b : a+b , note)
print(suma, "Media notelor: ", suma/len(note), sum(note)/len(note))

# numpy
# numpy ofera un obiect de tip ndarray, care spre deosebire de o lista built-in
# permite elemente de un singur tip (tip unic la nivel de ndarray), are o
# reprezentare continua in memorie si permite operatii de tip SIMD

l1 = [1, 4, 6, True, None, "ana", 'b', [5.6, 8]]
print(l1)
a = np.array([1,2,3])
b = np.array([
    [2.3, 5.8],
    [4.3, 2.1],
    [7.5, 12.3]
])

print("a: \n", a)
print("b: \n", b)

# proprietati
print("Forma (shape): ", b.shape)
print("Numar dimensiuni: ", b.ndim)
print("Tip de data: ", b.dtype)
print("Dimensiune element (item size byte): ", b.itemsize)
print("Numar elemente: ", b.size)
print("Dimensiune totala in memorie: ", b.nbytes)

print("Forma (shape): ", a.shape)
print("Numar dimensiuni: ", a.ndim)
print("Tip de data: ", a.dtype)

# indexing & slicing
c = [1,2,3,4,5]
print(c[0], len(c), c[len(c) - 1])

print(c[0: len(c) -1]) # forma gresita
print(c[0: len(c)]) # forma corecta

# numpy again
a = np.array([
    [1,2,3,4,5],
    [6,7,8,9,10]
])

# indexare
print(a[1,2], a[1][2])
# a[1,2] = 20
# print(a[1,2], a[1][2])

# slicing
print(a[0, 1:-1]) # 2, 3, 4
print(a[0, 1:-1:2]) # 2, 4
print(a[0, ::2]) # 1, 3, 5
print(a[0, :]) # 1, 2, 3, 4, 5
print(a[:, 3]) # 4, 9
print(a[:-1, 3]) # 4
