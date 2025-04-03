# import re
# import nltk
# import spacy
# from nltk.tokenize import sent_tokenize
# from sklearn.feature_extraction.text import TfidfVectorizer

# # Ensure NLTK punkt is downloaded
# nltk.download('punkt')

# # Load spaCy's English model
# nlp = spacy.load("en_core_web_sm")


# def extract_keywords_tfidf(context, top_n=10):
#     """
#     Extracts top keywords from the context using TF-IDF.
#     """
#     vectorizer = TfidfVectorizer(stop_words="english", max_features=top_n)
#     tfidf_matrix = vectorizer.fit_transform([context])
#     keywords = vectorizer.get_feature_names_out()
#     return list(keywords)


# def extract_terms_ner(context):
#     """
#     Extracts domain-specific terms using Named Entity Recognition (NER).
#     """
#     doc = nlp(context)
#     terms = set()
    
#     for ent in doc.ents:
#         # Consider only technical or domain-specific entities
#         if ent.label_ in ["ORG", "PRODUCT", "GPE", "PERSON", "EVENT", "WORK_OF_ART"]:
#             terms.add(ent.text)

#     return list(terms)


# def evaluate_accuracy(conv, ctx, keywords):
#     """Evaluates accuracy by checking if key phrases from the context appear in the conversation."""
#     found = sum(1 for kw in keywords if re.search(kw, conv, re.IGNORECASE))
#     score = (found / len(keywords)) * 10 if keywords else 0
#     return min(score, 10)


# def evaluate_coherence(conv):
#     """Evaluates coherence by analyzing sentence length as a proxy for natural flow."""
#     sentences = sent_tokenize(conv)
#     lengths = [len(s.split()) for s in sentences if s.strip()]
    
#     if not lengths:
#         return 0

#     avg_length = sum(lengths) / len(lengths)

#     if avg_length < 10:
#         score = (avg_length / 10) * 10
#     elif avg_length > 20:
#         score = (20 / avg_length) * 10
#     else:
#         score = 10

#     return min(score, 10)


# def evaluate_depth(conv, terms):
#     """Evaluates depth by counting the presence of advanced domain-related terms."""
#     found = sum(1 for term in terms if re.search(term, conv, re.IGNORECASE))
#     score = (found / len(terms)) * 10 if terms else 0
#     return min(score, 10)


# def evaluate_engagement(conv):
#     """Evaluates engagement by comparing the balance of turns between the speakers."""
#     turns_a = conv.count("Person A")
#     turns_b = conv.count("Person B")
#     balance = min(turns_a, turns_b) / max(turns_a, turns_b) if max(turns_a, turns_b) > 0 else 0
#     score = balance * 10
#     return min(score, 10)


# def evaluate_grammar(conv):
#     """Evaluates grammar with a basic check for proper punctuation at the end of sentences."""
#     errors = 0
#     sentences = sent_tokenize(conv)

#     for s in sentences:
#         if not re.search(r'[.!?]$', s.strip()):
#             errors += 1

#     error_rate = errors / len(sentences) if sentences else 1
#     print("error rate: ",error_rate)
#     score = max(10 - error_rate * 10, 0)
#     return min(score, 10)


# def evaluate_relevance(conv):
#     """Evaluates relevance by counting the number of follow-up questions."""
#     questions = re.findall(r'\?', conv)
#     score = min(len(questions) * 2, 10)
#     return score


# def evaluate_conversation(conv, ctx):
#     """
#     Main function to evaluate a conversation using dynamically extracted keywords & terms.
#     """
#     keywords = extract_keywords_tfidf(ctx, top_n=10)
#     terms = extract_terms_ner(ctx)

#     scores = {
#         "accuracy": evaluate_accuracy(conv, ctx, keywords),
#         "coherence": evaluate_coherence(conv),
#         "depth": evaluate_depth(conv, terms),
#         "engagement": evaluate_engagement(conv),
#         "grammar": evaluate_grammar(conv),
#         "relevance": evaluate_relevance(conv)
#     }
#     scores["average"] = sum(scores.values()) / len(scores)

#     return scores, keywords, terms


# # ============================
# # 🚀 Example Usage
# # ============================

