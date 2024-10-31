import sys
import re
import json
import magic
import PyPDF2
import docx
import spacy
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.probability import FreqDist
from collections import Counter
from langdetect import detect

import matplotlib.pyplot as plt
from wordcloud import WordCloud
from nltk.stem import WordNetLemmatizer
# S'assurer que les ressources NLTK nécessaires sont téléchargées
import nltk
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

# Charger le modèle spaCy
nlp = spacy.load("en_core_web_sm")

def read_file(file_path):
    file_type = magic.from_file(file_path, mime=True)
    content = ""

    if file_type == 'application/pdf':
        with open(file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            for page in range(len(reader.pages)):
                content += reader.pages[page].extract_text()
    elif file_type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
        doc = docx.Document(file_path)
        for paragraph in doc.paragraphs:
            content += paragraph.text
    else:
        with open(file_path, 'r') as file:
            content = file.read()

    return content, file_type

def clean_content(content):
    # Supprimer les espaces inutiles, les retours à la ligne, etc.
    content = re.sub(r'\s+', ' ', content)
    return content

def analyze_sensitive_info(content):
    # Détection des emails et numéros de téléphone avec des expressions régulières
    emails = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', content)
    phone_numbers = re.findall(r'\b(?:\+\d{1,3}\s?)?\(?\d{2,3}\)?[\s.-]?\d{2,4}[\s.-]?\d{2,4}[\s.-]?\d{2,4}\b', content)
    
    # Utiliser spaCy pour détecter les entités nommées
    doc = nlp(content)
    for ent in doc.ents:
        if ent.label_ == "EMAIL":
            emails.append(ent.text)
        elif ent.label_ == "PHONE":
            phone_numbers.append(ent.text)
    
    # Nettoyer les doublons
    emails = list(set(emails))
    phone_numbers = list(set(phone_numbers))
    
    sensitive_info = {
        "emails": emails,
        "phone_numbers": phone_numbers,
    }
    return f"Sensitive Information Detected: {json.dumps(sensitive_info)}"

def analyze_vulnerability(content):
    # Extended list of vulnerability-related keywords in English and French
    keywords = {
        "en": [
            "vulnerability", "security flaw", "security defect", "weakness",
            "attack", "hacking", "breach", "intrusion", "phishing", "denial of service",
            "exploit", "takeover", "malware", "virus", "trojan", "worm", "ransomware",
            "spyware", "adware", "scam", "online fraud", "sensitive data", "privacy",
            "data leak", "identity theft", "encryption", "decryption", "cryptographic key",
            "SSL certificate", "digital signature", "password", "authentication", 
            "two-factor authentication", "biometrics"
        ],
        "fr": [
            "vulnérabilité", "faille de sécurité", "défaut de sécurité", "point faible",
            "attaque", "piratage", "intrusion", "hameçonnage", "déni de service",
            "exploitation", "prise de contrôle", "logiciel malveillant", "virus", 
            "cheval de Troie", "ver", "rançongiciel", "spyware", "adware", "escroquerie",
            "fraude en ligne", "données sensibles", "confidentialité", "fuite de données",
            "vol d'identité", "chiffrement", "déchiffrement", "clé cryptographique", 
            "certificat SSL", "signature numérique", "mot de passe", "authentification", 
            "double authentification", "biométrie"
        ],
    }

    # Tokenize the content and convert to lowercase
    tokens = word_tokenize(content.lower())

    # Search for keywords in both English and French
    found_keywords = []
    for lang, words in keywords.items():
        found_keywords += [(word, lang) for word in tokens if word in words]

    # Return the result with a comment on whether keywords were found or not
    if found_keywords:
        return found_keywords, "Keywords detected indicating possible vulnerabilities."
    else:
        return found_keywords, "No keywords detected. The document seems clean."

def analyze_content(content):
    # Initialiser le lemmatiseur
    lemmatizer = WordNetLemmatizer()

    # Tokenisation
    words = word_tokenize(content.lower())

    # Suppression des mots non-alphanumériques et des stopwords
    stop_words = set(stopwords.words('english'))
    filtered_words = [word for word in words if word.isalnum() and word not in stop_words]

    # Lemmatisation
    lemmatized_words = [lemmatizer.lemmatize(word) for word in filtered_words]

    # Calcul de la distribution de fréquence
    freq_dist = FreqDist(lemmatized_words)

    # Extraction des 10 mots les plus fréquents
    most_common = freq_dist.most_common(10)

    # Affichage des résultats
    result = f"Content Analysis: Most Common Words {most_common}"
    
    # Générer un nuage de mots
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(freq_dist)
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.show() 
    
    return result

def analyze_regulation_compliance(content):
    gdpr_keywords = ['gdpr', 'consent', 'data protection', 'privacy']
    words = word_tokenize(content.lower())
    found_gdpr = [word for word in words if word in gdpr_keywords]
    # Afficher les mots trouvés pour débogage
    print(f"Words found in content: {Counter(found_gdpr)}")
    return f"Regulation Compliance: Found GDPR Keywords {Counter(found_gdpr)}"

# analyze_regulation_compliance aide à identifier la présence et la fréquence de termes liés à la conformité réglementaire, 
# notamment ceux liés au GDPR, dans un document textuel.

def validate_format(file_type):
    valid_types = ['application/pdf', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', 'text/plain']
    if file_type in valid_types:
        return f"Format Validation: File type {file_type} is valid."
    else:
        return f"Format Validation: File type {file_type} is invalid."

def assess_quality(content):
    language = detect(content)
    num_words = len(word_tokenize(content))
    quality_score = 'High' if num_words > 100 and language == 'en' else 'Low'
    return f"Quality Assessment: Language detected: {language}, Quality Score: {quality_score}"

def analyze_document(file_path, analysis_type):
    content, file_type = read_file(file_path)
    content = clean_content(content)  # Nettoyer le contenu

    if analysis_type == 'sensitiveInfo':
        result = analyze_sensitive_info(content)
    elif analysis_type == 'vulnerability':
        result = analyze_vulnerability(content)
    elif analysis_type == 'regulationCompliance':
        result = analyze_regulation_compliance(content)
    elif analysis_type == 'contentAnalysis':
        result = analyze_content(content)
    elif analysis_type == 'formatValidation':
        result = validate_format(file_type)
    elif analysis_type == 'qualityAssessment':
        result = assess_quality(content)
    else:
        result = f"Unknown analysis type for {file_path}"
    
    return result
#return json.dumps({"analysisType": analysis_type, "result": result})

if __name__ == "__main__":
    file_path = sys.argv[1]
    analysis_type = sys.argv[2]
    print(analyze_document(file_path, analysis_type))
