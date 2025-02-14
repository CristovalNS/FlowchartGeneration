import json
import time
from transformers import AutoModelForCausalLM, AutoTokenizer

# Load the Mermaid JSON file
input_json_path = 'linear_flowchart_mermaid_json/v_linear_combined_mermaid_data.json'
output_json_path = 'linear_flowchart_mermaid_json/v_linear_flowchart_descriptions.json'

# Load the Mermaid flowchart data
with open(input_json_path, 'r') as file:
    mermaid_data = json.load(file)

# Load the model and tokenizer
model_name = "Qwen/Qwen2.5-3B"
tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    torch_dtype="auto",
    device_map="auto",
    trust_remote_code=True
)

# Dictionary to store the descriptions
descriptions = {}

# Generate descriptions for each Mermaid flowchart
for idx, (filename, mermaid_text) in enumerate(mermaid_data.items(), start=1):
    start_time = time.time()
    
    print(f"Processing {idx}/{len(mermaid_data)}: {filename}")
    
    prompt = f"Describe the following flowchart in natural language:\n\n{mermaid_text}\n\nNatural Language Description:"
    inputs = tokenizer(prompt, return_tensors="pt")

    # Generate output
    outputs = model.generate(**inputs, max_length=200)
    description = tokenizer.decode(outputs[0], skip_special_tokens=True)

    # Store the description in the dictionary
    descriptions[filename] = description
    
    elapsed_time = time.time() - start_time
    print(f"Completed: {filename} in {elapsed_time:.2f} seconds")

    # Save intermediate results after each file
    with open(output_json_path, 'w') as file:
        json.dump(descriptions, file, indent=4)
    print(f"Intermediate save completed after {filename}.")

print(f'All natural language descriptions saved to: {output_json_path}')
