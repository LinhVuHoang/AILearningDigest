# AI Learning Digest

An automated AI news aggregation and notification workflow built with n8n, Python, Google Gemini, PostgreSQL, and Telegram.

The system collects AI-related articles from the Hugging Face Blog RSS feed, filters the latest articles, detects duplicates, and sends notifications through Telegram.

## Architecture

```text
Schedule Trigger
       |
       v
   RSS Feed
       |
       v
 Python Processing
       |
       v
   PostgreSQL
       |
       v
 IF: New Articles?
    /       \
  True      False
   |          |
   v          v
 Gemini     End
   |
   v
 Telegram
```

## Tech Stack

- **Workflow Automation:** n8n
- **Programming Language:** Python
- **LLM:** Google Gemini API
- **Database:** PostgreSQL
- **Notification:** Telegram Bot API
- **Containerization:** Docker

## Features

- Automatically fetches AI news from RSS feeds.
- Processes a limited number of recent RSS articles.
- Filters articles based on the latest publication date.
- Stores article information in PostgreSQL.
- Prevents duplicate articles using a unique URL constraint.
- Uses conditional execution to skip LLM processing when no new articles are found.
- Generates a formatted AI news digest using Gemini.
- Sends notifications through Telegram.
- Supports scheduled execution.

## Project Structure

```text
AI-Learning-Digest/
├── workflow/
│   └── ai-learning-digest.json
├── scripts/
│   └── process_rss.py
├── database/
│   └── schema.sql
├── prompts/
│   └── digest_prompt.txt
├── docker-compose.yml
├── .env
├── .gitignore
└── README.md
```

## RSS Source

Hugging Face Blog RSS:

https://huggingface.co/blog/feed.xml

## Database

Database name: `ai_learning_digest`

Table: `rss_articles`

| Column | Type | Description |
|---|---|---|
| id | BIGSERIAL | Primary key |
| title | TEXT | Article title |
| link | TEXT | Article URL, unique |
| created_at | TIMESTAMPTZ | Record creation time |

## Workflow Logic

1. Schedule Trigger starts the workflow at the configured time.
2. RSS Feed retrieves recent articles.
3. Python processes RSS items and selects articles from the latest publication date.
4. PostgreSQL checks for duplicate URLs and inserts only new articles.
5. IF node checks the returned status:
   - `NEW`: Continue to Gemini and Telegram.
   - `NONE`: Stop the workflow.
6. Gemini formats the article information.
7. Telegram sends the notification.

## Setup

### 1. Start n8n

```bash
docker compose up -d
```

Open:

http://localhost:5678

### 2. Create PostgreSQL Database

```sql
CREATE DATABASE ai_learning_digest;
```

Connect to the database and execute:

```sql
\c ai_learning_digest
```

Then run the SQL script:

```text
database/schema.sql
```

### 3. Configure Credentials in n8n

Configure the following credentials directly in n8n:

- PostgreSQL connection
- Google Gemini API
- Telegram Bot API

Do not commit API keys, bot tokens, or database passwords to Git.

### 4. Import Workflow

Import `workflow/ai-learning-digest.json` into n8n.

Verify the credentials and node configurations before activating the workflow.

### 5. Activate Workflow

Save and activate the workflow to enable scheduled execution.

## Notes

- The project is designed as a learning and personal automation project.
- PostgreSQL stores processed article URLs to prevent duplicate processing.
- Workflow credentials are managed separately from the exported workflow.
