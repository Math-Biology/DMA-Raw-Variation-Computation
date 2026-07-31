# LINKED-TO: [REQ-COMP-P26.0073]
import pandas as pd
import xml.etree.ElementTree as ET
import os
import numpy as np
import re


def clean_filename(filename, replacement="_"):
    forbidden_chars = r'[<>:"/\\|?*.]'
    return re.sub(forbidden_chars, replacement, filename)


def load_config(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    file_config_element = root.find("./file_config")
    file_config = {}
    if file_config_element is not None:
        for child in file_config_element:
            file_config[child.tag] = child.text.strip() if child.text else "default_value"

    visit_config_element = root.find("./visit_config")
    visit_config = {}
    if visit_config_element is not None:
        for child in visit_config_element:
            visit_config[child.tag] = float(child.text.strip()) if child.text else "default_value"

    it_config_element = root.find("./it_config")
    it_config = {}
    if it_config_element is not None:
        for child in it_config_element:
            it_config[child.tag] = child.text.strip() if child.text else "default_value"

    return file_config, visit_config, it_config


file_config, visit_config, it_config = load_config("config.xml")

input_path = file_config["input_path"]
output_path = file_config["output_path"]

soglia1 = visit_config["threshold_1"]

original = it_config["original"]
percentage_variation = it_config["percentage_variation"]

cartella_originale = input_path

for folder_name in os.listdir(cartella_originale):
    folder_path = os.path.join(cartella_originale, folder_name)

    if not os.path.isdir(folder_path):
        print(f"{folder_name} non è una cartella")
        continue

    visita = folder_name
    print(f"Visita = {visita}")
    cartella = cartella_originale + visita
    files = os.listdir(cartella)

    for file in files:
        nome_file_senza_estensione = file.rstrip(".xlsx")
        cartella_destinazione = output_path + f"{visita}" + "_" + f"{nome_file_senza_estensione}"

        if file.endswith('.xlsx') or file.endswith('.xls') and '_p' not in file:
            percorso_file = os.path.join(cartella, file)
            df_dict = pd.read_excel(percorso_file, sheet_name=None)
            sheets_to_remove = {"Screening Protocol", "Notes"}
            df_dict = {name: df for name, df in df_dict.items() if name not in sheets_to_remove}

            for sheet_name, df in df_dict.items():
                df.replace({0: np.nan, None: np.nan, pd.NA: np.nan}, inplace=True)

                df_risultati = df.copy()

                for colonna in df.columns[1:]:
                    valori = df[colonna].values
                    valori_positivi = valori[valori > 0]
                    if len(valori_positivi) == 0:
                        continue

                    base = df[colonna][0]
                    valori_basali = df[colonna].values
                    min_val = min(x for x in valori_basali if x > 0)

                    if base != min_val:
                        base = min_val

                    variazioni_percentuali = [(valore - base) / base * 100 for valore in df[colonna][1:]]
                    df_risultati[colonna] = df_risultati[colonna].astype(float)
                    df_risultati.loc[1:, colonna] = variazioni_percentuali

                df_risultati = df_risultati.iloc[1:]

                sheet_name_clean = clean_filename(sheet_name)
                folder_out = cartella_destinazione + '_' + f"{sheet_name_clean}"
                if not os.path.exists(folder_out):
                    os.makedirs(folder_out)

                percorso_originale = os.path.join(folder_out,
                    f"{nome_file_senza_estensione}_{sheet_name_clean}_{original}.xlsx")
                df.to_excel(percorso_originale, index=False)

                percorso_variazione = os.path.join(folder_out,
                    f"{nome_file_senza_estensione}_{sheet_name_clean}_{percentage_variation}.xlsx")
                df_risultati.to_excel(percorso_variazione, index=False)

                print(f"Salvato: {percorso_variazione}")
