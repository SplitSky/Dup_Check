import os
import pandas as pd

# Step 1: Load the large group entries file (assumed to be CSV)
large_group_entries = pd.read_csv('large_group_entries.csv')

# Step 2: Load all author lookup files from the 'data' directory
author_files_dir = 'data'  # Directory where the author lookup files are stored
author_files = []
unloaded_files = []  # List to keep track of files that weren't loaded

# Debug: Check if the directory exists
if not os.path.exists(author_files_dir):
    print(f"Error: Directory {author_files_dir} does not exist.")
else:
    # Loop through all .xlsx files in the 'data' directory
    for filename in os.listdir(author_files_dir):
        if filename.endswith('.xlsx'):  # Look for .xlsx files
            file_path = os.path.join(author_files_dir, filename)
            try:
                # Read the Excel file
                author_df = pd.read_excel(file_path)
                # Debug: Print the file being read
                print(f"Reading file: {file_path}")
                # Add a column with the author name (assumed to be the file name without extension)
                author_df['Author'] = filename.split('.')[0]
                # Append to the list of author dataframes
                author_files.append(author_df)
            except Exception as e:
                # Track files that couldn't be loaded
                unloaded_files.append(filename)
                print(f"Error reading {file_path}: {e}")

# Debug: Check how many author files were loaded
print(f"Number of author files loaded: {len(author_files)}")

# Step 3: Combine all author files into a single dataframe (if any were loaded)
if len(author_files) > 0:
    author_files_combined = pd.concat(author_files)
    # Step 4: Merge large group entries with the combined author lookup dataframe
    merged_data = pd.merge(large_group_entries, author_files_combined,
                           left_on='DSE__DS_Master__r.Name', right_on='DUPLICATE GROUP', how='left')

    # Step 5: Save the merged data to a new CSV file, now including the author info
    merged_data.to_csv('large_group_entries_with_authors.csv', index=False)

    # Print the first few rows to verify
    print(merged_data.head())
else:
    print("No author files were found or loaded.")

# Step 6: Print out any files that weren't successfully loaded
if unloaded_files:
    print("\nThe following files were not loaded successfully:")
    for file in unloaded_files:
        print(file)
else:
    print("\nAll files were loaded successfully.")
