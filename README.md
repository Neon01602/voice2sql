Got it — here’s your **plain-text, no-emoji, compiler-friendly README** for the **Voice2SQL** project.

---

````markdown
# Voice2SQL — Natural Language to SQL with Gemini API

Voice2SQL is a Python-based command-line tool that converts spoken natural language queries into executable SQL statements using Google's Gemini API, and runs them directly on your database (SQLite, MySQL, or PostgreSQL).

## Features
- Voice recognition via `speech_recognition` and Google Speech-to-Text
- AI-powered SQL generation using Gemini API
- Multi-database support: SQLite, MySQL, PostgreSQL
- Interactive workflow with query confirmation
- Live execution and result display

## Installation

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/voice2sql.git
cd voice2sql
````

### 2. Install dependencies

Make sure you have Python 3.10+ installed, then run:

```bash
pip install -r requirements.txt
```

Example `requirements.txt`:

```
requests
SpeechRecognition
pyaudio
mysql-connector-python
psycopg2
```

Note: On some systems, `pyaudio` requires additional OS-specific installation. See: [https://people.csail.mit.edu/hubert/pyaudio/](https://people.csail.mit.edu/hubert/pyaudio/)

## API Key Setup

This project uses the Google Gemini API.

1. Create a project in Google AI Studio: [https://aistudio.google.com/](https://aistudio.google.com/)
2. Enable the Gemini API and obtain your API key.
3. Set the API key as an environment variable:

   ```bash
   export GEMINI_API_KEY="your_api_key_here"
   ```
4. The script will read the API key from the environment.

## Usage

Run the script:

```bash
python voice2sql.py
```

Steps:

1. Choose your database type:

   * sqlite: Enter the .db file path
   * mysql / postgresql: Enter host, port, username, password, and database name
2. Speak your query when prompted
3. Gemini converts it into SQL
4. Confirm the generated SQL before execution
5. View results in the console

## Example

Voice input:

```
Show me all customers who joined after January 2023.
```

Generated SQL (PostgreSQL):

```sql
SELECT * FROM customers WHERE join_date > '2023-01-01';
```

## Limitations

* Requires a working microphone for voice input
* Speech-to-text may misinterpret certain words or names
* Always verify AI-generated SQL before running in production
* Your API key is sensitive — do not commit it to version control

## Development and Testing

If you do not have a microphone or live database:

* Replace `get_voice_input()` with manual text input
* Use in-memory SQLite:

```python
sqlite3.connect(":memory:")
```


