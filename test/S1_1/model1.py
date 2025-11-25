import numpy as np
import pandas as pd
from pandas.api.types import is_numeric_dtype

misc_nat = pd.read_csv("MiscareaNatLoc.csv",index_col=0)

indicatori = list(misc_nat)[1:]

# 1
cerinta1 = misc_nat[misc_nat["Divorturi"]>misc_nat["Casatorii"]]
cerinta1[["Localitate","Divorturi","Casatorii"]].to_csv("Cerinta1_2.csv")

# 2
populatia = pd.read_csv("PopulatieLocalitati.csv",index_col=0)
misc_nat_ = misc_nat.merge(populatia[["Judet","Populatie"]],left_index=True,right_index=True)
cerinta2 = misc_nat_.apply(
    lambda x:pd.Series(
        [x["Localitate"],x["NascutiVii"]*1000/x["Populatie"]],
        ["Localitate","NascutiVii_1000loc"]
    ),
    axis=1)
cerinta2.sort_values(by="NascutiVii_1000loc",ascending=False,inplace=True)
cerinta2.to_csv("Cerinta2_2.csv")

# 3
cerinta3 = misc_nat_[["Judet"]+indicatori].groupby(by="Judet").sum()
cerinta3.to_csv("Cerinta3_2.csv")

# 4
cerinta4 = misc_nat_[["Judet"]+indicatori].groupby(by="Judet").agg(lambda x:x.std()/x.mean())
cerinta4.round(5).to_csv("Cerinta4_2.csv")
