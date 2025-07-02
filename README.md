# Google News Adverse Media Search Service

This is a Python-based web service that uses the Google News to perform searches based on a specified subject and a list of adverse media keywords.

## Features

- **Synchronous Web Service**: Designed to be simple without asynchronous complexity.
- **Input Parameters**:
  - Search subject (string)
  - Adverse media keywords (list of strings)
- **Functionality**:
  - Cleans article URLs to remove Google tracking parameters.
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

5. **Example Request**:
   ```bash
   curl -X POST http://localhost:5000/search -H "Content-Type: application/json" -d '{"search_subject": "Some Subject", "adverse_keywords": ["keyword1", "keyword2"]}'
   ```

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

