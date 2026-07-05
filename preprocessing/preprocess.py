import re
import spacy

# Load spaCy English model
nlp = spacy.load("en_core_web_sm")

def preprocess_text(text):
    """
    Clean and preprocess resume text.
    """

    # Convert to lowercase
    text = text.lower()

    # Remove URLs
    text = re.sub(r"http\S+|www\S+", "", text)

    # Remove email addresses
    text = re.sub(r"\S+@\S+", "", text)

    # Remove phone numbers
    text = re.sub(r"\d{10,}", "", text)

    # Remove special characters
    text = re.sub(r"[^a-zA-Z\s]", " ", text)

    # Remove extra spaces
    text = re.sub(r"\s+", " ", text).strip()

    # NLP processing
    doc = nlp(text)

    cleaned_words = []

    for token in doc:
        if not token.is_stop and not token.is_punct:
            cleaned_words.append(token.lemma_)

    return " ".join(cleaned_words)