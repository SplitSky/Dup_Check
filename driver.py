import csv
from math import floor
from jarowinkler import jarowinkler_similarity
import re
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import fuzzy as fz

differences = []
exp_differences = []
exp_scores = []

# Function to calculate the Jaro Similarity of two strings
def jaro_distance(s1, s2):
    if s1 == s2:
        return 1.0

    len1, len2 = len(s1), len(s2)
    if len1 == 0 or len2 == 0:
        return 0.0

    max_dist = (max(len1, len2) // 2) - 1
    match = 0
    hash_s1 = [0] * len1
    hash_s2 = [0] * len2

    for i in range(len1):
        for j in range(max(0, i - max_dist), min(len2, i + max_dist + 1)):
            if s1[i] == s2[j] and hash_s2[j] == 0:
                hash_s1[i] = 1
                hash_s2[j] = 1
                match += 1
                break

    if match == 0:
        return 0.0

    t = 0
    point = 0
    for i in range(len1):
        if hash_s1[i]:
            while hash_s2[point] == 0:
                point += 1
            if s1[i] != s2[point]:
                t += 1
            point += 1

    t /= 2
    return (match / len1 + match / len2 + (match - t) / match) / 3.0

# Jaro-Winkler Similarity
def JW_score(s1_in, s2_in):
    s1 = pre_process_string(s1_in)
    s2 = pre_process_string(s2_in)
    jaro_dist = jaro_distance(s1, s2)

    if jaro_dist > 0.7:
        prefix = 0
        for i in range(min(len(s1), len(s2))):
            if s1[i] == s2[i]:
                prefix += 1
            else:
                break
        prefix = min(4, prefix)
        jaro_dist += 0.1 * prefix * (1 - jaro_dist)
    
    return jaro_dist

def pre_process_string(s_in):
    return str(s_in).upper()

def read_csv(file_path):
    data = []
    with open(file_path, mode='r', encoding='utf-8-sig') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            data.append(row)
    return data

def read_excel(file_path):
    df = pd.read_excel(file_path, dtype=str)
    df = df.fillna('')
    return df.to_dict(orient='records')

def exact_match(s1, s2):
    return 1 if s1 == s2 else 0

def write_csv(file_path, data):
    if not data:
        raise ValueError("Data is empty")
    headers = data[0].keys()
    with open(file_path, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()
        for row in data:
            writer.writerow(row)

def load_config(config_path):
    data = {}
    with open(config_path, mode='r', encoding='utf-8-sig') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            data[row['Name']] = [row['null_score'], row['weighting_score']]
    return data

def one_null_check(s1, s2):
    return len(s1) < 1 or len(s2) < 1

def check_string_types(s1, s2):
    def get_type(s):
        if s.isnumeric():
            return 1
        elif s.isalnum():
            return -1
        else:
            return 0
    return get_type(s1) + get_type(s2)

def check_types_score(key, s1, s2, score):
    value = check_string_types(s1, s2)
    if key in ['DSE__DS_Custom_Field_1__c', 'DSE__DS_Custom_Field_2__c']:
        if value == 2:
            return exact_match(s1, s2)
        elif value == -2:
            return score
    elif key in ['DSE__DS_Custom_Field_5__c', 'DSE__DS_Custom_Field_6__c', 'DSE__DS_Domain__c']:
        return exact_match(s1, s2)
    return score

def calculate_score(weighting, null_score, s1_in, s2_in, score, key):
    s1, s2 = str(s1_in), str(s2_in)
    if weighting != 2.0:
        if one_null_check(s1, s2):
            return null_score
        score = check_types_score(key, s1, s2, score)
        return score
    else:
        if null_score == 0:
            return 0 if s1 == s2 else -1
        if 1 <= null_score <= 100:
            return 0 if s1 == s2 else -1
    raise Exception("Invalid input. Null Score above 100")

def append_to_log(text_to_append):
    with open("Driver_log.txt", 'a') as file:
        file.write(text_to_append + '\n')

def weighted_ratio(config_dict, scores, score_exp, row):
    total_score = 0
    #append_to_log('Adding scores for record: ' + row['Id'])
    for key, value in scores.items():
        if value < 0: # negative values indicate the 200 weighting fields.
            # dictate whether it's allowed but don't count towards the score
            return 0
        master_prefix = "DSE__DS_Master__r." # TODO: change . to _
        dup_prefix = "DSE__DS_Duplicate__r."
        master_field = row[master_prefix + key]
        dup_field = row[dup_prefix + key]
        #append_to_log(f'Key: {key} - Value {value} - master: {master_field} - dup: {dup_field}')
        total_score += float(config_dict[key][1]) * value

    differences.append(total_score)
    if (len(score_exp) != 0):
        exp_differences.append(float(score_exp) - total_score)
        exp_scores.append(float(score_exp))
    else:
        exp_differences.append(total_score)
    
    return total_score

def DUNS_score(path_to_data):
    config_dict = load_config("config.csv")
    master_prefix = "DSE__DS_Master__r."
    dup_prefix = "DSE__DS_Duplicate__r."
    data = read_excel(path_to_data)

    for i in range(len(data)):
        out_dict = {}
        for key in config_dict.keys():
            master_field = data[i][master_prefix + key]
            dup_field = data[i][dup_prefix + key]
            weighting = float(config_dict[key][1]) / 100
            null_score = float(config_dict[key][0]) / 100
            score = JW_score(master_field, dup_field)
            if score != 1.0:
                score *= 0.7
            score = calculate_score(weighting, null_score, master_field, dup_field, score, key)
            out_dict[key] = score

        data[i]['score'] = int(weighted_ratio(config_dict, out_dict, data[i]['DSE__DS_Score__c'], data[i]))

    return data

def plot_histogram(data, bins=1000, title='Histogram', xlabel='Values', ylabel='Frequency', color='blue'):
    plt.figure(figsize=(8, 6))
    plt.hist(data, bins=bins, color=color, edgecolor='black')
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.grid(True)
    plt.show()

def driver():
    data = DUNS_score('DUNS_data.xlsx')
    write_csv('FINAL.csv', data)
    
    correct, incorrect, total = 0, 0, 0
    incorrect_data = []

    for row in data:
        total += 1
        if len(row['DSE__DS_Score__c']) > 1:
            temp = float(row['DSE__DS_Score__c'])
            if float(row['score']) == temp:
                correct += 1
            else:
                incorrect += 1
                incorrect_data.append(row)

    print(f'corr ={correct} and incc = {incorrect}')
    print(f'The totals are: correct={int(correct/total * 100)}% and incorrect={int(incorrect/total * 100)}%')
    
    Score_Matching = [
        int(correct/total * 100),
        int(incorrect/total * 100),
        np.array(differences).mean(),
        np.std(np.array(differences)),
        np.max(np.array(differences))
    ]
    
    stats_data = np.array(differences)
    a = np.array(exp_differences)
    
    print(f'mean = {stats_data.mean()}')
    print(f'max = {stats_data.max()}')
    print(f'min = {stats_data.min()}')
    print(f'std = {np.std(stats_data)}')
    print(f'mean diff = {a.mean()}')
    print(f'max diff = {a.max()}')
    print(f'min diff = {a.min()}')
    print(f'std diff = {np.std(a)}')
    print(f'len= {len(a.tolist())}')
    
    plot_histogram(stats_data)

print(driver())
