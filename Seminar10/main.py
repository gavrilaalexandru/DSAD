import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sb
from factor_analyzer import FactorAnalyzer, calculate_kmo, calculate_bartlett_sphericity
from pandas.core.dtypes.common import is_numeric_dtype

def nan_replace(df):
    for col in df.columns:
        if df[col].isna().any():
            if is_numeric_dtype(df[col]):
                df[col].fillna(df[col].mean(), inplace=True)
            else:
                df[col].fillna(df[col].mode()[0], inplace=True)

def to_dataframe(x, row_names, col_names, filename):
    df = pd.DataFrame(x, index=row_names, columns=col_names)
    df.to_csv(filename)
    return df

def scree_plot(valori_proprii):
    """
    Reprezentam grafic valorile proprii, in ordine
    Acest grafic ne ajuta sa decidem cati factori latenti sunt semnificativi pt AnalizaFactoriala
    Acest nr se det fol criteriul lui Kaiser: se pastreaza drept factori latenti
    acesi factori care au valoarea proprie asociata > 1
    """

    plt.figure(figsize=(8, 6))
    plt.plot(range(1, len(valori_proprii) + 1), valori_proprii, marker="o")
    plt.title("Scree plot")
    plt.xlabel("Componenta/Factor")
    plt.ylabel("Valoare proprie")
    plt.axhline(1, color="red", linestyle="--")
    plt.show()

def heatmap(df, vmin=0, vmax=1, title="Heatmap"):
    """
    Grafic de uz general folosit pentru a reprezenta legaturile intre:
    - corelatii
    - comunalitati
    - factori de incarcare(loadings)
    """

    plt.figure(figsize=(8,6))
    sb.heatmap(df, vmin=vmin, vmax=vmax, annot=True, cmap="RdYlGn")
    plt.title(title)
    plt.show()

def main():
    # citim datele
    df = pd.read_csv("res/freelancer.csv", index_col=1)
    nan_replace(df)

    variable_names = list(df.columns)[2:]
    x = df[variable_names].values

    # teste care raspund intrebarii: se preteaza setul nostru de date la analiza factoriala?
    # teste posibile: Bartlett si KMO
    # Testul Bartlett verifica daca matricea coef. de corelatie difera semnificativ de matricea identitate I
    # testul bartlett este un test de tip Student, unde H0: nu exista corelatie intre date

    # testul KMO verifica daca exista date partiale intre date si cat de compacte sunt acestea

    chi2, p_value = calculate_bartlett_sphericity(x)
    print(f"Bartlett: chi2 = {chi2}, p_value = {p_value}")
    if p_value > 0.05:
        # daca p_value > 0.05 matricea coef de corelatie nu e diferita de I
        print("Bartlett p_value este prea mare, iar prin urmare se accepta ipoteza nula - nu exista factori latenti")
        return

    kmo_all, kmo_overall = calculate_kmo(x)
    print(f"KMO: {kmo_overall}")
    if kmo_overall < 0.6:
        # Analiza factoriala se preteaza pentru care au kmo overall cel putin egal cu 0.6
        print("KMO value prea mic, prin urmare nu exista factori latenti")
        return

    # initializare model AF
    fa_n = FactorAnalyzer(rotation=None)
    fa_n.fit(x)

    valori_proprii, _ = fa_n.get_eigenvalues()
    print("Valori proprii: ", valori_proprii)

    # folosind crit. Kaiser vom considera ca fiind semnificativi acei factori cu val. prop. > 1
    n_factori = sum(valori_proprii > 1)
    print("Numar factori latenti semnificativi: ", n_factori)

    scree_plot(valori_proprii)

    # reinitializare model AF folosind n_factori si rotation
    # rotation = 'varimax' - metoda de maximizare a disperiei fiecarui factor
    fa = FactorAnalyzer(n_factors=n_factori, rotation="varimax")
    fa.fit(x)

    factor_labels = [f"F{i+1}" for i in range(n_factori)]

    # loadings = reprezinta cat de importanti sunt factorii latenti pentru fiecare variabila initiala
    # principalul output al AF

    loadings = fa.loadings_
    loadings_df = to_dataframe(loadings, variable_names, factor_labels, "Loadings.csv")
    print("Loadings: ", loadings_df)

    heatmap(loadings_df, vmin=-1, vmax=1, title="Factor loadings")

    # comunalitati - proportia dispersiei explicate de catre toti factorii latenti combinati impreuna pentru fiecare variabila initiala
    comunalitati = fa.get_communalities()
    comunalitati_df = to_dataframe(comunalitati, variable_names, ["Comunalitati"], "Comunalitati.csv")
    heatmap(comunalitati_df, vmin=0, vmax=1, title="Comunalitati")

    # dispersia (varianta) explicata
    # - dispersia la nivel de fiecare factor
    # - dispersia ca proportie
    # - dispersia cumulata
    dispersie, proportie_dispersie, dispersie_cumulata = fa.get_factor_variance()
    dispersie_df = pd.DataFrame({
        "Dispersie": dispersie,
        "Proportie": proportie_dispersie,
        "Cumulat": dispersie_cumulata
    }, index=factor_labels)
    dispersie_df.to_csv("Dispersie.csv")
    print("Dispersie: ", dispersie_df)

    # scorurile factorilor = coordonatele observatiilor (randurilor) initiale in spatiul factorilor latenti
    scoruri = fa.transform(x)
    scoruri_df = to_dataframe(scoruri, df.index, factor_labels, "Scoruri.csv")

    # vizualizare a informatiilor in spatiul lui F1 si F2
    plt.figure(figsize=(8,6))
    plt.scatter(scoruri_df["F1"], scoruri_df["F2"])

    for i in range(len(scoruri_df)):
        plt.text(scoruri_df["F1"].iloc[i], scoruri_df["F2"].iloc[i], scoruri_df.index[i])

    plt.title("Scoruri factoriale F1 vs F2")
    plt.xlabel("F1")
    plt.ylabel("F2")
    plt.show()

main()
