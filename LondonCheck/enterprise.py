import pandas as pd
import matplotlib.pyplot as plt

# Step 1: Read the Excel file
file_path = 'EnterpriseAccount.xlsx'
df = pd.read_excel(file_path)

# Step 2: Perform the analysis
# a) Find groups with more than 10 accounts
group_counts = df['DSE__DS_Master__r.Name'].value_counts()
large_groups = group_counts[group_counts >= 5]

# b) Get rows that are part of the large groups
large_group_names = large_groups.index  # Get the names of large groups
large_group_entries = df[df['DSE__DS_Master__r.Name'].isin(
    large_group_names)]  # Filter rows in large groups

# Save the filtered rows into a CSV file
large_group_entries.to_csv('large_group_entries.csv', index=False)

# c) Plot a histogram of groups
plt.hist(group_counts, bins=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 15, 20])
plt.title('Distribution of Accounts in Groups')
plt.xlabel('Number of Accounts in a Group')
plt.ylabel('Frequency')
# plt.show()

# Step 3: Export the large groups summary to Excel
large_groups_df = pd.DataFrame(large_groups)
large_groups_df.to_excel('large_groups_summary.xlsx', index=False)
