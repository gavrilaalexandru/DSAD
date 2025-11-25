import pandas as pd
from pandas.api.types import is_numeric_dtype

def f(t,ani):
    assert isinstance(t,pd.DataFrame)
    return pd.Series(t.index[t[ani].values.argmax(axis=0)],ani)

def nan_replace_t(t):
    assert isinstance(t, pd.DataFrame)
    for v in t.columns:
        if any(t[v].isna()):
            if is_numeric_dtype(t[v]):
                t[v].fillna(t[v].mean(), inplace=True)
            else:
                t[v].fillna(t[v].mode()[0], inplace=True)

alcool = pd.read_csv("alcohol.csv",index_col=1)
nan_replace_t(alcool)
# print(alcool)
ani = list(alcool)[1:]
coduri = pd.read_csv("CoduriTariExtins.csv",index_col=2)

# 1
cerinta1 = alcool.apply(
    lambda x:pd.Series(
        [x["Country"],x.iloc[1:].mean()],
        ["Country","Consum Mediu"]
    ),
    axis=1)
cerinta1.sort_values(by="Consum Mediu",ascending=False,inplace=True)
cerinta1.to_csv("Cerinta1_1.csv")

# 2
cerinta2 = alcool.apply(
    lambda x:pd.Series(
        [x["Country"],x.index[x.iloc[1:].argmax()+1]],
        ["Country","Anul"]
    ),
    axis=1)
cerinta2.to_csv("Cerinta2.csv")

# 3
alcool_ = alcool[ani].merge(coduri[["Continent_Name"]],left_index=True,right_index=True)
cerinta3 = alcool_[["Continent_Name"]+ani].groupby(by="Continent_Name").agg(lambda x:x.std()/x.mean())
cerinta3.round(5).to_csv("Cerinta3_1.csv")

# 4
cerinta4 = alcool_.groupby(by="Continent_Name").apply(func=f,ani=ani)
cerinta4.to_csv("Cerinta4_1.csv")
