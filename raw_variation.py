# COMPONENT: #L001-U015-P26.0234
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


def compute_percentage_variations(df):
    df_results = df.copy()

    for column in df.columns[1:]:
        values = df[column].values
        positive_values = values[values > 0]
        if len(positive_values) == 0:
            continue

        base = df[column][0]
        baseline_values = df[column].values
        min_val = min(x for x in baseline_values if x > 0)

        if base != min_val:
            base = min_val

        percentage_variations = [(value - base) / base * 100 for value in df[column][1:]]
        df_results[column] = df_results[column].astype(float)
        df_results.loc[1:, column] = percentage_variations

    df_results = df_results.iloc[1:]
    return df_results


def run(config_path="config.xml"):
    file_config, visit_config, it_config = load_config(config_path)

    input_path = file_config["input_path"]
    output_path = file_config["output_path"]

    threshold1 = visit_config["threshold_1"]  # noqa: F841

    original = it_config["original"]
    percentage_variation = it_config["percentage_variation"]

    input_folder = input_path

    for folder_name in os.listdir(input_folder):
        folder_path = os.path.join(input_folder, folder_name)

        if not os.path.isdir(folder_path):
            print(f"{folder_name} is not a folder")
            continue

        visit = folder_name
        print(f"Visit = {visit}")
        visit_folder = input_folder + visit
        files = os.listdir(visit_folder)

        for file in files:
            filename_no_ext = os.path.splitext(file)[0]
            output_folder = output_path + f"{visit}" + "_" + f"{filename_no_ext}"

            if file.endswith('.xlsx') or file.endswith('.xls') and '_p' not in file:
                file_path = os.path.join(visit_folder, file)
                df_dict = pd.read_excel(file_path, sheet_name=None)
                sheets_to_remove = {"Screening Protocol", "Notes"}
                df_dict = {name: df for name, df in df_dict.items() if name not in sheets_to_remove}

                for sheet_name, df in df_dict.items():
                    df.replace({0: np.nan, None: np.nan, pd.NA: np.nan}, inplace=True)

                    df_results = compute_percentage_variations(df)

                    sheet_name_clean = clean_filename(sheet_name)
                    folder_out = output_folder + '_' + f"{sheet_name_clean}"
                    if not os.path.exists(folder_out):
                        os.makedirs(folder_out)

                    original_path = os.path.join(folder_out,
                        f"{filename_no_ext}_{sheet_name_clean}_{original}.xlsx")
                    df.to_excel(original_path, index=False)

                    variation_path = os.path.join(folder_out,
                        f"{filename_no_ext}_{sheet_name_clean}_{percentage_variation}.xlsx")
                    df_results.to_excel(variation_path, index=False)

                    print(f"Saved: {variation_path}")


if __name__ == "__main__":
    run()
