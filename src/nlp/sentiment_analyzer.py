import pandas as pd
from transformers import pipeline
import sys
from pathlib import Path

# Add the src folder to path so we can import our logger and db_utils
sys.path.append(str(Path(__file__).parent.parent / 'etl'))
from logger import get_logger
from db_utils import get_db_connection

logger = get_logger(__name__)

class FinBERTSentimentAnalyzer:
    def __init__(self):
        logger.info("Loading FinBERT NLP model from HuggingFace...")
        # ProsusAI/finbert is a popular financial sentiment model trained on financial text
        self.nlp = pipeline("sentiment-analysis", model="ProsusAI/finbert")
        logger.info("Model loaded successfully.")

    def chunk_text(self, text, max_len=400):
        """Split text into manageable chunks for BERT (max 512 tokens)."""
        words = text.split()
        return [' '.join(words[i:i+max_len]) for i in range(0, len(words), max_len)]

    def analyze_statement(self, text: str) -> float:
        """
        Analyzes a central bank statement.
        Returns a score from -1.0 (Dovish) to 1.0 (Hawkish).
        """
        if not text or len(text.strip()) == 0:
            return 0.0
            
        chunks = self.chunk_text(text, max_len=400)
        scores = []
        
        for chunk in chunks:
            # The model outputs [{'label': 'positive', 'score': 0.8}]
            result = self.nlp(chunk)[0]
            label = result['label']
            score = result['score']
            
            # Map FinBERT labels to our Hawkish (Positive) / Dovish (Negative) scale
            if label == 'positive': 
                scores.append(score)
            elif label == 'negative': 
                scores.append(-score)
            else:
                scores.append(0.0)
                
        # Average the score across the entire document
        final_score = sum(scores) / len(scores) if scores else 0.0
        return final_score

def save_nlp_score(cb_id, statement_date, doc_type, raw_text, hawkish_score):
    """Save the NLP analysis into the PostgreSQL database."""
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            insert_query = """
                INSERT INTO fact_communications (cb_id, date, doc_type, raw_text, nlp_hawkish_score)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (cb_id, date, doc_type) DO UPDATE 
                SET nlp_hawkish_score = EXCLUDED.nlp_hawkish_score;
            """
            cur.execute(insert_query, (cb_id, statement_date, doc_type, raw_text, hawkish_score))
        conn.commit()
        logger.info(f"Saved NLP score for {cb_id} on {statement_date}: {hawkish_score:.3f}")
    except Exception as e:
        conn.rollback()
        logger.error(f"Failed to save NLP score: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    # Independent Test Block
    analyzer = FinBERTSentimentAnalyzer()
    
    # Dummy FOMC Statement snippet demonstrating aggressive hiking language
    dummy_text = "The Committee remains highly attentive to inflation risks and is strongly committed to returning inflation to its 2 percent objective. We will continue to increase the target range for the federal funds rate as necessary."
    
    score = analyzer.analyze_statement(dummy_text)
    print(f"\nAnalyzed Text:\n'{dummy_text}'\n")
    print(f"Hawkish/Dovish Score: {score:.3f} (Scale: -1.0 Dovish to +1.0 Hawkish)")
