import spacy
from presidio_analyzer import AnalyzerEngine
from presidio_analyzer.nlp_engine import NlpEngineProvider
from presidio_anonymizer import AnonymizerEngine

# 1. Configure the NLP Engine to use the Italian spaCy model
configuration = {
    "nlp_engine_name": "spacy",
    "models": [
        {"lang_code": "it", "model_name": "it_core_news_lg"},
        {"lang_code": "en", "model_name": "en_core_web_lg"},
    ],
}

# Initialize the NLP engine (Spacy)
provider = NlpEngineProvider(nlp_configuration=configuration)
nlp_engine = provider.create_engine()

# 2. Initialize the Analyzer Engine
# FIX: We remove the manual 'registry' setup. 
# By passing 'supported_languages' and 'nlp_engine' here, 
# the Analyzer will automatically load the correct Italian recognizers for us.
analyzer = AnalyzerEngine(
    nlp_engine=nlp_engine, 
    supported_languages=["it", "en"]
)

# 3. Initialize the Anonymizer
anonymizer = AnonymizerEngine()

def anonymize_text(text: str, language: str = "it") -> str:
    """
    Analyzes text for PII and replaces it with <ENTITY_TYPE>.
    """
    # Step A: Analyze (Find the PII)
    results = analyzer.analyze(text=text, language=language)
    
    # Step B: Anonymize (Redact the PII)
    anonymized_result = anonymizer.anonymize(
        text=text,
        analyzer_results=results
    )
    
    return anonymized_result.text