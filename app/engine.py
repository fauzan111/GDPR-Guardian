import spacy
from presidio_analyzer import AnalyzerEngine
from presidio_analyzer.nlp_engine import NlpEngineProvider
from presidio_anonymizer import AnonymizerEngine

configuration = {
    "nlp_engine_name": "spacy",
    "models": [
        {"lang_code": "it", "model_name": "it_core_news_lg"},
        {"lang_code": "en", "model_name": "en_core_web_lg"},
    ],
}
provider = NlpEngineProvider(nlp_configuration=configuration)
nlp_engine = provider.create_engine()

analyzer = AnalyzerEngine(
    nlp_engine=nlp_engine, 
    supported_languages=["it", "en"]
)

anonymizer = AnonymizerEngine()

def anonymize_text(text: str, language: str = "it") -> str:
    """
    Analyzes text for PII and replaces it with <ENTITY_TYPE>.
    """
    results = analyzer.analyze(text=text, language=language)
  
    anonymized_result = anonymizer.anonymize(
        text=text,
        analyzer_results=results
    )
    
    return anonymized_result.text
