# liste
temperaturi = [15, 22, -3, 0, 7] # array normal
print("lista: ", temperaturi, type(temperaturi))
print("primul element: ", temperaturi[0])
print("ultimele doua elemente: ", temperaturi[-2:])

# tupluri
coordonate = (21, 45) # nu pot schimba valorile
# coordonate[0] = 33;

# dictionare
student = {"nume" : "Ana", "nota" : 10} # cheie valoare, cheia este unica
print(student["nume"], student.get("nota"))

# seturi
litere = set("analiza datelor") # elimina duplicate si random
print(litere)