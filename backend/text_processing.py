import nltk
import spacy
from bertopic import BERTopic
from nltk.tokenize import sent_tokenize

nltk.download("punkt")
nlp = spacy.load("en_core_web_sm")

def preprocess_text(text):
    """Cleans text by removing extra spaces, special characters, etc."""
    return " ".join(text.split())

def chunk_text(text):
    """Splits text into topic-based chunks using BERTopic."""
    # Sentence tokenization
    sentences = sent_tokenize(text)
    
    # Use BERTopic to detect topic shifts
    topic_model = BERTopic()
    topics, _ = topic_model.fit_transform(sentences)

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

    return chunks
