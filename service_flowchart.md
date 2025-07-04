# Google News Adverse Media Search Service - Flowchart

## Service Architecture Flow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                      Google News Adverse Media Search Service               │
└─────────────────────────────────────────────────────────────────────────────┘
                                        │
                                        ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                              Flask Web Server                               │
│                         (Running on port 5000)                             │
└─────────────────────────────────────────────────────────────────────────────┘
                                        │
                                        ▼
              ┌─────────────────────────────────────────────────────┐
              │                    API Endpoints                    │
              │                                                     │
              │  ┌─────────────────┐    ┌─────────────────────────┐ │
              │  │  GET /health    │    │     POST /search        │ │
              │  │                 │    │                         │ │
              │  │ Returns:        │    │ Input: JSON payload     │ │
              │  │ - Status        │    │ - search_subject        │ │
              │  │ - Timestamp     │    │ - adverse_keywords[]    │ │
              │  └─────────────────┘    └─────────────────────────┘ │
              └─────────────────────────────────────────────────────┘
                                        │
                    ┌───────────────────┼───────────────────┐
                    │                   │                   │
                    ▼                   ▼                   ▼
          ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
          │  Health Check   │  │  Search Request │  │  Error Handler  │
          │                 │  │   Validation    │  │                 │
          │ - Simple status │  │                 │  │ - 404 handler   │
          │   response      │  │ - JSON format   │  │ - 500 handler   │
          └─────────────────┘  │ - Required      │  └─────────────────┘
                               │   fields check  │
                               │ - Type check    │
                               └─────────────────┘
                                        │
                                        ▼
                               ┌─────────────────┐
                               │   Input Valid?  │
                               └─────────────────┘
                                        │
                           ┌────────────┼────────────┐
                           │            │            │
                           ▼            ▼            ▼
                    ┌─────────────┐    │      ┌─────────────┐
                    │  Return     │    │      │  Continue   │
                    │  400 Error  │    │      │  Processing │
                    └─────────────┘    │      └─────────────┘
                                       │
                                       ▼
                              ┌─────────────────┐
                              │ AdverseMedia    │
                              │ Searcher Class  │
                              └─────────────────┘
                                       │
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                     Search Processing Pipeline                               │
│                                                                             │
│  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────────────┐ │
│  │  1. Initialize  │    │  2. Build       │    │  3. Execute Google      │ │
│  │  Google News    │ ─► │  Search Query   │ ─► │  News Search            │ │
│  │                 │    │                 │    │                         │ │
│  │ - Set language  │    │ - Combine       │    │ - Clear previous        │ │
│  │   (English)     │    │   subject +     │    │   results               │ │
│  │ - Set period    │    │   keywords      │    │ - Execute search        │ │
│  │   (7 days)      │    │ - Limit to 3    │    │ - Get raw results       │ │
│  │ - Set encoding  │    │   keywords max  │    │                         │ │
│  │   (UTF-8)       │    │                 │    │                         │ │
│  └─────────────────┘    └─────────────────┘    └─────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────┘
                                       │
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                     Article Processing Pipeline                              │
│                                                                             │
│  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────────────┐ │
│  │  4. For Each    │    │  5. Validate    │    │  6. Calculate           │ │
│  │  Article        │ ─► │  Article        │ ─► │  Relevance Score        │ │
│  │                 │    │                 │    │                         │ │
│  │ - Extract title │    │ - Check title   │    │ - Subject matching      │ │
│  │ - Extract link  │    │   exists        │    │   (up to 30 points)    │ │
│  │ - Extract desc  │    │ - Check link    │    │ - Keyword matching      │ │
│  │                 │    │   exists        │    │   (15 points each)      │ │
│  │                 │    │                 │    │ - Context bonus         │ │
│  │                 │    │                 │    │   (10 points)           │ │
│  └─────────────────┘    └─────────────────┘    └─────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────┘
                                       │
                                       ▼
                              ┌─────────────────┐
                              │ Score >= 15%?   │
                              └─────────────────┘
                                       │
                           ┌───────────┼───────────┐
                           │           │           │
                           ▼           ▼           ▼
                    ┌─────────────┐   │     ┌─────────────┐
                    │  Skip       │   │     │  Include    │
                    │  Article    │   │     │  Article    │
                    └─────────────┘   │     └─────────────┘
                                      │
                                      ▼
                             ┌─────────────────┐
                             │  7. Clean URL   │
                             │                 │
                             │ - Remove Google │
                             │   tracking      │
                             │   parameters    │
                             │ - Extract real  │
                             │   article URL   │
                             └─────────────────┘
                                      │
                                      ▼
                             ┌─────────────────┐
                             │  8. Format      │
                             │  Article Data   │
                             │                 │
                             │ - Title         │
                             │ - Clean link    │
                             │ - Summary       │
                             │   (max 200 chars)│
                             │ - Relevance %   │
                             └─────────────────┘
                                      │
                                      ▼
                             ┌─────────────────┐
                             │  9. Sort by     │
                             │  Relevance      │
                             │                 │
                             │ - Highest       │
                             │   score first   │
                             │ - Descending    │
                             │   order         │
                             └─────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                         Response Formation                                   │
