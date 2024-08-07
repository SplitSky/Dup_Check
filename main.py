import csv
from math import floor

'''
Requirements:
1. Must be able to calculate the duplicate score for Duplicate Account entity
2. Must work from a CSV duplicate account records that have no score. This will include all matching
fields from the Master Beans
3. Must be able to handle Null scoring
4. Must be able to handle weighting logic
5. must be able to handle fuzzy logic (field dependent) - Calculate JW distance Jaro-Winkler similarity
6. Must be able to utilise weighting and null score input parameters
'''

# Function to calculate the 
# Jaro Similarity of two strings 
def jaro_distance(s1, s2) :
	# If the strings are equal 
	if (s1 == s2) :
		return 1.0; 
	# Length of two strings 
	len1 = len(s1);
	len2 = len(s2); 
	if (len1 == 0 or len2 == 0) :
		return 0.0;
	# Maximum distance upto which matching 
	# is allowed 
	max_dist = (max(len(s1), len(s2)) // 2 ) - 1; 
	# Count of matches 
	match = 0; 
	# Hash for matches 
	hash_s1 = [0] * len(s1) ;
	hash_s2 = [0] * len(s2) ; 
	# Traverse through the first string 
	for i in range(len1) : 
		# Check if there is any matches 
		for j in range( max(0, i - max_dist), 
					min(len2, i + max_dist + 1)) : 
			# If there is a match 
			if (s1[i] == s2[j] and hash_s2[j] == 0) : 
				hash_s1[i] = 1; 
				hash_s2[j] = 1; 
				match += 1; 
				break; 
	# If there is no match 
	if (match == 0) :
		return 0.0; 
	# Number of transpositions 
	t = 0; 
	point = 0; 
	# Count number of occurrences 
	# where two characters match but 
	# there is a third matched character 
	# in between the indices 
	for i in range(len1) : 
		if (hash_s1[i]) :

			# Find the next matched character 
			# in second string 
			while (hash_s2[point] == 0) :
				point += 1; 

			if (s1[i] != s2[point]) :
				point += 1;
				t += 1;
			else :
				point += 1;
				
		t /= 2; 
	# Return the Jaro Similarity 
	return ((match / len1 + match / len2 +
			(match - t) / match ) / 3.0); 
# Jaro Winkler Similarity 
def JW_score(s1, s2) : 

	jaro_dist = jaro_distance(s1, s2); 

	# If the jaro Similarity is above a threshold 
	if (jaro_dist > 0.7) :

		# Find the length of common prefix 
		prefix = 0; 

		for i in range(min(len(s1), len(s2))) :
		
			# If the characters match 
			if (s1[i] == s2[i]) :
				prefix += 1; 

			# Else break 
			else :
				break; 

		# Maximum of 4 characters are allowed in prefix 
		prefix = min(4, prefix); 

		# Calculate jaro winkler Similarity 
		jaro_dist += 0.1 * prefix * (1 - jaro_dist); 
	return jaro_dist; 

def read_csv(file_path):
    """
    Reads a CSV file into a list of dictionaries for data management.
    :param file_path: str, path to the CSV file
    :return: list of dictionaries
    """
    full_data = []

    
    with open(file_path, mode='r', encoding='utf-8-sig') as file:
        # Create a CSV reader object
        csv_reader = csv.DictReader(file)
        # Iterate over each row and append it to the data list
        for row in csv_reader:
            full_data.append(row)
            # the individual row of data
    return data

def exact_match(s1, s2):
    if s1 == s2:
        return 1
    else:
        return 0

def write_csv(file_path, data):
    if not data:
        raise ValueError("Data is empty")

    # Extract the header from the keys of the first dictionary
    headers = data[0].keys()

    with open(file_path, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=headers)

        # Write the header
        writer.writeheader()

        # Write the data rows
        for row in data:
            writer.writerow(row)
        file.close()
            
def load_config(config_path):
	# Loads the config csv and uses it for data calculations
	# Use the keys for the list of fields that are available in the CSV
	data = {}
	with open(config_path, mode='r', encoding='utf-8-sig') as file:
		# Create a CSV reader object
		csv_reader = csv.DictReader(file)
		# Iterate over each row and append it to the data list
		first = True
		for row in csv_reader:
			if first:
				first = False
			else:
				# compile the row: key : [null, weighting]
				data[row['Name']] = [row['null_score'], row['weighting_score']]
		print(data)
		file.close()
	return data


def calculate_score(weighting, null_score, s1, s2, score):
    # return the score given the logical criteria
    if weighting != 200:
        return score
    # not 200 return
    
    if null_score == 0:
        if value1 is not None and value2 is not None:
            return exact_match(s1,s2) if value1 == value2 else 0
        return 0
    
    if 1 <= null_score <= 100:
        if value1 is not None and value2 is not None:
            return exact_match(s1,s2) if value1 == value2 else 0
        return exact_match(s1,s2)  # This covers both cases: only one populated or both null

    raise Exception("invalid input")

def weighted_ratio(config_dict, scores):
    sum = 0
    for key, value in scores:
        sum += config_dict[key][1] * value
    return sum

def DUNS_score(path_to_data):
    config_dict = load_config("config.csv") # stores all of the config data to be used in weighting and nulls
    # Modifies the data dicitonary to include a score column and adds the scores there
    # For pair of fields -> load the csv
    master_prefix = "DSE__DS_Master__r."
    dup_prefix = "DSE__DS_Duplicate__r."
    data = read_csv(path_to_data) # array of dictionaries
    out_dict = {}
    for i in range(0,len(data),1): # Each row in data
        print("a") 
        for key in config_dict.keys(): # Each field
            # Fetch master field
            master_field = data[i][master_prefix + key]
            # Fetch duplicate field
            dup_field = data[i][dup_prefix + key] 
            # calculate the score
            print(f'Key: {key} -Fields: Master - {master_field} - Dup - {dup_field}')
            # calc score
            weighting = config_dict[key][1] 
            null_score = config_dict[key][0]
            score = JW_score(master_field, dup_field)
            score = calculate_score(weighting,null_score,master_field,dup_field,score)
            out_dict[key] = score

        # sum all of the scores as a weighted ratio
        data[i]['score'] = weighted_ratio(config_dict, scores)
        # loop over each pair
    return out_dict
# define main
def main():
    # import the CSV
    ######read_csv("Test_Example.csv")
    # import the config weights and null values
        # This is a csv containing all of the editable variables
    # calculate the score for a duplicate pair
    # write the score into a file along with the values from the duplicates
    print(DUNS_score('Test_Example.csv'))

main()
