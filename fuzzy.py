import re
from jellyfish import soundex
from jarowinkler import jarowinkler_similarity
from itertools import product

def normalize_string(s):
    """Normalize the string by lowercasing, removing punctuation and splitting into tokens."""
    s = s.lower()
    s = re.sub(r'[^\w\s]', '', s)  # Remove punctuation
    tokens = s.split()
    return tokens

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
    adjusted_score = int(similarity_score * 100)  # Adjust to scale similar to 31/100
    
    return adjusted_score

