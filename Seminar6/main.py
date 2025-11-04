import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# pandas = biblioteca pentru procesarea datelor tabelare (randuri si coloane)
# pandas pune la dispozitie 2 obiecte:
# 1. Series = date unidimensionale (coloane din csv)
# 2. DataFrame = data bidimensionale (foaia de calcul)

s = pd.Series([10, 20, 30], index=['a', 'b', 'c'])

# coloane/variabie/features
# randuri/index

df = pd.DataFrame({
    'Name': ['Alice', 'Bob', 'Carol'],
    'Age': [25, 27, 29],
    'Salary': [3000, 4500, 6000]
})

df = pd.read_csv('res/employees.csv', index_col=1) # coloana cu indexul 0 este coloana cu id
# proprietati pe df
print("df head\n", df.head()) # primele 5 randuri din df
print("df tail\n", df.tail()) # ultimele 5 randuri din df
print("df info\n", df.info()) # informatii despre structura df: tipuri de date, valori null
print("df describe\n", df.describe()) # statistici descriptive despre coloane
print("df shape\n", df.shape) # (rows, cols)
print("df columns\n", df.columns) # lista cu coloanele din df
print("df index\n", df.index) # lista cu referintele randurile din df

# accesul datelor
# citirea - se realizeaza folosind operatorul de indexare []

ages = df["Age"] # case sensitive
coloane = ["Gender", "Salary"]
subset = df[coloane]
# echivalent: df[coloane] = df[["Name", "Salary"]]

# citire pe randuri in fct. de index | iloc = index location
fr = df.iloc[0] # primul rand
ftr = df.iloc[0:3] # primele 3 randuri

# citire in functie de label/eticheta | loc;
l1 = df.loc["Bob"] # strict in acest caz, 1 se refera la eticheta 1, la stringul 1 din coloana ID; nu ca si pozitia (indexul)
# aici de exemplu
l2 = df.loc["Eva":"Ivy", ["Gender", "Salary"]]

# filtrare boolean
f1 = df[df["Age"] > 30]
f2 = df[(df["Salary"] > 6000) & (df["Age"] < 40)]

#modificare in df
# adaugarea unei coloane noi
df["TaxedSalary"] = df["Salary"] * 0.9

df.rename(columns={"Salary": "GrossSalary"}, inplace=True)
df.rename(columns={"GrossSalary": "Salary"}, inplace=True)

df.drop(columns=["TaxedSalary"], inplace=True) # drop coloana TaxedSalary
df.drop(index=["Carol"], inplace=True) # drop rand cu ID 6 (nu index)

# loc este valoarea si iloc este indexul

# data sanitization / curatarea datelor

# in general avem de a face cu una din urmatoarele situatii
# 1. operam cu date numerice
# 2. operam cu date categorice (gender, M sau F)
# cand vrei sa faci data sanitization ai 2 abordari: fie faci drop randurilor/coloanelor cu valori lipsa
# fie le inlocuiesti cu valori convenabil alese
# date numerice: media pe coloane sau o valoare utila in scenariul respectiv
# date categorice: modulul (valoarea cea mai frecvent intalnita) sau o valoare utila in scenaraiul respectiv

# depistarea valorilor lipsa
missing = df.isna().sum() # cate avem lipsa

# drop
df.dropna() # drop fiecarui rand care contine NaN (not a number/not available)
df.dropna(axis=1) # drop fiecarei coloane care contine NaN (in general 0 randuri, 1 coloane)

# replace
df.fillna(0)
df["Salary"].fillna(df["Salary"].mean(), inplace=True)

# transformari
# vectorizate
df["AgeInMonths"] = df["Age"] * 12

# lambda si apply
df["IncomeBracket"] = df["Salary"].apply(lambda x: "High" if x > 6000 else "Low")

# functii string
df["Gender"] = df["Gender"].str.lower()

# statistici
# centrare = repozitionarea setului de date in jurul unei valori de referinta (valorea care va sta in centrul distributiei)
df["Salary_centered"] = df["Salary"] - df["Salary"].mean()

# scalare = aducerea termenilor la acelasi ordin de marine

#standardizarea datelor
# standardizare = centrare + scalare
# valorile standardizate au valori in intervalul -inf:+inf si ca procedeu, standardizarea se foloseste atunci cand modelele de analize a datelor
# pornesc cu premiza ca datele respecta o distributie normala: ACP, regresiile
df["Salary_std"] = (df["Salary"] - df["Salary"].mean()) / df["Salary"].std()

