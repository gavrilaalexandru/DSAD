import numpy as np
import pandas as pd
from sklearn.decomposition import PCA

from utils import nan_replace, tabelare_matrice

t = pd.read_csv("Freelancer.csv", index_col=1)
nan_replace(t)

variabile_observate = list(t.columns)[2:]

x_orig = t[variabile_observate]
# standardizarea datelor
x = (x_orig - np.mean(x_orig, axis=0,)) / np.std(x_orig, axis=0)

# dimensiuni
n, m = x.shape

# initializare model ACP prin apel de constructor + apelul metodei fit (antrenare pe datele disponibile)
model_acp = PCA()
model_acp.fit(x)

# alpha reprezinta valorile proprii (eigen values)
alpha = model_acp.explained_variance_
print("Alpha: ", alpha)

# a reprezinta vectorii proprii (eigen vectors) / loadings
a = model_acp.components_

# c reprezinta componentele principale rezultate in urma ACP, obtinute: c = x @ a transpus
# calculare rezultate
c= model_acp.transform(x)

# afisarea componentelor principale
labels = ["C" + str(i + 1) for i in range(len(alpha))]
componente_df = tabelare_matrice(c, t.index, labels, "componente_principale.csv")
# plot_componente(componente_df, "C1", "C2", aspect=1)

# criterii de identificare al numarului de componente principale semnificative
# Kaiser
# in ACP variabilele sunt standardizate - std pt. fiecare vi = 1
# criteriul Kaiser: se aleg acele comp. principale calculate care au std > 1
# (adica varianta explicata de comp. principale e mai mare decat a variabilelor initiale)
conditie = np.where(alpha > 1)
print("conditie Kaiser: ", conditie)
nr_comp_s_kaiser = len(conditie[0])
print("Componentele principale cf crit Kaiser: ", nr_comp_s_kaiser)

# Cattel
eps = alpha[0 : (m-1)] - alpha[1 : m]
sigma = eps[0 : (m-2)] - eps[1 : len(eps)]
indici_negativi = (sigma < 0)

if any(indici_negativi):
    conditie = np.where(indici_negativi) # np.where intoarce un tuplu similar cu (array([0, 1, 2, 3, 4, 5, 6]),)
    print("conditie Cattel: ", conditie)
    array_din_where = conditie[0] # extragem array-ul din tuplu
    indice_referinta = array_din_where[0] # primul element din array repr. pozitia cautata
    nr_comp_s_cattel = indice_referinta + 1
else:
    nr_comp_s_cattel =  None
print("Componente principale cf crit Cattel: ", nr_comp_s_cattel)

# procent de acoperire
ponderi = np.cumsum(alpha / sum(alpha))
print("ponderi cumulate: ", ponderi)
conditie = np.where(ponderi > 0.8)
nr_comp_s_procent = conditie[0][0] + 1 # explicatiile sunt aceleasi ca la Cattel
print(f"Componente principale cf crit procent de acoperire: {nr_comp_s_procent} \n")

# calculul corelatiilor dintre variabilele initiale si componentele principale
# corelatiile raspund la intrebari de forma: din ce se compun comp. principale
corr = np.corrcoef(x, c, rowvar=False)
print(f"Corrcoef: {corr.shape}, {n}, {m} \n, {corr}")

# !!!!!!!!!!!!
# atentie la indicii alesi
# daca dorim coef de corelatie intre x si c: corr[:m, m:]
# daca dorim coef de corelatie intre c si x: corr[m:, :m]
r_x_c = corr[:m, m:]
r_x_c_df = tabelare_matrice(r_x_c, variabile_observate, labels, "corelatii_factoriale.csv")

# corelograma(r_x_c_df)
# plot_corelatii(r_x_c_df, "C1", "C2")
# plot_corelatii(r_x_c_df, "C1", "C3")

# comunalitati - in ce masura varianta variabilelor initiale este pastrata in comp. principale
r_patrat = r_x_c ** 2
comunalitati = np.cumsum(r_patrat, axis=1)
comunalitati_df = tabelare_matrice(comunalitati, variabile_observate, labels, "comunalitati.csv")

# cosinusuri cat de bine sunt reprezentate randurile (df.index) in cadrul comp. principale
componente_patrat = c ** 2
sume = componente_patrat.sum(axis=1, keepdims=True) # sume pe randuri
cosin = componente_patrat / sume

cosin_df = tabelare_matrice(cosin, t.index, labels, "cosinusuri.csv")