# Google News Adverse Media Search Service

This is a Python-based web service that uses the Google News to perform searches based on a specified subject and a list of adverse media keywords.

## Features

- **Synchronous Web Service**: Designed to be simple without asynchronous complexity.
- **Input Parameters**:
  - Search subject (string)
  - Adverse media keywords (list of strings)
- **Functionality**:
  - Searches Google News within the last 3 months
  - Cleans article URLs to remove Google tracking parameters.
  - Evaluates each article's relevance based on subject and adverse media keywords.
  - Assigns a relevance score to each article (expressed as a percentage).
  - **NEW**: Entity analysis using Named Entity Recognition (NER) to extract entities from search results.
- **Response Structure**:
  1. Total count of relevant articles
  2. List of results, where each result includes:
     - title (string)
     - link (URL to the article)
     - summary (brief description, max 2 lines)
     - relevance score (percentage)
  3. **NEW**: Entity analysis (optional) - list of dictionaries with entity_type: entity_name pairs for each search result

## Usage

1. **Set Up Virtual Environment**:
   - Navigate to the project folder and create a virtual environment:
     ```bash
     python -m venv venv
     ```
   - Activate the virtual environment:
     - On Windows (PowerShell):
       ```bash
       .\venv\Scripts\Activate.ps1
       ```
     - On Windows (Command Prompt):
       ```bash
       .\venv\Scripts\activate.bat
       ```
     - On macOS/Linux:
       ```bash
       source venv/bin/activate
       ```

2. **Install Dependencies**:
   - With the virtual environment activated, install required packages:
     ```bash
     pip install -r requirements.txt
     ```
   - Install the spaCy English language model:
     ```bash
     python -m spacy download en_core_web_sm
     ```

3. **Run the Service**:
   - Start the web service by running:
     ```bash
     python app.py
     ```
   - The service will be available at `http://localhost:5000`

4. **API Endpoints**:
   - **Health Check**:
     - `GET /health`
     - Returns health status of the service.
   - **Search**:
     - `POST /search`
     - **Expected JSON Payload**:
       ```json
       {
         "search_subject": "Company or person name",
         "adverse_keywords": ["fraud", "lawsuit", "investigation"]
       }
       ```
     - Returns a list of relevant articles with scores.
   - **Search with Entity Analysis**:
     - `POST /search-with-entities`
     - **Expected JSON Payload** (same as `/search`):
       ```json
       {
         "search_subject": "Company or person name",
         "adverse_keywords": ["fraud", "lawsuit", "investigation"]
       }
       ```
     - Returns search results AND entity analysis for each article.
   - **Analyze Entities**:
     - `POST /analyze-entities`
     - **Expected JSON Payload**:
       ```json
       {
         "search_results": [
           {
             "title": "Article title",
             "summary": "Article summary"
           }
         ]
       }
       ```
     - Returns entity analysis for provided search results.

5. **Example Requests**:
   
   **Basic Search**:
   ```bash
   curl -X POST http://localhost:5000/search \
     -H "Content-Type: application/json" \
     -d '{"search_subject": "Tesla Inc", "adverse_keywords": ["fraud", "lawsuit", "investigation"]}'
   ```
   
   **Search with Entity Analysis**:
   ```bash
   curl -X POST http://localhost:5000/search-with-entities \
     -H "Content-Type: application/json" \
     -d '{"search_subject": "Tesla Inc", "adverse_keywords": ["fraud", "lawsuit", "investigation"]}'
   ```
   
   **Analyze Entities Only**:
   ```bash
   curl -X POST http://localhost:5000/analyze-entities \
     -H "Content-Type: application/json" \
     -d '{"search_results": [{"title": "Tesla CEO Elon Musk faces SEC investigation", "summary": "The Securities and Exchange Commission is investigating Tesla CEO..."}]}'
   ```

## Entity Analysis Feature

The service now includes Named Entity Recognition (NER) capabilities using spaCy to extract entities from search results. This feature helps identify key people, organizations, locations, and other entities mentioned in adverse media articles.

### Supported Entity Types

- **person**: People mentioned in articles
- **organization**: Companies, institutions, agencies
- **location**: Places, countries, cities
- **date**: Dates and time references
- **money**: Monetary amounts
- **event**: Named events
- **product**: Products or services
- **law**: Legal references
- **facility**: Buildings, airports, etc.
- **group**: Nationalities, religious groups
- **percentage**: Percentage values
- **quantity**: Measurements and quantities
- **ordinal**: First, second, etc.
- **cardinal**: Numbers

### Example Entity Analysis Response

```json
{
  "status": "success",
  "data": {
    "search_results": {
      "total_count": 2,
      "results": [
        {
          "title": "Tesla CEO Elon Musk faces SEC investigation",
          "link": "https://example.com/article1",
          "summary": "The Securities and Exchange Commission is investigating Tesla CEO...",
          "relevance_score": "85%"
        }
      ]
    },
    "entity_analysis": [
      {
        "person": "Elon Musk",
        "organization": "Tesla",
        "organization": "SEC"
      }
    ]
  },
  "timestamp": "2024-01-15T10:30:00"
}
```

### Use Cases for Entity Analysis

1. **Risk Assessment**: Identify key entities involved in adverse media
2. **Compliance Monitoring**: Track mentions of specific people or organizations
3. **Due Diligence**: Extract structured information from unstructured news data
4. **Relationship Mapping**: Understand connections between entities in adverse events
5. **Alert Systems**: Monitor for specific entity mentions in news

## AI Agent Test

A PowerShell script (`Google_Search_Agent.ps1`) is available in the `AI Agent Test` folder that demonstrates how to use the AI agent function as a web service. This script provides an interactive way to test the adverse media search functionality.

### Using the PowerShell Script

1. **Navigate to the AI Agent Test folder**:
   ```powershell
   cd "AI Agent Test"
   ```

2. **Run the PowerShell script**:
   ```powershell
   .\Google_Search_Agent.ps1
   ```

3. **Follow the interactive prompts**:
   - Enter the search subject (e.g., "Tesla", "Microsoft", etc.)
   - Enter adverse keywords separated by commas (e.g., "fraud,lawsuit,investigation")

4. **View the results**:
   - The script will make a request to the AI agent web service
   - Results will be displayed in JSON format showing relevant articles with their relevance scores
   - Press Enter to exit when finished

### What the Script Does

- Prompts for user input (search subject and adverse keywords)
- Formats the input into a proper JSON request
- Sends a POST request to the AI agent web service endpoint
- Displays the formatted response with article results and relevance scores
- Provides an easy way to test the service without manually crafting API requests

**Note**: The script is configured to work with a specific AI agent web service endpoint. Make sure the service is running and accessible before using the script.

## License

This project is licensed under the MIT License.

