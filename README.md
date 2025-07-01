# Google News Adverse Media Search Service

This is a Python-based web service that uses the Google News to perform searches based on a specified subject and a list of adverse media keywords.

## Features

- **Synchronous Web Service**: Designed to be simple without asynchronous complexity.
- **Input Parameters**:
  - API key (string)
  - Search subject (string)
  - Adverse media keywords (list of strings)
- **Functionality**:
  - Searches Google News for articles related to the search subject.
  - Evaluates each article's relevance based on subject and adverse media keywords.
  - Assigns a relevance score to each article (expressed as a percentage).
- **Response Structure**:
  1. Total count of relevant articles
  2. List of results, where each result includes:
     - title (string)
     - link (URL to the article)
     - summary (brief description, max 2 lines)
     - relevance score (percentage)

## Usage

1. **Install Dependencies**:
   - Navigate to the project folder and install required packages:
     ```bash
     pip install -r requirements.txt
     ```

2. **Run the Service**:
   - Start the web service by running:
     ```bash
     python app.py
     ```
   - The service will be available at `http://localhost:5000`

3. **API Endpoints**:
   - **Health Check**:
     - `GET /health`
     - Returns health status of the service.
   - **Search**:
     - `POST /search`
     - **Expected JSON Payload**:
       ```json
       {
         "api_key": "your_api_key",
         "search_subject": "Company or person name",
         "adverse_keywords": ["fraud", "lawsuit", "investigation"]
       }
       ```
     - Returns a list of relevant articles with scores.

4. **Example Request**:
   ```bash
   curl -X POST http://localhost:5000/search -H "Content-Type: application/json" -d '{"api_key": "your_api_key", "search_subject": "Some Subject", "adverse_keywords": ["keyword1", "keyword2"]}'
   ```

## License

This project is licensed under the MIT License.