# conversation = """
# Person A : A DBMS is a software system designed to store, manage, and retrieve data efficiently.\nPerson B : That's correct! It allows for the storage, management, and retrieval of data in an organized and secure manner. Database management systems play a crucial role in data-driven applications and businesses.\nPerson A : Yes, indeed! They are essential for any system that relies on data to function effectively. There are various DBMS types, but the most common ones are Relational, NoSQL, and Object-oriented.\nPerson B : Interesting! Could you elaborate on the differences between these types and how they are used in various scenarios?\nPerson A : Of course! Relational DBMS (RDBMS) organizes data in tables with rows and columns, using a relational model for data representation. This is the most widely used type of DBMS. NoSQL DBMS, on the other hand, does not use the traditional method and offers alternative ways to store and access data, such as key-value, document, and graph databases. Object-oriented DBMS (OODBMS) stores data in the form of objects, allowing for complex relationships and hierarchies between data.\nPerson B : That's insightful! So, when might one choose to use NoSQL or Object-oriented DBMS over a traditional RDBMS?\nPerson A : NoSQL and OODBMS are often used for applications with large volumes of unstructured or semi-structured data, such as social media platforms, content management systems, and IoT applications. They offer better performance and scalability for such scenarios.\nPerson B : Thanks for the explanation! So, when someone interacts with a DBMS, what are some common ways to do so, and how would one go about designing a database schema?\nPerson A : Typically, people use SQL queries to retrieve, manipulate, and manage data in a relational database. For other types of DBMS, interaction can be through specific query languages or APIs. Database design involves data modeling, which is the process of designing a database schema to accommodate the data and relationships required by an application. There are various data modeling techniques, such as Entity-Relationship (ER) diagrams, which visually represent the relationships between data entities.\nPerson B : I see! SQL is the standard language for querying and managing data in RDBMS, but are there any graphical user interfaces or database management tools that can help with database design and maintenance?\nPerson A : Yes, there are many graphical user interfaces (GUIs) available for designing, building, and maintaining a database. Examples include Oracle SQL Developer, MySQL Workbench, and Microsoft SQL Server Management Studio. These tools offer intuitive interfaces for creating tables, managing schema, and executing SQL queries.\nPerson B : That sounds useful! Also, I've heard about database administration and the importance of maintaining a database. What does this entail, and why is it crucial?\nPerson A : Database administration involves monitoring and maintaining a database to ensure its performance, security, and recovery capabilities. This includes tasks such as backups, restores, security management, performance tuning, and database design changes. The importance of database administration lies in ensuring data integrity, availability, and recoverability, which are essential for any data-driven application or business. Without proper database administration, a database may become slow, unstable, or prone to errors, leading to lost data or system downtime.\nPerson B : Thanks for explaining that! It all makes sense now. I appreciate your detailed responses on the intricacies of DBMS and how they are used in various scenarios.\nPerson A : You're welcome! I'm glad I could help. If you have any more questions, don't hesitate to ask!
# """

# context = """
#  1. DBMS (DataBase Management System) is a software system designed to store, manage, and retrieve data efficiently.\n    2. DBMS (DataBase Management System) is a software system that allows for the storage, management, and retrieval of data in an organized and secure manner.\n    3. DBMS (DataBase Management System) is a software system specifically designed for the purpose of storing, managing, and retrieving data efficiently.\n\nTo further expand on the topic:\n\n1. Concepts of DBMS:\n   - Schema: A set of related tables, views, and other database objects that define the structure of a database.\n   - Queries: A request for data from the database, typically in the form of SQL (Structured Query Language) statements.\n   - Transactions: A collection of operations that must be performed together and in sequence, ensuring data integrity.\n   - Concurrent access: The ability for multiple users to access, modify, and update data simultaneously without causing conflicts or errors.\n   - Recovery: The process of restoring a database to a consistent state after errors or system failures.\n\n2. Types of DBMS:\n   - Relational DBMS (RDBMS): A type of DBMS that organizes data in tables with rows and columns, using a relational model for data representation.\n   - NoSQL DBMS: A category of DBMS that does not use the traditional relational model, offering alternative ways to store and access data, such as key-value, document, and graph databases.\n   - Object-oriented DBMS (OODBMS): A type of DBMS that stores data in the form of objects, allowing for complex relationships and hierarchies between data.\n\n3. Interacting with a DBMS:\n   - SQL: A standard language for querying, manipulating, and managing data in a relational database.\n   - Database management tools: Graphical user interfaces (GUIs) for designing, building, and maintaining a database.\n   - APIs: Application programming interfaces that allow software applications to access and interact with a DBMS.\n   - Data modeling: The process of designing a database schema to accommodate the data and relationships required by an application.\n   - Database administration: The tasks involved in monitoring and maintaining a database, such as backup and recovery, security, and performance tuning.
# """