│                                                                             │
│  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────────────┐ │
│  │  10. Build      │    │  11. Add        │    │  12. Return JSON        │ │
│  │  Response       │ ─► │  Metadata       │ ─► │  Response               │ │
│  │                 │    │                 │    │                         │ │
│  │ - total_count   │    │ - status        │    │ - HTTP 200 OK           │ │
│  │ - results[]     │    │ - timestamp     │    │ - Content-Type:         │ │
│  │                 │    │                 │    │   application/json      │ │
│  └─────────────────┘    └─────────────────┘    └─────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                            Error Handling                                   │
│                                                                             │
│  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────────────┐ │
│  │  Exception      │    │  Log Error      │    │  Return Error           │ │
│  │  Occurred?      │ ─► │                 │ ─► │  Response               │ │
│  │                 │    │ - Log to        │    │                         │ │
│  │ - Network error │    │   application   │    │ - HTTP 500              │ │
│  │ - API timeout   │    │   logs          │    │ - Error message         │ │
│  │ - Parse error   │    │ - Include       │    │ - Timestamp             │ │
│  │                 │    │   stack trace   │    │                         │ │
│  └─────────────────┘    └─────────────────┘    └─────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Key Components Explained

### 1. **Relevance Scoring Algorithm**
```
Total Score = Subject Score + Adverse Keywords Score + Context Bonus
- Subject Score: 0-30 points (exact match = 30, partial match = proportional)
- Adverse Keywords: 15 points per keyword + 5 bonus per additional keyword
- Context Bonus: 10 points for high-relevance terms (investigation, lawsuit, etc.)
- Maximum Score: 100 points
- Minimum Threshold: 15% to include in results
```

### 2. **URL Cleaning Process**
```
1. URL decode the Google News URL
2. Check for Google tracking parameters (ved=, google domain)
3. Extract actual article URL from 'url' parameter
4. Remove tracking parameters: ved, usg, sa, source, cd, cad
5. Return clean article URL
```

### 3. **Search Query Construction**
```
Query Format: "{search_subject} {keyword1} OR {keyword2} OR {keyword3}"
- Limited to first 3 keywords to avoid overly long queries
- Combines subject with OR logic for keywords
- Searches within last 7 days of news
```

### 4. **Data Flow Example**
```
Input:
{
  "search_subject": "Tesla Inc",
  "adverse_keywords": ["lawsuit", "investigation", "fraud", "recall"]
}

Processing:
1. Query: "Tesla Inc lawsuit OR investigation OR fraud"
2. Search Google News (7 days)
3. For each article:
   - Calculate relevance score
   - Filter if score >= 15%
   - Clean URL
   - Format response

Output:
{
  "status": "success",
  "data": {
    "total_count": 3,
    "results": [
      {
        "title": "Tesla Faces Investigation...",
        "link": "https://reuters.com/article/...",
        "summary": "Tesla is under investigation...",
        "relevance_score": "85%"
      }
    ]
  },
  "timestamp": "2025-07-04T07:15:37Z"
}
```

## Service Characteristics

- **Language**: Python (Flask framework)
- **Search Engine**: Google News API
- **Search Period**: Last 7 days
- **Language Filter**: English only
- **Scoring**: 0-100% relevance based on keyword matching
- **URL Cleaning**: Removes tracking parameters
- **Response Format**: JSON with metadata
- **Error Handling**: Comprehensive logging and error responses
- **Deployment**: Azure App Service ready
