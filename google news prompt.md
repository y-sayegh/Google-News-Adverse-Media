# Google News Adverse Media - Original Prompt

## Request

Create a folder named "Google News Adverse Media". 

Inside this folder, build a Python-based web service that uses the Google News API to perform a search based on a given subject and a list of adverse media keywords.

## Web Service Requirements

- The service should be synchronous.
- It should accept the following inputs:
  1. API key (string)
  2. Search subject (string)
  3. Adverse media keywords (list of strings)

## Functionality

- Use the provided inputs to search Google News for articles related to the search subject.
- Assess each article's relevance by analyzing how closely it matches both the subject and the adverse media keywords.
- Assign a relevance score to each article (expressed as a percentage).

## Response Structure

The web service should return:
1. Total count of relevant articles
2. List of results, where each result includes:
   - title (string)
   - link (URL to the article)
   - summary (brief description, max 2 lines)
   - relevance score (percentage)

## Git Requirements

- Create a readme.md file to explain the code and how to use it
- Create a git repo for this project and commit the first version

## Additional Context

```json
{
  "directory_state": {
    "pwd": "C:\\Users\\YoussefSayegh\\python_apps",
    "home": "C:\\Users\\YoussefSayegh"
  },
  "operating_system": {
    "platform": "Windows"
  },
  "current_time": "2025-07-01T06:11:45Z",
  "shell": {
    "name": "pwsh",
    "version": "5.1.22621.4391"
  }
}
```
