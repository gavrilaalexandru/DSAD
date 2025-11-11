import numpy as np
import pandas as pd


def diversitate(tabel, denumire_coloana=None):
    if denumire_coloana is not None:
        date = np.array(tabel.iloc[1:], dtype=float)
    else:
        date = np.array(tabel.values, dtype=float)

    suma = np.sum(date)
    proportii = date / suma

    # validare necesara din punct de vedere matematic pentru a evita calcularea de logaritmi din 0
    # codul de mai jos identifica acele pozitii pentru care avem valoarea 0 si le inlocuiesc cu 1
    indici_nuli = (proportii == 0)
    proportii[indici_nuli] = 1

    # definire indice de diversitate Shannon
    shannon = - np.sum(proportii * np.log(proportii))

    # definire indice de diversitate Simpson
    simpson = 1 - np.sum(proportii * proportii)

    if denumire_coloana is not None:
        results = pd.Series(data=[tabel.iloc[0], shannon, simpson], index=['denumire_coloana', 'Shannon', 'Simpson'])
    else:
        results = pd.Series(data=[shannon, simpson], index=['Shannon', 'Simpson'])
    return results