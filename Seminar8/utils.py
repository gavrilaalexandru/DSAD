import pandas as pd
from pandas.core.dtypes.common import is_numeric_dtype


def nan_replace(df):
    for col in df.columns:
        if df[col].isna().any:
            if is_numeric_dtype(df[col]):
                # np.mean(df[col])
                val = df[col].mean()
                df[col].fillna(val, inplace=True)
            else:
                val = df[col].mode()
                # functia mode intoarce un output de forma
                # 0 abc
                # 1 def
                df[col].fillna(val[0], inplace=True)


def tabelare_matrice(x, nume_randuri=None, nume_coloane=None,
                     nume_fisier=None):
    df = pd.DataFrame(x, index=nume_randuri, columns=nume_coloane)

    if nume_fisier is not None:
        df.to_csv(nume_fisier)

    return df