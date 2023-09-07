import re
import tokenize  # Python's built-in tokenizer
from io import BytesIO

# Function to tokenize code using Python's built-in tokenizer
def tokenize_code(input_code):
    tokens = []
    try:
        code_bytes = input_code.encode('utf-8')
        code_stream = BytesIO(code_bytes)
        tokenizer = tokenize.tokenize(code_stream.readline)
        for tok in tokenizer:
            if tok.type == tokenize.NAME:
                tokens.append("IDENTIFIER")
            elif tok.type == tokenize.NUMBER:
                tokens.append("NUMBER")
            else:
                tokens.append(tokenize.tok_name[tok.type])
    except Exception as e:
        print(f"Tokenization error: {str(e)}")
    return tokens

# Function to clean and preprocess code
def clean_and_preprocess_code(input_code):
    # Perform your cleaning and preprocessing steps here
    # Example: Remove comments
    cleaned_code = re.sub(r'#.*', '', input_code)
    
    # Example: Normalize variable names
    cleaned_code = re.sub(r'\b[a-zA-Z_][a-zA-Z0-9_]*\b', 'IDENTIFIER', cleaned_code)
    
    return cleaned_code

# Input and output file paths
input_file_path = 'github_repo_content.txt'
output_file_path = 'cleaned_and_tokenized_code.txt'

try:
    # Read code from the input file
    with open(input_file_path, 'r', encoding='utf-8') as input_file:
        code = input_file.read()

    # Clean and preprocess the code
    cleaned_code = clean_and_preprocess_code(code)

    # Tokenize the cleaned code
    tokens = tokenize_code(cleaned_code)

    # Save the cleaned and tokenized code to the output file
    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        output_file.write('\n'.join(tokens))

    print("Cleaning and tokenization complete. Output saved to", output_file_path)
except FileNotFoundError:
    print("Input file not found.")
except Exception as e:
    print("An error occurred:", str(e))
