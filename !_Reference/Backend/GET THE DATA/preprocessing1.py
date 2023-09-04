import re
import tokenize
from io import BytesIO
import os
import random

# Function to tokenize code using Python's built-in tokenizer
def tokenize_code(input_code):
    tokens = []
    try:
        code_bytes = input_code.encode('utf-8')
        code_stream = BytesIO(code_bytes)
        tokenizer = tokenize.tokenize(code_stream.readline)
        for tok in tokenizer:
            tokens.append(tokenize.tok_name[tok.type])
    except Exception as e:
        print(f"Tokenization error: {str(e)}")
    return tokens

# Function to clean and preprocess code (modify as needed)
def clean_and_preprocess_code(input_code):
    # Example: Remove comments
    cleaned_code = re.sub(r'#.*', '', input_code)
    return cleaned_code

# Function to split code into input and target sequences
def split_code_into_sequences(code_tokens, sequence_length):
    sequences = []
    for i in range(0, len(code_tokens) - sequence_length - 1, sequence_length):
        input_sequence = code_tokens[i:i + sequence_length]
        target_sequence = code_tokens[i + sequence_length:i + sequence_length + 1]
        sequences.append((input_sequence, target_sequence))
    return sequences

# Read code from the text file
with open('github_repo_content.txt', 'r', encoding='utf-8') as input_file:
    code = input_file.read()

# Clean and preprocess the code
cleaned_code = clean_and_preprocess_code(code)

# Tokenize the cleaned code
tokens = tokenize_code(cleaned_code)

# Define sequence length for input and target sequences
sequence_length = 5  # Adjust this based on your use case

# Split code into input and target sequences
sequences = split_code_into_sequences(tokens, sequence_length)

# Shuffle the sequences for better training
random.shuffle(sequences)

# Define the output file path
output_file_path = 'prepared_code.txt'

# Save the prepared code sequences to the output file
with open(output_file_path, 'w', encoding='utf-8') as output_file:
    for input_seq, target_seq in sequences:
        input_line = ' '.join(input_seq)
        target_line = ' '.join(target_seq)
        output_file.write(f"{input_line}\t{target_line}\n")

print("Data preparation complete. Prepared code saved to", output_file_path)