# # Evaluate
# scores, extracted_keywords, extracted_terms = evaluate_conversation(conversation, context)

# # Print Results
# print("\n📌 Evaluation Scores:")
# for criterion, score in scores.items():
#     print(f"{criterion.capitalize()}: {score:.2f}")

# print("\n🔹 Extracted Keywords:", extracted_keywords)
# print("🔹 Extracted Terms:", extracted_terms)
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from sentence_transformers import SentenceTransformer, util
import nltk
from nltk.translate.bleu_score import sentence_bleu
from rouge_score import rouge_scorer

# Download necessary NLTK data
nltk.download('punkt')

# ---------------------------
# Load SentenceTransformer for Semantic Similarity
embedding_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# ---------------------------
# Load Mistral-7B-Instruct-v0.3 for Perplexity Calculation
model_name = "mistralai/Mistral-7B-Instruct-v0.3"
model = AutoModelForCausalLM.from_pretrained(model_name, torch_dtype=torch.float16, device_map="auto")
tokenizer = AutoTokenizer.from_pretrained(model_name)

# Example Context and Generated Conversation

context = """1. DBMS (DataBase Management System) is a software system designed to store, manage, and retrieve data efficiently.\n    2. DBMS (DataBase Management System) is a software system that allows for the storage, management, and retrieval of data in an organized and secure manner.\n    3. DBMS (DataBase Management System) is a software system specifically designed for the purpose of storing, managing, and retrieving data efficiently.\n\nTo further expand on the topic:\n\n1. Concepts of DBMS:\n   - Schema: A set of related tables, views, and other database objects that define the structure of a database.\n   - Queries: A request for data from the database, typically in the form of SQL (Structured Query Language) statements.\n   - Transactions: A collection of operations that must be performed together and in sequence, ensuring data integrity.\n   - Concurrent access: The ability for multiple users to access, modify, and update data simultaneously without causing conflicts or errors.\n   - Recovery: The process of restoring a database to a consistent state after errors or system failures.\n\n2. Types of DBMS:\n   - Relational DBMS (RDBMS): A type of DBMS that organizes data in tables with rows and columns, using a relational model for data representation.\n   - NoSQL DBMS: A category of DBMS that does not use the traditional relational model, offering alternative ways to store and access data, such as key-value, document, and graph databases.\n   - Object-oriented DBMS (OODBMS): A type of DBMS that stores data in the form of objects, allowing for complex relationships and hierarchies between data.\n\n3. Interacting with a DBMS:\n   - SQL: A standard language for querying, manipulating, and managing data in a relational database.\n   - Database management tools: Graphical user interfaces (GUIs) for designing, building, and maintaining a database.\n   - APIs: Application programming interfaces that allow software applications to access and interact with a DBMS.\n   - Data modeling: The process of designing a database schema to accommodate the data and relationships required by an application.\n   - Database administration: The tasks involved in monitoring and maintaining a database, such as backup and recovery, security, and performance tuning."""
conversation = """Person A : A DBMS is a software system designed to store, manage, and retrieve data efficiently.\nPerson B : That's correct! It allows for the storage, management, and retrieval of data in an organized and secure manner. Database management systems play a crucial role in data-driven applications and businesses.\nPerson A : Yes, indeed! They are essential for any system that relies on data to function effectively. There are various DBMS types, but the most common ones are Relational, NoSQL, and Object-oriented.\nPerson B : Interesting! Could you elaborate on the differences between these types and how they are used in various scenarios?\nPerson A : Of course! Relational DBMS (RDBMS) organizes data in tables with rows and columns, using a relational model for data representation. This is the most widely used type of DBMS. NoSQL DBMS, on the other hand, does not use the traditional method and offers alternative ways to store and access data, such as key-value, document, and graph databases. Object-oriented DBMS (OODBMS) stores data in the form of objects, allowing for complex relationships and hierarchies between data.\nPerson B : That's insightful! So, when might one choose to use NoSQL or Object-oriented DBMS over a traditional RDBMS?\nPerson A : NoSQL and OODBMS are often used for applications with large volumes of unstructured or semi-structured data, such as social media platforms, content management systems, and IoT applications. They offer better performance and scalability for such scenarios.\nPerson B : Thanks for the explanation! So, when someone interacts with a DBMS, what are some common ways to do so, and how would one go about designing a database schema?\nPerson A : Typically, people use SQL queries to retrieve, manipulate, and manage data in a relational database. For other types of DBMS, interaction can be through specific query languages or APIs. Database design involves data modeling, which is the process of designing a database schema to accommodate the data and relationships required by an application. There are various data modeling techniques, such as Entity-Relationship (ER) diagrams, which visually represent the relationships between data entities.\nPerson B : I see! SQL is the standard language for querying and managing data in RDBMS, but are there any graphical user interfaces or database management tools that can help with database design and maintenance?\nPerson A : Yes, there are many graphical user interfaces (GUIs) available for designing, building, and maintaining a database. Examples include Oracle SQL Developer, MySQL Workbench, and Microsoft SQL Server Management Studio. These tools offer intuitive interfaces for creating tables, managing schema, and executing SQL queries.\nPerson B : That sounds useful! Also, I've heard about database administration and the importance of maintaining a database. What does this entail, and why is it crucial?\nPerson A : Database administration involves monitoring and maintaining a database to ensure its performance, security, and recovery capabilities. This includes tasks such as backups, restores, security management, performance tuning, and database design changes. The importance of database administration lies in ensuring data integrity, availability, and recoverability, which are essential for any data-driven application or business. Without proper database administration, a database may become slow, unstable, or prone to errors, leading to lost data or system downtime.\nPerson B : Thanks for explaining that! It all makes sense now. I appreciate your detailed responses on the intricacies of DBMS and how they are used in various scenarios.\nPerson A : You're welcome! I'm glad I could help. If you have any more questions, don't hesitate to ask!"""


