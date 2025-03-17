import nltk
import spacy
from bertopic import BERTopic
from nltk.tokenize import sent_tokenize
import re

nltk.download("punkt")
nlp = spacy.load("en_core_web_sm")

def preprocess_text(text):
    """Cleans and structures text before passing it to the model."""
    
    # Remove extra spaces, newlines, and unwanted symbols
    text = re.sub(r'\s+', ' ', text).strip()  # Collapse multiple spaces
    text = re.sub(r'\*\*', '', text)  # Remove markdown bold markers (**text**)
    text = re.sub(r'---+', ' ', text)  # Remove dividers (---)
    text = re.sub(r'[-#]{2,}', ' ', text)  # Remove dividers (---, ###, ####, etc.)
    
    # Optional: Fix sentence spacing (ensure periods are properly spaced)
    text = re.sub(r'\.([A-Za-z])', r'. \1', text)
    
    print("Preprocessed Text:", text[:500])  # Debug preprocessed text
    return text

def chunk_text(text):
    """Splits text into topic-based chunks using BERTopic."""
    # Sentence tokenization
    sentences = sent_tokenize(text)
    print("Tokenized Sentences:", sentences[:5])  # Debug first 5 sentences
    
    # Use BERTopic to detect topic shifts
    topic_model = BERTopic()
    topics, _ = topic_model.fit_transform(sentences)
    print("Detected Topics:", topics[:5])  # Debug first 5 topics

    chunks = []
    current_chunk = []
    last_topic = topics[0]

    for i, sentence in enumerate(sentences):
        if topics[i] != last_topic:
            chunks.append(" ".join(current_chunk))
            current_chunk = []
        current_chunk.append(sentence)
        last_topic = topics[i]

    if current_chunk:
        chunks.append(" ".join(current_chunk))

    print("Generated Chunks:", chunks[:5])  # Debug first 5 chunks
    return chunks