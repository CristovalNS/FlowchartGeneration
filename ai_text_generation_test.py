from transformers import pipeline, set_seed

# This sucks don't use this
generator = pipeline('text-generation', model='EleutherAI/gpt-neo-1.3B')
set_seed(42)

prompt = """
I like bananas
"""

description = generator(prompt, max_length=150, num_return_sequences=1, temperature=0.7, top_p=0.9, truncation=True)
print(description[0]['generated_text'])