##############################################
# 1. Compute Perplexity using the Mistral Model
##############################################
def compute_perplexity(text, model, tokenizer):
    inputs = tokenizer(text, return_tensors="pt").to("cuda")
    model.eval()
    with torch.no_grad():
        outputs = model(**inputs, labels=inputs["input_ids"])
    loss = outputs.loss
    perplexity = torch.exp(loss)
    return perplexity.item()

ppl = compute_perplexity(conversation, model, tokenizer)
print(f"Perplexity: {ppl}")


##############################################
# 2. Compute Cosine Similarity via SentenceTransformer
##############################################
# Encode both texts into embeddings
context_embedding = embedding_model.encode(context, convert_to_tensor=True)
conversation_embedding = embedding_model.encode(conversation, convert_to_tensor=True)

# Compute cosine similarity
cosine_score = util.pytorch_cos_sim(context_embedding, conversation_embedding)
print(f"Cosine Similarity: {cosine_score.item()}")


##############################################
# 3. Compute BLEU Score using NLTK
##############################################
# Tokenize reference (context) and candidate (conversation)
reference_tokens = [nltk.word_tokenize(context)]
candidate_tokens = nltk.word_tokenize(conversation)

# Calculate BLEU score
bleu_score = sentence_bleu(reference_tokens, candidate_tokens)
print(f"BLEU Score: {bleu_score}")


##############################################
# 4. Compute ROUGE Scores using rouge-score
##############################################
scorer = rouge_scorer.RougeScorer(['rouge1', 'rougeL'], use_stemmer=True)
rouge_scores = scorer.score(context, conversation)

print("ROUGE Scores:")
for key, score_val in rouge_scores.items():
    print(f"  {key}: {score_val}")
