import csv
from textwrap import wrap
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
# import fuzzy as fz


def read_excel(file_path):
    df = pd.read_excel(file_path, dtype=str)
    df = df.fillna('')
    # print(f'dataframe size{df.head(20)} \n')
    return df.to_dict(orient='records')


# def write_csv(file_path, data):
#     if not data:
#         raise ValueError("Data is empty")
#     headers = data[0].keys()
#     with open(file_path, mode='w', newline='') as file:
#         writer = csv.DictWriter(file, fieldnames=headers)
#         writer.writeheader()
#         for row in data:
#             writer.writerow(row)


def get_counts(data):
    results = []
    master_dict = {}

    for row in data:
        master_duns = row.get(
            'DSE__DS_Master__r.DSE__DS_Account__r.kfx_DUNSNumber__c')
        dup_duns = row.get(
            'DSE__DS_Duplicate__r.DSE__DS_Account__r.kfx_DUNSNumber__c')
        master_id = row.get('DSE__DS_Master__r.DSE__DS_Account__c')
        dup_id = row.get('DSE__DS_Duplicate__r.DSE__DS_Account__c')

        if master_duns not in master_dict:
            master_dict[master_duns] = {
                "Master_name": master_id,
                "Master_DUNS": master_duns,
                "Dup_list": [],
                "count": 0
            }

        master_dict[master_duns]["Dup_list"].append(
            {"Dup_Id": dup_id, "Dup_DUNS": dup_duns})
        master_dict[master_duns]["count"] += 1

    results.extend(master_dict.values())
    return results


def write_csv(file_path, data):
    # Check if data is a list and is not empty
    if not data or not isinstance(data, list):
        raise ValueError("Data must be a non-empty list")

    # Check if the first element is a dictionary to extract headers
    if not isinstance(data[0], dict):
        raise ValueError("Data must be a list of dictionaries")

    headers = set()
    for row in data:
        headers.update(row.keys())  # Collect all possible headers

    headers = sorted(headers)  # Sort headers for consistent order

    try:
        with open(file_path, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=headers)
            writer.writeheader()
            for row in data:
                # Write each row, ensuring missing keys have empty string values
                writer.writerow({key: row.get(key, '') for key in headers})
        print(f"Data successfully written to {file_path}")
    except Exception as e:
        print(f"An error occurred while writing to CSV: {e}")

# Example usage:
# data = [{'col1': 'value1', 'col2': 'value2'}, {'col1': 'value3', 'col2': 'value4'}]
# write_csv('output.csv', data)

# analyze_duplicates(counts)


def main():
    data = read_excel("data.xlsx")
    a = get_counts(data)
    for data in a:
        print(data)

    write_csv("data.csv", data)


main()
