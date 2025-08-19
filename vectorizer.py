import string

# Function to preprocess text
def preprocess_text(text):
    # Convert text to lowercase
    text = text.lower()
    
    # Remove punctuation
    text = text.translate(str.maketrans('', '', string.punctuation))
    
    # You can add more preprocessing steps here, such as:
    # - Removing stop words
    # - Lemmatization or stemming
    # - Removing numbers, etc.
    
    return text
