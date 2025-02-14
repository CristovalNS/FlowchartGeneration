import os
import json

# Directory containing the Mermaid .txt files
directory = '/Users/cristovalneosasono/Internship-Code/Mermaid_Generation_Test/linear_flowcharts/V_linear_system_flowchart_test_files/mermaid_txt'

# Dictionary to store file contents
mermaid_data = {}

# Iterate over all .txt files in the directory
for filename in os.listdir(directory):
    if filename.endswith('.txt'):
        file_path = os.path.join(directory, filename)
        with open(file_path, 'r') as file:
            content = file.read()
            mermaid_data[filename] = content

# Output JSON file path
output_file = os.path.join('linear_flowchart_mermaid_json', 'v_linear_combined_mermaid_data.json')

# Write the combined data to a JSON file
with open(output_file, 'w') as json_file:
    json.dump(mermaid_data, json_file, indent=4)

print(f'Combined JSON file saved as: {output_file}')
