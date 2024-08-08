import csv
from math import floor
from jarowinkler import jarowinkler_similarity




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
def JW_score(s1_in, s2_in):
    s1 = s1_in#.upper()
    s2 = s2_in#.upper()
    jaro_dist = jaro_distance(s1, s2)
	# If the jaro Similarity is above a threshold 
    if (jaro_dist > 0.7) :
		# Find the length of common prefix 
        prefix = 0; 
        for i in range(min(len(s1), len(s2))):
			# If the characters match 
            if (s1[i] == s2[i]):
                prefix += 1
			# Else break 
            else:
                break 
		# Maximum of 4 characters are allowed in prefix 
            prefix = min(4, prefix); 
		# Calculate jaro winkler Similarity 
        jaro_dist += 0.1 * prefix * (1 - jaro_dist); # 0.1
    return jaro_dist

    #Prototyping
def jaro_distance2(s1, s2):
    # If the strings are equal 
    if s1 == s2:
        return 1.0
    # Length of two strings 
    len1 = len(s1)
    len2 = len(s2)
    if len1 == 0 or len2 == 0:
        return 0.0
    # Maximum distance upto which matching is allowed 
    max_dist = (max(len1, len2) // 2) - 1
    # Count of matches 
    match = 0
    # Hash for matches 
    hash_s1 = [0] * len1
    hash_s2 = [0] * len2
    # Traverse through the first string 
    for i in range(len1):
        # Check if there is any match
        for j in range(max(0, i - max_dist), min(len2, i + max_dist + 1)):
            # If there is a match
            if s1[i] == s2[j] and hash_s2[j] == 0:
                hash_s1[i] = 1
                hash_s2[j] = 1
                match += 1
                break
    # If there is no match
    if match == 0:
        return 0.0
    # Number of transpositions
    t = 0
    point = 0
    # Count number of transpositions
    for i in range(len1):
        if hash_s1[i]:
            while hash_s2[point] == 0:
                point += 1
            if s1[i] != s2[point]:
                t += 1
            point += 1
    t /= 2
    # Return the Jaro Similarity
    return (match / len1 + match / len2 + (match - t) / match) / 3.0

def JW_score2(s1_in, s2_in, variable1=0.1, variable2=4, variable3=0.7):
    s1 = s1_in.upper()
    s2 = s2_in.upper()
    jaro_dist = jaro_distance(s1, s2)
    # If the jaro Similarity is above a threshold 
    if jaro_dist > variable3:
        # Find the length of common prefix 
        prefix = 0
        for i in range(min(len(s1), len(s2))):
            # If the characters match
            if s1[i] == s2[i]:
                prefix += 1
            # Else break
            else:
                break
        # Maximum of 4 characters are allowed in prefix 
        prefix = min(variable2, prefix)
        # Calculate jaro winkler Similarity 
        jaro_dist += variable1 * prefix * (1 - jaro_dist)
    return jaro_dist
    

def read_csv(file_path):
    """
    Reads a CSV file into a list of dictionaries for data management.
    :param file_path: str, path to the CSV file
    :return: list of dictionaries
    """
    data = []

    with open(file_path, mode='r', encoding='utf-8-sig') as file:
        # Create a CSV reader object
        csv_reader = csv.DictReader(file)
        # Iterate over each row and append it to the data list
        for row in csv_reader:
            data.append(row)
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
		for row in csv_reader:
			# compile the row: key : [null, weighting]
			data[row['Name']] = [row['null_score'], row['weighting_score']]
		file.close()
	return data

def one_null_check(s1,s2):
    # Checks whether one or two are null and returns true
    if (len(s1) < 1 or len(s2) < 1):
        # one or more is null
        return True
    else:
        return False

def check_string_types(s1, s2):
    def get_type(s):
        if s.isnumeric():
            return 1
        elif s.isalnum():
            return -1
        else:
            return 0
    return get_type(s1) + get_type(s2)

def check_types_score(key, s1,s2, score):
    # checks type dependent
    value = check_string_types(s1,s2)
    if (key=='DSE__DS_Custom_Field_1__c' or key=='DSE__DS_Custom_Field_2__c'):
        if (value == 2):
            return exact_match(s1,s2)
        elif (value == -2):
            return score
    elif (key=='DSE__DS_Custom_Field_5__c' or key=='DSE__DS_Custom_Field_6__c' or key=='DSE__DS_Domain__c'):
        # exact match
        return exact_match(s1,s2)        
    return score

def calculate_score(weighting, null_score, s1, s2, score, key):
    # return the score given the logical criteria
    # modify the values based on data type
    # change the score comparison from fuzzy to exact if
    #print(f'type={type(weighting)} and value = {weighting}')
    if weighting != 2.0:
        # Check for null values
        # if one or both null then return null score
        if (one_null_check(s1,s2)):
            return null_score
        else:
            # else return fuzzy match or exact match if the data types match
            score = check_types_score(key, s1,s2, score)
            return score
    else:
        if null_score == 0:
            if s1 is not None and s2 is not None:
                return 0 if s1 == s2 else -1
            return -1
        if 1 <= null_score <= 100:
            if s1 is not None and s2 is not None:
                return 0 if s1 == s2 else -1
            return 0  # This covers both cases: only one populated or both null
    raise Exception("invalid input. Null Score above 100")

def weighted_ratio(config_dict: dict, scores: list, score_exp: float):
    # Scores is a dictionary
    sum = 0
    for key, value in scores.items():
        if (value < 0):
            return 0 # invalid matching by 200 weighting field
        #print(f'Key - {key} - Value - {value}')
        #print(config_dict[key][1])
        sum += float(config_dict[key][1]) * value
        print(f'Weighting score for {key} : {float(config_dict[key][1]) * value}')
    print(f'Expected value: {score_exp} - actual: {sum}')
    return sum

def DUNS_score(path_to_data):
    config_dict = load_config("config.csv") # stores all of the config data to be used in weighting and nulls
    # Modifies the data dicitonary to include a score column and adds the scores there
    # For pair of fields -> load the csv
    master_prefix = "DSE__DS_Master__r."
    dup_prefix = "DSE__DS_Duplicate__r."
    data = read_csv(path_to_data) # array of dictionaries
    ## data_out = []
    for i in range(0,len(data),1): # Each row in data
        #print("a")
        out_dict = {}
        for key in config_dict.keys(): # Each field
            # Fetch master field
            master_field = data[i][master_prefix + key]
            # Fetch duplicate field
            dup_field = data[i][dup_prefix + key] 
            # calculate the score
            weighting = float(config_dict[key][1]) / 100
            null_score = float(config_dict[key][0]) / 100 # converting from csv string into int
            score = jarowinkler_similarity(master_field.upper(), dup_field.upper())
            score = calculate_score(weighting,null_score,master_field,dup_field,score, key)
            out_dict[key] = score
            #print(f'Key: {key} -Fields: Master - {master_field} - Dup - {dup_field} - score: {score}')
        # sum all of the scores as a weighted ratio
        #print(" ")
        data[i]['score'] = int(weighted_ratio(config_dict, out_dict,float(data[i]['DSE__DS_Score__c'])))
        # loop over each pair
        # reassign out dict
        ## data_out.append(out_dict)
    return data

def main():
    # import the CSV
    # import the config weights and null values
        # This is a csv containing all of the editable variables
    # calculate the score for a duplicate pair
    # write the score into a file along with the values from the duplicates
    data = DUNS_score('Test_Example.csv')
    print(len(data))
    write_csv('Out_data.csv', data)#

    # check the validity of the checks
    correct = 0
    incorrect = 0
    total = 0
    incorrect_data = []
    for row in data:
        total += 1
        if len(row['DSE__DS_Score__c']) > 1:
            temp = float(row['DSE__DS_Score__c'])
            temp = int(temp)
            if (int(row['score']) == temp):
                correct += 1
            else:
                incorrect += 1
                incorrect_data.append(row)
    print(f'The totals are: correct={int(correct/total * 100)}% and incorrect={int(incorrect/total * 100)}%'.format())
 #   
 #   if (incorrect != 0):
 #       print("There are some records which got marked as wrong")
 #       print("Writing to csv ... ")
 #      write_csv('Wrong_Data.csv', incorrect_data)
#   data = DUNS_score('Wrong_Data.csv')
#
#   for row in data:
#       total += 1
#       if len(row['DSE__DS_Score__c']) > 1:
#           temp = float(row['DSE__DS_Score__c'])
#           temp = int(temp)
#           if (int(row['score']) == temp):
#               correct += 1
#           else:
#               incorrect += 1
#               incorrect_data.append(row)
#   print(f'The totals are: correct={int(correct/total * 100)}% and incorrect={int(incorrect/total * 100)}%'.format())
#   # runs the second check on single incorrect record
    
  #  s1 = 'Dr. Boehringer-Gasse 5-11'
  #  s2 = 'Belghofergasse 15'
  #  print(JW_score2(s1,s2, 0.1, 2, 0.7))
#
  #  print(jarowinkler_similarity(s1,s2))
    
    s1 = '320 S Tryon St Ste 213'
    s2 = '320 S. TRYON STREET, SUITE 213'
    
    print(len(s1))
    print(len(s2))
    print(jarowinkler_similarity(s1,s2,score_cutoff=0.9))
    print(0.9*JW_score(s1,s2))
    print(JW_score2(s1,s2, 1000,4,1)) # TODO : check what those variables are
    
main()