import csv
import re

def fix_csv_line_breaks(input_file, output_file):
    # Open the input file and read the contents
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Replace line breaks that occur within quotes with a space
    fixed_content = re.sub(r'"\n', '" ', content)
    fixed_content = re.sub(r'\n"', ' "', fixed_content)

    # Write the fixed content to the output file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(fixed_content)

    print(f"Line breaks inside CSV fields have been fixed and saved to {output_file}.")

# Example usage:
input_file = 'Test_Example.csv'
output_file = 'Test_Example2.csv'
fix_csv_line_breaks(input_file, output_file)