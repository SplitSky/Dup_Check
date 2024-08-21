import re
from jellyfish import soundex
from jarowinkler import jarowinkler_similarity
from itertools import product
import json
import csv

def normalize_string(s):
    """Normalize the string by lowercasing, removing punctuation and splitting into tokens."""
    s = s.lower()
    s = re.sub(r'[^\w\s]', '', s)  # Remove punctuation
    tokens = s.split()
    return tokens

def json_to_csv(json_file, csv_file):
    # Open the JSON file and load the data
    with open(json_file, 'r') as f:
        data = json.load(f)

    # Open the CSV file for writing
    with open(csv_file, 'w', newline='') as f:
        # Create a CSV writer object
        writer = csv.writer(f)

        # If the JSON data is a list of dictionaries, write the header and data rows
        if isinstance(data, list) and all(isinstance(item, dict) for item in data):
            # Extract the header from the keys of the first dictionary
            header = data[0].keys()
            writer.writerow(header)

            # Write each dictionary as a row in the CSV file
            for row in data:
                writer.writerow(row.values())
        else:
            raise ValueError("JSON data must be a list of dictionaries")

    print(f"Data successfully written to {csv_file}")


def phonetic_representation(tokens):
    """Convert tokens to their phonetic representation using Soundex."""
    return [soundex(token) for token in tokens]

def match_tokens(tokens1, tokens2):
    """Compute the best Jaro-Winkler similarity using a greedy matching strategy."""
    best_score = 0
    used_indices = set()
    
    for token1 in tokens1:
        best_local_score = 0
        best_local_index = -1
        for i, token2 in enumerate(tokens2):
            if i in used_indices:
                continue
            score = jarowinkler_similarity(token1, token2)
            if score > best_local_score:
                best_local_score = score
                best_local_index = i
        
        if best_local_index != -1:
            used_indices.add(best_local_index)
        best_score += best_local_score
    
    return best_score / max(len(tokens1), len(tokens2))

def custom_fuzzy_match(s1, s2):
    if len(s1) == 0 or len(s2) == 0:
        return 0
    if s1 == s2:
        return 1
    
    # Step 1: Normalize the strings
    tokens1 = normalize_string(s1)
    tokens2 = normalize_string(s2)
    
    # Step 2: Convert tokens to phonetic representation
    phonetic_tokens1 = phonetic_representation(tokens1)
    phonetic_tokens2 = phonetic_representation(tokens2)
    
    # Step 3: Match tokens using Jaro-Winkler on phonetic tokens
    similarity_score = match_tokens(phonetic_tokens1, phonetic_tokens2)
    
    # Step 4: Custom scoring adjustment (mimicking the low score behavior)
    adjusted_score = int(similarity_score)  # Adjust to scale similar to 31/100
    
    return adjusted_score

