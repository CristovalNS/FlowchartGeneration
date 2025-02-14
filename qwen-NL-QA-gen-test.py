from transformers import AutoModelForCausalLM, AutoTokenizer

# This one seems to work well

model_name = "Qwen/Qwen2.5-3B"

tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)

model = AutoModelForCausalLM.from_pretrained(
    model_name,
    torch_dtype="auto",  
    device_map="auto",  
    trust_remote_code=True
)

# Example prompt
mermaid_text = """
[[[
flowchart TD
    0(Start)
    1[/IO 2/]
    0 --> 1
    2{Decision 2}
    1 --> 2
    3[Process 2]
    2 -- Yes --> 3
    4[/IO 3/]
    2 -- No --> 4
    5[Process 3]
    3 --> 5
    6(End)
    4 --> 6
    5 --> 6
]]]
"""
prompt = (
    "You are provided with a Mermaid flowchart description enclosed in [[[]]]. Your task is to describe the flowchart in natural language, ensuring every node and connection is explained in detail. Each node type must be explicitly identified as follows:"
    "Process nodes are denoted by [Process X], where X is a number."
    "Input/Output (IO) nodes are denoted by [/IO X/], where X is a number."
    "Decision nodes are enclosed in {} and represent branching logic (e.g., Yes/No decisions)."
    "Termination nodes are represented by (Start) or (End)."
    "Describe the flowchart step-by-step in a single, coherent paragraph. Do not skip any steps, and ensure the logical flow between nodes is clearly explained."
    "Here is the flowchart in Mermaid syntax:"
    f"{mermaid_text}\n\n"
    "Natural Language Description:"
)
inputs = tokenizer(prompt, return_tensors="pt")

# Generate output
outputs = model.generate(**inputs, max_length=200)
description = tokenizer.decode(outputs[0], skip_special_tokens=True)
print(description)