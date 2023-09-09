import pickle
import spacy

# Load a spaCy language model to tokenize the text into words
nlp = spacy.load("en_core_web_sm")

def split_text_into_chunks(text, token_limit):
    # Tokenize the text into words using spaCy
    doc = nlp(text)

    text_chunks = []
    current_chunk = ""

    for token in doc:
        # Check if adding the token to the current chunk exceeds the token limit
        if len(current_chunk) + len(token.text) + 1 <= token_limit:
            current_chunk += token.text + " "
        else:
            # Append the current chunk to the list of chunks
            text_chunks.append(current_chunk.strip())
            current_chunk = token.text + " "

    # Append the last chunk
    text_chunks.append(current_chunk.strip())

    return text_chunks

def main(input_txt_path, token_limit, output_pkl_path):
    # Read the text content from the input file
    with open(input_txt_path, 'r', encoding='utf-8') as file:
        text = file.read()

    # Split the text into chunks
    text_chunks = split_text_into_chunks(text, token_limit)

    # Save the chunks as a pickle file
    with open(output_pkl_path, 'wb') as pkl_file:
        pickle.dump(text_chunks, pkl_file)

    # Return the text_chunks list
    return text_chunks

if __name__ == "__main__":
    input_txt_path = 'test.txt'      # Replace with the path to your input text file
    token_limit = 1000               # Specify the desired token limit per chunk
    output_pkl_path = 'output_chunks.pkl'  # Specify the path for the output pickle file

    text_chunks = main(input_txt_path, token_limit, output_pkl_path)  # Capture the returned value
    
    print(f'Split text content into {len(text_chunks)} chunks and saved as {output_pkl_path}')
