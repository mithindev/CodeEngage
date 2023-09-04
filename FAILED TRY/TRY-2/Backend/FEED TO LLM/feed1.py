from transformers import AutoTokenizer, AutoModelForCausalLM

# Specify the backend explicitly (in this case, TensorFlow)
tokenizer = AutoTokenizer.from_pretrained("gpt2", backend="tf")
model = AutoModelForCausalLM.from_pretrained("gpt2", backend="tf")


# Read your data from the TXT file
with open('test.txt', 'r', encoding='utf-8') as file:
    code_data = file.read()

# Split the text into chunks of 1,000 tokens
chunk_size = 1000
text_chunks = [code_data[i:i + chunk_size] for i in range(0, len(code_data), chunk_size)]

# Initialize an empty string to store the generated responses
generated_responses = ""

# Loop through text chunks and interact with the model
for chunk in text_chunks:
    input_text = "Code: " + chunk + " Question: "
    input_ids = tokenizer.encode(input_text, return_tensors="pt")

    # Generate a response
    num_tokens_to_generate = 50  # Adjust as needed
    outputs = model.generate(input_ids, max_length=num_tokens_to_generate, num_return_sequences=1)
    generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)

    # Append the generated response to the result
    generated_responses += generated_text + "\n"

# Print or use the generated responses
print(generated_responses)
