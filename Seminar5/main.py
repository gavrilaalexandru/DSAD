import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy.dialects.mssql.information_schema import columns

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

df = pd.read_csv('res/employees.csv', index_col=0) # coloana cu indexul 0 este coloana cu id
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
coloane = ["Name", "Salary"]
subset = df[coloane]
# echivalent: df[coloane] = df[["Name", "Salary"]]

# citire pe randuri in fct. de index | iloc = index location
fr = df.iloc[0] # primul rand
ftr = df.iloc[0:3] # primele 3 randuri

# citire in functie de label/eticheta | loc
l1 = df.loc[1] # strict in acest caz, 1 se refera la eticheta 1, la stringul 1 din coloana ID; nu ca si pozitia (indexul)
# aici de exemplu
l2 = df.loc[1:3, ["Name", "Salary"]]

# filtrare boolean
f1 = df[df["Age"] > 30]
f2 = df[(df["Salary"] > 6000) & (df["Age"] < 40)]

#modificare in df
# adaugarea unei coloane noi
df["TaxedSalary"] = df["Salary"] * 0.9

df.rename(columns={"Salary": "GrossSalary"}, inplace=True)
df.rename(columns={"GrossSalary": "Salary"}, inplace=True)

df.drop(columns=["TaxedSalary"], inplace=True) # drop coloana TaxedSalary
df.drop(index=[6], inplace=True) # drop rand cu ID 6 (nu index)

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
df["Name"] = df["Name"].str.upper()

# statistici
# centrare = repozitionarea setului de date in jurul unei valori de referinta (valorea care va sta in centrul distributiei)
df["Salary_centered"] = df["Salary"] - df["Salary"].mean()

# scalare = aducerea termenilor la acelasi ordin de marine

# standardizare = centrare + scalare
df["Salary_std"] = (df["Salary"] - df["Salary"].mean()) / df["Salary"].std()