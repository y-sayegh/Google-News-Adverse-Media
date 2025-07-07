from flask import Flask, request, jsonify
from GoogleNews import GoogleNews
import re
from datetime import datetime, timedelta
from typing import List, Dict, Any
import logging
import urllib.parse
import spacy
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    print("Warning: spaCy English model not found. Please install it with: python -m spacy download en_core_web_sm")
    nlp = None

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

class AdverseMediaSearcher:
    def __init__(self):
        self.google_news = GoogleNews()
        self.google_news.set_lang('en')
        self.google_news.set_period('3m')  # Search last 3 months
        self.google_news.set_encode('utf-8')
    
    def clean_google_url(self, url: str) -> str:
        """
        Remove Google tracking parameters from URL and extract the actual article URL
        """
        if not url:
            return url
            
        try:
            url = urllib.parse.unquote(url)
            # Check if this is a Google redirect URL with tracking parameters
            if 'ved=' in url or 'google' in url.lower():
                parsed = urllib.parse.urlparse(url)
                params = urllib.parse.parse_qs(parsed.query)
                
                # Try to extract the actual URL from 'url' parameter
                if 'url' in params:
                    actual_url = params['url'][0]
                    return actual_url
                
                # If no 'url' parameter, try to clean common Google tracking parameters
                clean_params = {k: v for k, v in params.items() 
                              if k not in ['ved', 'usg', 'sa', 'source', 'cd', 'cad']}
                
                if clean_params:
                    clean_query = urllib.parse.urlencode(clean_params, doseq=True)
                    return urllib.parse.urlunparse((
                        parsed.scheme, parsed.netloc, parsed.path,
                        parsed.params, clean_query, parsed.fragment
                    ))
                else:
                    # Return URL without query parameters if all were tracking params
                    return urllib.parse.urlunparse((
                        parsed.scheme, parsed.netloc, parsed.path,
                        parsed.params, '', parsed.fragment
                    ))
            
            return url
            
        except Exception as e:
            logger.warning(f"Failed to clean URL {url}: {str(e)}")
            return url
    
    def calculate_relevance_score(self, title: str, summary: str, subject: str, adverse_keywords: List[str]) -> float:
        """
        Calculate relevance score based on keyword matching and context analysis
        """
        text = f"{title} {summary}".lower()
        subject_lower = subject.lower()
        
        # Base score for subject match
        subject_score = 0
        if subject_lower in text:
            subject_score = 30
        else:
            # Partial match scoring
            subject_words = subject_lower.split()
            matched_words = sum(1 for word in subject_words if word in text)
            subject_score = (matched_words / len(subject_words)) * 20
        
        # Adverse keywords scoring
        adverse_score = 0
        matched_keywords = []
        for keyword in adverse_keywords:
            if keyword.lower() in text:
                matched_keywords.append(keyword)
                adverse_score += 15
        
        # Bonus for multiple keyword matches
        if len(matched_keywords) > 1:
            adverse_score += len(matched_keywords) * 5
        
        # Context relevance bonus
        context_bonus = 0
        high_relevance_terms = ['investigation', 'lawsuit', 'fraud', 'scandal', 'controversy', 'violation', 'penalty', 'fine']
        for term in high_relevance_terms:
            if term in text:
                context_bonus += 10
                break
        
        total_score = min(100, subject_score + adverse_score + context_bonus)
        return round(total_score, 2)
    
    def analyze_entities(self, search_results: List[Dict[str, Any]]) -> List[Dict[str, str]]:
        """
        Analyze search results and extract entities from titles and summaries.
        Returns a list of dictionaries with entity_type: entity_name for each search result.
        """
        if not nlp:
            logger.warning("spaCy model not loaded. Cannot perform entity analysis.")
            return []
        
        entity_analysis = []
        
        for result in search_results:
            title = result.get('title', '')
            summary = result.get('summary', '')
            
            # Combine title and summary for entity extraction
            text = f"{title} {summary}"
            
            # Process text with spaCy
            doc = nlp(text)
            
            # Extract entities and create dictionary
            entities_dict = {}
            for ent in doc.ents:
                # Map spaCy entity labels to more readable names
                entity_type = self._map_entity_type(ent.label_)
                entity_name = ent.text.strip()
                
                # Only include meaningful entities (avoid single characters, numbers, etc.)
                if len(entity_name) > 2 and not entity_name.isdigit():
                    entities_dict[entity_type] = entity_name
            
            entity_analysis.append(entities_dict)
        
        return entity_analysis
    
    def _map_entity_type(self, spacy_label: str) -> str:
        """
        Map spaCy entity labels to more readable entity types
        """
        mapping = {
            'PERSON': 'person',
            'ORG': 'organization',
            'GPE': 'location',
            'LOC': 'location',
            'NORP': 'group',
            'FACILITY': 'facility',
            'PRODUCT': 'product',
            'EVENT': 'event',
            'WORK_OF_ART': 'work_of_art',
            'LAW': 'law',
            'LANGUAGE': 'language',
            'DATE': 'date',
            'TIME': 'time',
            'PERCENT': 'percentage',
            'MONEY': 'money',
            'QUANTITY': 'quantity',
            'ORDINAL': 'ordinal',
            'CARDINAL': 'cardinal'
        }
        return mapping.get(spacy_label, spacy_label.lower())
    
    def search_adverse_media(self, subject: str, adverse_keywords: List[str]) -> Dict[str, Any]:
        """
        Search Google News for adverse media related to the subject
        """
        try:
            
            # Create search query combining subject and adverse keywords
            search_query = f"{subject} {' OR '.join(adverse_keywords[:3])}"  # Limit to first 3 keywords to avoid too long query
            
            logger.info(f"Searching for: {search_query}")
            
            # Clear previous results and search
            self.google_news.clear()
            self.google_news.search(search_query)
            
            # Get results
            results = self.google_news.results()
            
            processed_results = []
            for article in results:
                title = article.get('title', '')
                link = article.get('link', '')
                summary = article.get('desc', '')
                
                # Skip if essential fields are missing
                if not title or not link:
                    continue
                
                # Calculate relevance score
                relevance_score = self.calculate_relevance_score(
                    title, summary, subject, adverse_keywords
                )
                
                # Only include articles with minimum relevance
                if relevance_score >= 15:  # Minimum threshold
                    # Clean the URL to remove Google tracking parameters
                    clean_link = self.clean_google_url(link)
                    
                    processed_results.append({
                        'title': title,
                        'link': clean_link,
                        'summary': summary[:200] + '...' if len(summary) > 200 else summary,
                        'relevance_score': f"{relevance_score}%"
                    })
            
            # Sort by relevance score (descending)
            processed_results.sort(key=lambda x: float(x['relevance_score'].replace('%', '')), reverse=True)
            
            return {
                'total_count': len(processed_results),
                'results': processed_results
            }
            
        except Exception as e:
            logger.error(f"Error searching adverse media: {str(e)}")
            raise Exception(f"Search failed: {str(e)}")