# normalizarea datelor = aducerea valorilor unei variabile intr un interval adesea [0:1]
# normalizarea se face urmarind formula (xi - xmin) / (xmax - xmin)
# se intalneste in retele neuronale sau in aplicatii cu date de intrare cu domeniu finit de definite (procesarea de imagini)

# statistici descriptive
df["Salary"].mean() # media aritmetica
df["Salary"].median() # valoarea care imparte setul de date in 2 jumatati egale
df["Salary"].mode() # modul, cea mai intalnita valoare


# disperia datelor
df["Salary"].std() # abaterea medie patratica
df["Salary"].var() # varianta

# corelarea intre 2 variabile
df[["Age", "Salary"]].corr()

# daca valoarea e pozitiva: exista o relatie directa intre cele 2 var - daca una creste si cealalta creste, respectiv invers
# daca valoarea e negativa: exista o relatie inversa intre cele 2 var - daca una creste, cealalta scade si invers
# daca valoarea e in jurul lui 0 - variabilele sunt independente (nu se influenteaza una pe alta) (gradele de afara si PIB-ul tarii de ex)

# df["Salary"].hist(bins=15, edgecolor='orange')
# df["Age"].plot()
# plt.show()

# merge + groupby
df1 = pd.DataFrame({
    "ID": [1,2,3],
    "Name": ["Alice", "Bob", "Carol"]
})

df2 = pd.DataFrame({
    "ID": [4,5,6],
    "Name": ["Mark", "Eva", "Ivy"]
})

df3 = pd.DataFrame({
    "ID": [1,2,3],
    "Department": ["IT", "HR", "Finance"]
})

# merge by key
# exemplu de merge folosind o coloana - acest tip de operatie functioneaza doar in cazurile in care valoarea parametrului on exista
# in ambele data frames ca si variabila (df.columns, nu df.index)
merged = df1.merge(df3, on="ID")
print(merged)
print("\n")

# concatenare
concat = pd.concat([df1, df2])
print(concat)
print("\n")

# merge functioneaza similar cu un join in SQL; plecam de la ipoteza a 2 DF: df1 si d2, iar operatia de merge este de forma: df1.merge(df2)
# inner - randurile comune intre cele 2 DF
# left - toate randurile din DF1
# right - toate randurile din DF2
# outer - DF1 si DF2

employees = pd.read_csv('res/employees.csv')
departments = pd.read_csv('res/departments.csv')

# inner merge - doar randurile pt. care avem acelasi DepartmentID
inner = employees.merge(departments, on="DepartmentID", how="inner")
print("Inner merge:")
print(inner)

# left merge - toti employees chiar daca nu avem acelasi DepartmentID
left = employees.merge(departments, on="DepartmentID", how="left")
print("Left merge:")
print(left)

# right merge - toate departamentele chiar daca nu avem acelasi DepartmentID
right = employees.merge(departments, on="DepartmentID", how="right")
print("Right merge:")
print(right)

# outer merge - toate departamentele cu ID unic din ambele tabele
outer = employees.merge(departments, on="DepartmentID", how="outer")
print("Outer merge:")
print(outer)

# cazuri de merge atunci cand criteriul de merge va fi indexul si nu o coloana nume
tabel_etnii = pd.read_csv('res/Ethnicity.csv', index_col=0)
# nan_replace() - nu avem nevoie acum de el
variabile_etnii = list(tabel_etnii.columns)[1:] # - slicing

# calcul populatie pe etnii la nivel de judet
localitati = pd.read_excel('res/CoduriRomania.xlsx', index_col=0)

t1 = tabel_etnii.merge(right=localitati, right_index=True, left_index=True)
print(t1)

g1 = t1[variabile_etnii + ["County"]].groupby(by="County").agg(sum)
print(g1)

# calcul populatie pe etnii la nivel de regiuni
judete = pd.read_excel('res/CoduriRomania.xlsx', index_col=0, sheet_name="Judete")

t2 = g1.merge(right=judete, right_index=True, left_index=True)
print(t2)

g2 = t2[variabile_etnii + ["Regiune"]].groupby(by="Regiune").agg(sum)
print(g2)

# calcul populatie pe etnii la nivel de macroregiune
regiuni = pd.read_excel('res/CoduriRomania.xlsx', index_col=0, sheet_name="Regiuni")

t3 = g2.merge(right=regiuni, right_index=True, left_index=True)
print(t3)

g3 = t3.groupby(by="MacroRegiune").agg(sum)
print(g3)

g1.to_csv('res/output_etnii_judet.csv')
g2.to_csv('res/output_etnii_regiune.csv')
g3.to_csv('res/output_etnii_macroregiune.csv')

# indici de diversitate