# Initialize the searcher
adverse_media_searcher = AdverseMediaSearcher()

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()})

@app.route('/search', methods=['POST'])
def search_adverse_media():
    """
    Search for adverse media articles
    
    Expected JSON payload:
    {
        "search_subject": "Company or person name",
        "adverse_keywords": ["fraud", "lawsuit", "investigation"]
    }
    """
    try:
        # Validate request
        if not request.is_json:
            return jsonify({'error': 'Request must be JSON'}), 400
        
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['search_subject', 'adverse_keywords']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        search_subject = data['search_subject']
        adverse_keywords = data['adverse_keywords']
        
        # Validate field types
        
        if not isinstance(search_subject, str) or not search_subject.strip():
            return jsonify({'error': 'search_subject must be a non-empty string'}), 400
        
        if not isinstance(adverse_keywords, list) or len(adverse_keywords) == 0:
            return jsonify({'error': 'adverse_keywords must be a non-empty list'}), 400
        
        if not all(isinstance(kw, str) and kw.strip() for kw in adverse_keywords):
            return jsonify({'error': 'All adverse_keywords must be non-empty strings'}), 400
        
        # Perform search
        results = adverse_media_searcher.search_adverse_media(
            subject=search_subject,
            adverse_keywords=adverse_keywords
        )
        
        return jsonify({
            'status': 'success',
            'data': results,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error in search endpoint: {str(e)}")
        return jsonify({
            'status': 'error',
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

@app.route('/search-with-entities', methods=['POST'])
def search_adverse_media_with_entities():
    """
    Search for adverse media articles and analyze entities
    
    Expected JSON payload:
    {
        "search_subject": "Company or person name",
        "adverse_keywords": ["fraud", "lawsuit", "investigation"]
    }
    """
    try:
        # Validate request
        if not request.is_json:
            return jsonify({'error': 'Request must be JSON'}), 400
        
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['search_subject', 'adverse_keywords']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        search_subject = data['search_subject']
        adverse_keywords = data['adverse_keywords']
        
        # Validate field types
        if not isinstance(search_subject, str) or not search_subject.strip():
            return jsonify({'error': 'search_subject must be a non-empty string'}), 400
        
        if not isinstance(adverse_keywords, list) or len(adverse_keywords) == 0:
            return jsonify({'error': 'adverse_keywords must be a non-empty list'}), 400
        
        if not all(isinstance(kw, str) and kw.strip() for kw in adverse_keywords):
            return jsonify({'error': 'All adverse_keywords must be non-empty strings'}), 400
        
        # Perform search
        results = adverse_media_searcher.search_adverse_media(
            subject=search_subject,
            adverse_keywords=adverse_keywords
        )
        
        # Analyze entities in search results
        entity_analysis = adverse_media_searcher.analyze_entities(results['results'])
        
        return jsonify({
            'status': 'success',
            'data': {
                'search_results': results,
                'entity_analysis': entity_analysis
            },
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error in search-with-entities endpoint: {str(e)}")
        return jsonify({
            'status': 'error',
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

@app.route('/analyze-entities', methods=['POST'])
def analyze_entities():
    """
    Analyze entities in provided search results
    
    Expected JSON payload:
    {
        "search_results": [
            {
                "title": "Article title",
                "summary": "Article summary"
            }
        ]
    }
    """
    try:
        # Validate request
        if not request.is_json:
            return jsonify({'error': 'Request must be JSON'}), 400
        
        data = request.get_json()
        
        # Validate required fields
        if 'search_results' not in data:
            return jsonify({'error': 'Missing required field: search_results'}), 400
        
        search_results = data['search_results']
        
        # Validate field types
        if not isinstance(search_results, list):
            return jsonify({'error': 'search_results must be a list'}), 400
        
        if not search_results:
            return jsonify({'error': 'search_results cannot be empty'}), 400
        
        # Analyze entities
        entity_analysis = adverse_media_searcher.analyze_entities(search_results)
        
        return jsonify({
            'status': 'success',
            'data': {
                'entity_analysis': entity_analysis
            },
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error in analyze-entities endpoint: {str(e)}")
        return jsonify({
            'status': 'error',
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    
    print("Starting Google News Adverse Media Search Service...")
    print("Available endpoints:")
    print("  GET  /health - Health check")
    print("  POST /search - Search for adverse media")
    print("  POST /search-with-entities - Search for adverse media and analyze entities")
    print("  POST /analyze-entities - Analyze entities in provided search results")
    print(f"\nServer running on port {port}")
    
    app.run(debug=debug, host='0.0.0.0', port=port)
